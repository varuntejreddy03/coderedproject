"""
🔴 RUMOR SOURCE: Telegram Scraper (UNTRUSTED)
Monitors pump & dump groups for fraud detection
Data from this source must be validated against yfinance/NSE
"""
import sys
import io

# Fix unicode print errors
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import asyncio
import re
import os
import json
from telethon import TelegramClient, events
from datetime import datetime
from typing import List, Set

# Load NSE stocks dynamically
def load_nse_stocks() -> Set[str]:
    """Load NSE stock list from data folder"""
    paths = [
        'data/nse_stocks.json',
        '../data/nse_stocks.json',
        os.path.join(os.path.dirname(__file__), '..', 'data', 'nse_stocks.json')
    ]
    
    for path in paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    stocks = set(json.load(f))
                    print(f"✅ Loaded {len(stocks)} NSE stocks from {path}")
                    return stocks
            except:
                continue
    
    # Fallback to common stocks
    print("⚠️ Using fallback stock list")
    return {'YESBANK', 'TCS', 'RELIANCE', 'INFY', 'SBIN', 'HDFCBANK', 'ICICIBANK'}

TARGET_STOCKS = load_nse_stocks()

# Fraud keywords (indicators of pump & dump schemes on RUMOR SOURCES)
FRAUD_KEYWORDS = [
    'pakka', 'upper circuit', 'sure shot', 'guaranteed', '100%',
    'multibagger', 'jackpot', 'operator', 'premium tip', 'target'
]

class SimpleTelegramScraper:
    def __init__(self, api_id: int, api_hash: str, channels: List[str], use_test_dc: bool = False):
        self.api_id = api_id
        self.api_hash = api_hash
        self.channels = channels
        
        # Use sequential_updates to fix time sync issues
        self.client = TelegramClient(
            'pumpwatch_session',
            api_id,
            api_hash,
            sequential_updates=True
        )
        
        self.messages = []
        self.new_message_callback = None
        self.is_listening = False
    
    def extract_tickers(self, text: str) -> List[str]:
        """🔴 Extract stock tickers from RUMOR SOURCE message (UNTRUSTED)"""
        text_upper = text.upper()
        found_tickers = []
        
        # Extract all potential tickers (2-15 chars, all caps)
        potential = re.findall(r'\b[A-Z]{2,15}\b', text_upper)
        
        # Filter to only valid NSE stocks
        for ticker in potential:
            if ticker in TARGET_STOCKS:
                found_tickers.append(ticker)
        
        return found_tickers
    
    def detect_fraud(self, text: str) -> int:
        """🔴 Count fraud keywords in RUMOR SOURCE message"""
        text_lower = text.lower()
        return sum(1 for kw in FRAUD_KEYWORDS if kw in text_lower)
    
    async def connect(self):
        """Connect to Telegram"""
        await self.client.start()
        print("✅ Connected to Telegram")
    
    async def fetch_messages(self, limit: int = 50):
        """Fetch messages from all channels"""
        all_messages = []
        
        for channel in self.channels:
            try:
                entity = await self.client.get_entity(channel)
                msgs = await self.client.get_messages(entity, limit=limit)
                
                for m in msgs:
                    if m.message:
                        tickers = self.extract_tickers(m.message)
                        fraud_score = self.detect_fraud(m.message)
                        
                        # Store message
                        all_messages.append({
                            'id': m.id,
                            'channel': channel,
                            'text': m.message,
                            'date': m.date.isoformat() if m.date else None,
                            'tickers': tickers,
                            'fraud_score': fraud_score
                        })
                
                print(f"✅ Fetched {len(msgs)} messages from {channel}")
            except Exception as e:
                print(f"❌ Error fetching from {channel}: {e}")
        
        self.messages = all_messages
        return all_messages
    
    async def disconnect(self):
        """Disconnect from Telegram"""
        await self.client.disconnect()
        print("✅ Disconnected from Telegram")
    
    def get_all_tickers(self):
        """Get ticker mention counts"""
        ticker_counts = {}
        for msg in self.messages:
            for ticker in msg['tickers']:
                ticker_counts[ticker] = ticker_counts.get(ticker, 0) + 1
        return ticker_counts
    
    def get_fraud_alerts(self, min_risk_score=2):
        """Get high-risk messages"""
        return [m for m in self.messages if m['fraud_score'] >= min_risk_score]
    
    async def get_all_joined_channels(self):
        """Get all channels/groups user has joined"""
        dialogs = await self.client.get_dialogs()
        channels = []
        
        for dialog in dialogs:
            if dialog.is_channel or dialog.is_group:
                channels.append({
                    'id': dialog.id,
                    'name': dialog.name,
                    'username': dialog.entity.username if hasattr(dialog.entity, 'username') else None,
                    'type': 'channel' if dialog.is_channel else 'group'
                })
        
        return channels
    
    async def listen_all_joined(self, callback=None):
        """Listen to ALL joined channels/groups (not specific ones)"""
        self.new_message_callback = callback
        self.is_listening = True
        
        # Get all joined channels
        channels = await self.get_all_joined_channels()
        print(f"\u2705 Found {len(channels)} joined channels/groups")
        for ch in channels[:10]:  # Show first 10
            try:
                print(f"   - {ch['name']} (@{ch['username'] or 'private'})")
            except:
                print(f"   - [channel] (@{ch['username'] or 'private'})")
        
        # Listen to ALL channels (no filter)
        @self.client.on(events.NewMessage())
        async def handler(event):
            if not self.is_listening:
                return
            
            # Only process channel/group messages
            if not (event.is_channel or event.is_group):
                return
            
            text = event.message.message
            if text:
                tickers = self.extract_tickers(text)
                
                # Only store if has stock tickers
                if not tickers:
                    return
                
                fraud_score = self.detect_fraud(text)
                
                message = {
                    'id': event.message.id,
                    'channel': str(event.chat.username or event.chat.title or event.chat_id),
                    'text': text,
                    'date': event.message.date.isoformat() if event.message.date else None,
                    'tickers': tickers,
                    'fraud_score': fraud_score
                }
                
                self.messages.append(message)
                
                # Safe print (handle unicode)
                try:
                    print(f"NEW from {message['channel']}: {text[:50]}... (Tickers: {tickers})")
                except:
                    print(f"NEW from {message['channel']}: [message] (Tickers: {tickers})")
                
                if self.new_message_callback:
                    await self.new_message_callback(message)
        
        print(f"\u2705 Listening to ALL joined channels (real-time)")
        await self.client.run_until_disconnected()
    
    def stop_listening(self):
        """Stop real-time listener"""
        self.is_listening = False
