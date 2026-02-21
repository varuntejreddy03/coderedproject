"""
🔴 RUMOR SOURCE: YouTube Comment Scraper (UNTRUSTED)
Scrapes comments from stock tip videos for pump & dump detection
Data from this source must be validated against yfinance/NSE
"""
import requests
import re
from typing import List, Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Load NSE stocks
try:
    import os
    import json
    paths = [
        'data/nse_stocks.json',
        '../data/nse_stocks.json',
        os.path.join(os.path.dirname(__file__), '..', 'data', 'nse_stocks.json')
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                INDIAN_STOCKS = set(json.load(f))
                break
    else:
        raise FileNotFoundError
except:
    INDIAN_STOCKS = {
        'RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK', 'SBIN', 'YESBANK',
        'SUZLON', 'VEDL', 'SAIL', 'TATAMOTORS', 'TATASTEEL', 'ADANIPOWER'
    }

# YouTube search keywords for pump & dump videos
SEARCH_KEYWORDS = [
    'penny stock india today',
    'multibagger stock 2024', 
    'upper circuit stock today',
    'best stock to buy now india',
    'intraday stock tip today',
    'share market jackpot stock',
    'guaranteed profit stock',
    'stock recommendation today india',
    'hidden gem stock india',
    'operator stock india'
]

# Hype keywords
HYPE_KEYWORDS = [
    'pakka', 'guaranteed', 'sure shot', '100%', 'multibagger', 'upper circuit',
    'lower circuit', 'target', 'rocket', 'moon', 'jackpot', 'operator',
    'insider', 'premium tip', 'confirmed', 'zaroor', 'bilkul'
]


class YouTubeScraper:
    """🔴 Scrapes YouTube comments from stock tip videos (RUMOR SOURCE)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    def extract_tickers(self, text: str) -> List[str]:
        """🔴 Extract stock tickers from RUMOR SOURCE text"""
        text_upper = text.upper()
        found = []
        for ticker in INDIAN_STOCKS:
            if re.search(r'\b' + ticker + r'\b', text_upper):
                found.append(ticker)
        return list(set(found))
    
    def detect_hype(self, text: str) -> int:
        """🔴 Count hype keywords in text"""
        text_lower = text.lower()
        return sum(1 for kw in HYPE_KEYWORDS if kw in text_lower)
    
    def search_videos(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search YouTube videos by keyword"""
        if not self.api_key:
            logger.warning("No YouTube API key provided")
            return []
        
        try:
            url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'key': self.api_key,
                'relevanceLanguage': 'hi',
                'regionCode': 'IN'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                videos = []
                for item in data.get('items', []):
                    videos.append({
                        'video_id': item['id']['videoId'],
                        'title': item['snippet']['title'],
                        'channel': item['snippet']['channelTitle'],
                        'published_at': item['snippet']['publishedAt']
                    })
                return videos
            else:
                logger.error(f"YouTube API error: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error searching videos: {e}")
            return []
    
    def get_video_comments(self, video_id: str, max_results: int = 100) -> List[Dict]:
        """Get comments from a video"""
        if not self.api_key:
            return []
        
        try:
            url = f"{self.base_url}/commentThreads"
            params = {
                'part': 'snippet',
                'videoId': video_id,
                'maxResults': max_results,
                'key': self.api_key,
                'textFormat': 'plainText'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                comments = []
                for item in data.get('items', []):
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'text': comment['textDisplay'],
                        'author': comment['authorDisplayName'],
                        'likes': comment['likeCount'],
                        'published_at': comment['publishedAt']
                    })
                return comments
            return []
        except Exception as e:
            logger.error(f"Error fetching comments: {e}")
            return []
    
    def analyze_youtube_hype(self, max_videos_per_keyword: int = 5) -> Dict:
        """
        🔴 Analyze YouTube RUMOR SOURCE for stock hype (UNTRUSTED)
        Returns: {ticker: {mentions, hype_score, comments, videos}}
        """
        ticker_data = {}
        all_comments = []
        
        for keyword in SEARCH_KEYWORDS:
            videos = self.search_videos(keyword, max_videos_per_keyword)
            
            for video in videos:
                comments = self.get_video_comments(video['video_id'])
                
                for comment in comments:
                    tickers = self.extract_tickers(comment['text'])
                    hype_score = self.detect_hype(comment['text'])
                    
                    if tickers:
                        comment_info = {
                            'text': comment['text'][:200],
                            'video_title': video['title'],
                            'channel': video['channel'],
                            'likes': comment['likes'],
                            'tickers': tickers,
                            'hype_score': hype_score
                        }
                        all_comments.append(comment_info)
                        
                        for ticker in tickers:
                            if ticker not in ticker_data:
                                ticker_data[ticker] = {
                                    'mentions': 0,
                                    'total_hype_score': 0,
                                    'total_likes': 0,
                                    'comments': [],
                                    'videos': set()
                                }
                            
                            ticker_data[ticker]['mentions'] += 1
                            ticker_data[ticker]['total_hype_score'] += hype_score
                            ticker_data[ticker]['total_likes'] += comment['likes']
                            ticker_data[ticker]['comments'].append(comment_info)
                            ticker_data[ticker]['videos'].add(video['title'])
        
        # Calculate hype intensity
        for ticker, data in ticker_data.items():
            avg_hype = data['total_hype_score'] / data['mentions'] if data['mentions'] > 0 else 0
            engagement = data['total_likes'] / data['mentions'] if data['mentions'] > 0 else 0
            
            data['hype_intensity'] = round(
                (data['mentions'] * 10) + (avg_hype * 5) + (engagement / 5),
                2
            )
            data['avg_hype_score'] = round(avg_hype, 2)
            data['avg_engagement'] = round(engagement, 2)
            data['videos'] = list(data['videos'])
        
        sorted_tickers = dict(
            sorted(ticker_data.items(), key=lambda x: x[1]['hype_intensity'], reverse=True)
        )
        
        return {
            'top_hyped_stocks': sorted_tickers,
            'total_comments_analyzed': len(all_comments),
            'total_tickers_found': len(ticker_data)
        }
    
    def get_top_hyped(self, limit: int = 10) -> List[Dict]:
        """Get top N most hyped stocks from YouTube"""
        analysis = self.analyze_youtube_hype()
        top_stocks = []
        
        for ticker, data in list(analysis['top_hyped_stocks'].items())[:limit]:
            top_stocks.append({
                'ticker': ticker,
                'mentions': data['mentions'],
                'hype_intensity': data['hype_intensity'],
                'avg_hype_score': data['avg_hype_score'],
                'total_likes': data['total_likes'],
                'video_count': len(data['videos']),
                'sample_comments': data['comments'][:3]
            })
        
        return top_stocks


# Fallback: Scrape without API (limited functionality)
class YouTubeScraperNoAPI:
    """🔴 YouTube scraper without API - uses public search (RUMOR SOURCE)"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def extract_tickers(self, text: str) -> List[str]:
        """🔴 Extract stock tickers from RUMOR SOURCE text"""
        text_upper = text.upper()
        found = []
        for ticker in INDIAN_STOCKS:
            if re.search(r'\b' + ticker + r'\b', text_upper):
                found.append(ticker)
        return list(set(found))
    
    def detect_hype(self, text: str) -> int:
        """🔴 Count hype keywords"""
        text_lower = text.lower()
        return sum(1 for kw in HYPE_KEYWORDS if kw in text_lower)
    
    def search_video_titles(self, query: str) -> List[Dict]:
        """Search YouTube video titles (no API needed)"""
        try:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Extract video titles from HTML
                titles = re.findall(r'"title":{"runs":\[{"text":"([^"]+)"}', response.text)
                videos = []
                for title in titles[:20]:
                    tickers = self.extract_tickers(title)
                    hype_score = self.detect_hype(title)
                    if tickers:
                        videos.append({
                            'title': title,
                            'tickers': tickers,
                            'hype_score': hype_score
                        })
                return videos
            return []
        except Exception as e:
            logger.error(f"Error scraping YouTube: {e}")
            return []
    
    def analyze_youtube_hype(self) -> Dict:
        """🔴 Analyze YouTube video titles for stock hype (UNTRUSTED)"""
        ticker_data = {}
        
        for keyword in SEARCH_KEYWORDS[:3]:  # Limit to avoid rate limiting
            videos = self.search_video_titles(keyword)
            
            for video in videos:
                for ticker in video['tickers']:
                    if ticker not in ticker_data:
                        ticker_data[ticker] = {
                            'mentions': 0,
                            'total_hype_score': 0,
                            'videos': []
                        }
                    
                    ticker_data[ticker]['mentions'] += 1
                    ticker_data[ticker]['total_hype_score'] += video['hype_score']
                    ticker_data[ticker]['videos'].append(video['title'])
        
        # Calculate hype intensity
        for ticker, data in ticker_data.items():
            avg_hype = data['total_hype_score'] / data['mentions'] if data['mentions'] > 0 else 0
            data['hype_intensity'] = round((data['mentions'] * 10) + (avg_hype * 5), 2)
            data['avg_hype_score'] = round(avg_hype, 2)
        
        sorted_tickers = dict(
            sorted(ticker_data.items(), key=lambda x: x[1]['hype_intensity'], reverse=True)
        )
        
        return {
            'top_hyped_stocks': sorted_tickers,
            'total_tickers_found': len(ticker_data)
        }
