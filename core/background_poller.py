"""
Background Poller - Reddit & YouTube (every 60 seconds)
"""
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BackgroundPoller:
    def __init__(self, supabase_db=None):
        self.supabase_db = supabase_db
        self.is_running = False
        self.poll_interval = 60  # seconds
    
    async def start(self):
        """Start background polling"""
        self.is_running = True
        logger.info(f"\u2705 Background poller started (every {self.poll_interval}s)")
        
        while self.is_running:
            try:
                await self.poll_reddit()
                await self.poll_youtube()
            except Exception as e:
                logger.error(f"Polling error: {e}")
            
            await asyncio.sleep(self.poll_interval)
    
    async def poll_reddit(self):
        """Poll Reddit every 60 seconds"""
        try:
            from scrapers.reddit_hype_analyzer import RedditHypeAnalyzer
            
            analyzer = RedditHypeAnalyzer()
            result = analyzer.analyze_reddit_hype()
            
            if self.supabase_db:
                stored = 0
                for ticker, data in list(result['top_hyped_stocks'].items())[:5]:
                    for post in data['posts'][:2]:
                        try:
                            res = self.supabase_db.store_reddit_post(post)
                            if res:
                                stored += 1
                        except:
                            pass
                
                if stored > 0:
                    logger.info(f"\ud83d\udd34 POLL: Stored {stored} new Reddit posts")
        except Exception as e:
            logger.error(f"Reddit poll error: {e}")
    
    async def poll_youtube(self):
        """Poll YouTube every 60 seconds"""
        try:
            from scrapers.youtube_scraper import YouTubeScraperNoAPI
            
            scraper = YouTubeScraperNoAPI()
            result = scraper.analyze_youtube_hype()
            
            if self.supabase_db:
                stored = 0
                for ticker, data in list(result['top_hyped_stocks'].items())[:5]:
                    for video_title in data['videos'][:1]:
                        try:
                            video_data = {
                                'title': video_title,
                                'channel': 'Unknown',
                                'tickers': [ticker],
                                'hype_score': data['avg_hype_score'],
                                'url': f'https://youtube.com/results?search_query={ticker}'
                            }
                            res = self.supabase_db.store_youtube_video(video_data)
                            if res:
                                stored += 1
                        except:
                            pass
                
                if stored > 0:
                    logger.info(f"\ud83d\udd34 POLL: Stored {stored} new YouTube videos")
        except Exception as e:
            logger.error(f"YouTube poll error: {e}")
    
    def stop(self):
        """Stop background polling"""
        self.is_running = False
        logger.info("\u23f9\ufe0f Background poller stopped")
