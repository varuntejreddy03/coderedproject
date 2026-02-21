import requests
from bs4 import BeautifulSoup
import logging
from typing import List
from datetime import datetime
import json
import re

logger = logging.getLogger(__name__)

# Target stocks for demo
TARGET_STOCKS = {'YESBANK', 'TCS', 'RELIANCE', 'INFY'}


class RedditScraper:
    def __init__(self):
        self.subreddits = ['IndianStockMarket', 'IndianStreetBets', 'DalalStreetTalks']
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def contains_target_stock(self, text: str) -> bool:
        """Check if text mentions any target stock"""
        text_upper = text.upper()
        return any(stock in text_upper for stock in TARGET_STOCKS)
        
    def fetch_posts(self, limit: int = 100) -> List[dict]:
        """Fetch posts from Indian stock market subreddits (no API key needed)"""
        messages = []
        
        for sub in self.subreddits:
            try:
                # Use Reddit's JSON endpoint (public, no auth needed)
                url = f'https://www.reddit.com/r/{sub}/new.json?limit={min(limit, 100)}'
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for post in data['data']['children']:
                        post_data = post['data']
                        text = f"{post_data['title']} {post_data.get('selftext', '')}"
                        
                        # Include all posts, not just ones with target stocks
                        messages.append({
                            'id': post_data['id'],
                            'channel': f'r/{sub}',
                            'text': text,
                            'date': datetime.fromtimestamp(post_data['created_utc']).isoformat(),
                            'url': f"https://reddit.com{post_data['permalink']}",
                            'score': post_data['score'],
                            'author': post_data['author']
                        })
                else:
                    logger.warning(f"Reddit returned status {response.status_code} for r/{sub}")
                    
            except Exception as e:
                logger.error(f"Error fetching from r/{sub}: {e}")
        
        return messages
