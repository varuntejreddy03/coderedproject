"""
Production-Ready Telegram Scraper for FastAPI
Handles session persistence, time drift, and polling fallback
"""
import asyncio
import os
import re
from pathlib import Path
from telethon import TelegramClient
from datetime import datetime
from typing import List, Dict, Callable, Optional
import logging

logger = logging.getLogger(__name__)

class ProductionTelegramScraper:
    def __init__(self, api_id: int, api_hash: str, channels: List[str]):
        self.api_id = api_id
        self.api_hash = api_hash
        self.channels = channels
        
        # Use absolute path for session (prevents corruption)
        session_dir = Path(__file__).parent.parent / "sessions"
        session_dir.mkdir(exist_ok=True)
        self.session_path = str(session_dir / "pumpwatch_session")
        
        # Initialize client with production settings
        self.client = TelegramClient(
            self.session_path,
            api_id,
            api_hash,
            sequential_updates=True,  # Prevents time drift issues
            connection_retries=5,
            retry_delay=1,
            timeout=10,
            flood_sleep_threshold=60
        )
        
        self.messages = []
        self.is_running = False
        self.polling_task = None
        
    async def connect(self):
        """Connect to Telegram with proper error handling"""
        try:
            await self.client.start()
            logger.info(f"✅ Telegram connected (session: {self.session_path})")
            return True
        except Exception as e:
            logger.error(f"❌ Telegram connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Properly disconnect to prevent session corruption"""
        self.is_running = False
        if self.polling_task:
            self.polling_task.cancel()
        await self.client.disconnect()
        logger.info("✅ Telegram disconnected safely")
    
    def extract_tickers(self, text: str) -> List[str]:
        """Extract stock tickers from text"""
        # Load your NSE stocks list here
        NSE_STOCKS = {'RELIANCE', 'TCS', 'INFY', 'SBIN', 'HDFCBANK', 'ICICIBANK'}
        potential = re.findall(r'\b[A-Z]{2,15}\b', text.upper())
        return [t for t in potential if t in NSE_STOCKS]
    
    def detect_fraud(self, text: str) -> int:
        """Count fraud keywords"""
        keywords = ['pakka', 'upper circuit', 'sure shot', 'guaranteed', 'multibagger']
        return sum(1 for kw in keywords if kw in text.lower())
    
    async def fetch_messages(self, limit: int = 50) -> List[Dict]:
        """Fetch messages using polling (not update handlers)"""
        all_messages = []
        
        for channel in self.channels:
            try:
                entity = await self.client.get_entity(channel)
                msgs = await self.client.get_messages(entity, limit=limit)
                
                for m in msgs:
                    if m.message:
                        tickers = self.extract_tickers(m.message)
                        if not tickers:
                            continue
                        
                        fraud_score = self.detect_fraud(m.message)
                        
                        all_messages.append({
                            'id': m.id,
                            'channel': channel,
                            'text': m.message,
                            'date': m.date,
                            'tickers': tickers,
                            'fraud_score': fraud_score
                        })
                
                logger.info(f"✅ Fetched {len(msgs)} messages from {channel}")
            except Exception as e:
                logger.error(f"❌ Error fetching from {channel}: {e}")
        
        self.messages = all_messages
        return all_messages
    
    async def start_polling(self, callback: Optional[Callable] = None, interval: int = 30):
        """
        Start background polling loop (RECOMMENDED for production)
        Polls every N seconds instead of relying on update handlers
        """
        self.is_running = True
        last_message_ids = {ch: 0 for ch in self.channels}
        
        logger.info(f"✅ Starting polling loop (every {interval}s)")
        
        while self.is_running:
            try:
                for channel in self.channels:
                    try:
                        entity = await self.client.get_entity(channel)
                        msgs = await self.client.get_messages(entity, limit=10)
                        
                        for m in msgs:
                            # Skip if already processed
                            if m.id <= last_message_ids[channel]:
                                continue
                            
                            if m.message:
                                tickers = self.extract_tickers(m.message)
                                if not tickers:
                                    continue
                                
                                fraud_score = self.detect_fraud(m.message)
                                
                                message = {
                                    'id': m.id,
                                    'channel': channel,
                                    'text': m.message,
                                    'date': m.date,
                                    'tickers': tickers,
                                    'fraud_score': fraud_score
                                }
                                
                                self.messages.append(message)
                                last_message_ids[channel] = max(last_message_ids[channel], m.id)
                                
                                logger.info(f"📥 NEW: {channel} - {tickers}")
                                
                                if callback:
                                    await callback(message)
                    
                    except Exception as e:
                        logger.error(f"❌ Polling error for {channel}: {e}")
                
                await asyncio.sleep(interval)
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Polling loop error: {e}")
                await asyncio.sleep(interval)
    
    def get_all_tickers(self) -> Dict[str, int]:
        """Get ticker mention counts"""
        ticker_counts = {}
        for msg in self.messages:
            for ticker in msg['tickers']:
                ticker_counts[ticker] = ticker_counts.get(ticker, 0) + 1
        return ticker_counts
