"""
Job Queue System - Async Queue (No Redis needed)
Ingestion → Queue → Processing → DB → API
"""
import asyncio
from typing import Dict, Callable
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class JobQueue:
    """Simple async job queue (in-memory, no Redis needed)"""
    
    def __init__(self, supabase_db=None):
        self.queue = asyncio.Queue(maxsize=1000)
        self.supabase_db = supabase_db
        self.is_running = False
        self.processed_count = 0
        self.failed_count = 0
    
    async def add_job(self, job_type: str, data: Dict):
        """Add job to queue (non-blocking)"""
        try:
            await self.queue.put({
                'type': job_type,
                'data': data,
                'timestamp': datetime.now().isoformat()
            })
        except asyncio.QueueFull:
            logger.warning(f"Queue full, dropping job: {job_type}")
    
    async def start_worker(self):
        """Start background worker to process jobs"""
        self.is_running = True
        logger.info("✅ Job queue worker started")
        
        while self.is_running:
            try:
                # Get job from queue (non-blocking with timeout)
                job = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                await self.process_job(job)
                self.queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Worker error: {e}")
    
    async def process_job(self, job: Dict):
        """Process a job based on type"""
        job_type = job['type']
        data = job['data']
        
        try:
            if job_type == 'telegram_message':
                await self.process_telegram(data)
            elif job_type == 'reddit_post':
                await self.process_reddit(data)
            elif job_type == 'youtube_video':
                await self.process_youtube(data)
            elif job_type == 'risk_analysis':
                await self.process_risk_analysis(data)
            
            self.processed_count += 1
            
        except Exception as e:
            self.failed_count += 1
            logger.error(f"Job processing failed ({job_type}): {e}")
    
    async def process_telegram(self, message: Dict):
        """Process Telegram message"""
        if self.supabase_db:
            result = self.supabase_db.store_telegram_message(message)
            if result:
                logger.info(f"📥 Stored Telegram: {message.get('channel')}")
    
    async def process_reddit(self, post: Dict):
        """Process Reddit post"""
        if self.supabase_db:
            result = self.supabase_db.store_reddit_post(post)
            if result:
                logger.info(f"📥 Stored Reddit: {post.get('subreddit')}")
    
    async def process_youtube(self, video: Dict):
        """Process YouTube video"""
        if self.supabase_db:
            result = self.supabase_db.store_youtube_video(video)
            if result:
                logger.info(f"📥 Stored YouTube: {video.get('title', '')[:30]}...")
    
    async def process_risk_analysis(self, data: Dict):
        """Process risk analysis"""
        if self.supabase_db:
            ticker = data.get('ticker')
            analysis = data.get('analysis')
            result = self.supabase_db.store_risk_analysis(ticker, analysis)
            if result:
                logger.info(f"📊 Stored analysis: {ticker}")
    
    def get_stats(self) -> Dict:
        """Get queue statistics"""
        return {
            'queue_size': self.queue.qsize(),
            'processed': self.processed_count,
            'failed': self.failed_count,
            'is_running': self.is_running
        }
    
    def stop(self):
        """Stop worker"""
        self.is_running = False
        logger.info("⏹️ Job queue worker stopped")
