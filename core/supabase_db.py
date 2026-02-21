"""
Supabase Database Integration
Stores: Telegram/Reddit/YouTube data + Risk analysis results
"""
import os
from dotenv import load_dotenv
load_dotenv()  # Load .env file

from supabase import create_client, Client
from datetime import datetime
from typing import Dict, List

class SupabaseDB:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()  # Ensure .env is loaded
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError(
                "Missing Supabase credentials. Add to .env:\n"
                "SUPABASE_URL=https://xxxxx.supabase.co\n"
                "SUPABASE_KEY=your_anon_key_here\n\n"
                "Get these from: Supabase Dashboard → Settings → API"
            )
        
        # Create client - supabase library handles headers automatically
        self.client: Client = create_client(url, key)
    
    # ==================== STORE RUMOR SOURCES ====================
    
    def store_telegram_message(self, message: Dict):
        """Store Telegram message (RUMOR SOURCE) - avoid duplicates"""
        # Check if message already exists
        existing = self.client.table('rumor_sources')\
            .select('id')\
            .eq('source', 'telegram')\
            .eq('channel', message.get('channel'))\
            .eq('text', message.get('text'))\
            .execute()
        
        if existing.data:
            return None  # Already exists, skip
        
        data = {
            'source': 'telegram',
            'channel': message.get('channel'),
            'text': message.get('text'),
            'tickers': message.get('tickers', []),
            'fraud_score': message.get('fraud_score', 0),
            'timestamp': message.get('date'),
            'created_at': datetime.now().isoformat()
        }
        return self.client.table('rumor_sources').insert(data).execute()
    
    def store_reddit_post(self, post: Dict):
        """Store Reddit post (RUMOR SOURCE) - avoid duplicates"""
        # Check if post already exists
        existing = self.client.table('rumor_sources')\
            .select('id')\
            .eq('source', 'reddit')\
            .eq('url', post.get('url'))\
            .execute()
        
        if existing.data:
            return None  # Already exists, skip
        
        data = {
            'source': 'reddit',
            'subreddit': post.get('subreddit'),
            'title': post.get('title'),
            'tickers': post.get('tickers', []),
            'hype_score': post.get('hype_score', 0),
            'upvotes': post.get('score', 0),
            'comments': post.get('comments', 0),
            'url': post.get('url'),
            'created_at': datetime.now().isoformat()
        }
        return self.client.table('rumor_sources').insert(data).execute()
    
    def store_youtube_video(self, video: Dict):
        """Store YouTube video (RUMOR SOURCE) - avoid duplicates"""
        # Clean title (remove special chars)
        title = video.get('title', '')
        title = title.encode('ascii', 'ignore').decode('ascii')[:200]  # ASCII only, max 200 chars
        
        if not title:
            return None
        
        # Check if video already exists
        existing = self.client.table('rumor_sources')\
            .select('id')\
            .eq('source', 'youtube')\
            .eq('title', title)\
            .execute()
        
        if existing.data:
            return None  # Already exists, skip
        
        data = {
            'source': 'youtube',
            'title': title,
            'channel': str(video.get('channel', 'Unknown'))[:100],
            'tickers': video.get('tickers', []),
            'hype_score': int(video.get('hype_score', 0)),
            'url': str(video.get('url', ''))[:500],
            'created_at': datetime.now().isoformat()
        }
        return self.client.table('rumor_sources').insert(data).execute()
    
    # ==================== STORE RISK ANALYSIS ====================
    
    def store_risk_analysis(self, ticker: str, analysis: Dict):
        """Store complete risk analysis for a ticker"""
        data = {
            'ticker': ticker,
            'risk_score': analysis.get('risk_assessment', {}).get('score', 0),
            'risk_level': analysis.get('risk_assessment', {}).get('level'),
            'color': analysis.get('risk_assessment', {}).get('color'),
            
            # Market data (VERIFICATION SOURCE)
            'price': analysis.get('market_data', {}).get('price'),
            'volume': analysis.get('market_data', {}).get('volume'),
            'z_score': analysis.get('market_data', {}).get('z_score'),
            
            # Social activity (RUMOR SOURCES)
            'telegram_mentions': analysis.get('social_activity', {}).get('telegram', {}).get('mention_count', 0),
            'reddit_mentions': analysis.get('social_activity', {}).get('reddit', {}).get('mention_count', 0),
            'youtube_mentions': analysis.get('social_activity', {}).get('youtube', {}).get('mention_count', 0),
            
            # Risk breakdown
            'social_hype_score': analysis.get('risk_breakdown', {}).get('social_hype_score', {}).get('value', 0),
            'volume_anomaly': analysis.get('risk_breakdown', {}).get('volume_anomaly', {}).get('value', 0),
            'bot_coordination': analysis.get('risk_breakdown', {}).get('bot_coordination', {}).get('value', 0),
            'sentiment_spike': analysis.get('risk_breakdown', {}).get('sentiment_spike', {}).get('value', 0),
            'lack_of_filings': analysis.get('risk_breakdown', {}).get('lack_of_filings', {}).get('value', 0),
            
            # Legitimacy
            'legitimacy_verdict': analysis.get('legitimacy', {}).get('verdict'),
            'legitimacy_score': analysis.get('legitimacy', {}).get('legitimacy_score', 0),
            
            # AI analysis
            'ai_analysis': analysis.get('ai_analysis'),
            
            'analyzed_at': datetime.now().isoformat()
        }
        
        # Check if recent analysis exists (within 5 minutes)
        from datetime import timedelta
        cutoff = (datetime.now() - timedelta(minutes=5)).isoformat()
        existing = self.client.table('risk_analysis')\
            .select('id')\
            .eq('ticker', ticker)\
            .gte('analyzed_at', cutoff)\
            .execute()
        
        if existing.data:
            return None  # Recent analysis exists, skip
        
        return self.client.table('risk_analysis').insert(data).execute()
    
    # ==================== QUERY DATA ====================
    
    def get_high_risk_tickers(self, min_risk: int = 70):
        """Get tickers with high risk score"""
        return self.client.table('risk_analysis')\
            .select('*')\
            .gte('risk_score', min_risk)\
            .order('risk_score', desc=True)\
            .execute()
    
    def get_ticker_history(self, ticker: str, days: int = 7):
        """Get historical analysis for a ticker"""
        from datetime import timedelta
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        return self.client.table('risk_analysis')\
            .select('*')\
            .eq('ticker', ticker)\
            .gte('analyzed_at', cutoff)\
            .order('analyzed_at', desc=True)\
            .execute()
    
    def get_rumor_sources_by_ticker(self, ticker: str):
        """Get all rumor sources mentioning a ticker"""
        return self.client.table('rumor_sources')\
            .select('*')\
            .contains('tickers', [ticker])\
            .order('created_at', desc=True)\
            .limit(50)\
            .execute()
