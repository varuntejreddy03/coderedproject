"""
🔴 RUMOR SOURCE: Reddit Hype Analyzer (UNTRUSTED)
Monitors Indian stock subreddits for speculation and pump signals
Data from this source must be validated against yfinance/NSE
"""
import requests
import re
from collections import Counter
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

# Try to load live NSE stocks, fallback to hardcoded list
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from scrapers.fetch_nse_stocks import get_stocks_with_cache
    INDIAN_STOCKS = get_stocks_with_cache(force_refresh=False)
    logger.info(f"✅ Loaded {len(INDIAN_STOCKS)} live NSE stocks")
except Exception as e:
    logger.warning(f"Failed to load live stocks, using hardcoded list: {e}")
    # Fallback to hardcoded list
    INDIAN_STOCKS = {
    # Nifty 50
    'RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK', 'SBIN', 'BHARTIARTL',
    'ITC', 'KOTAKBANK', 'LT', 'AXISBANK', 'ASIANPAINT', 'MARUTI', 'TITAN',
    'SUNPHARMA', 'ULTRACEMCO', 'NESTLEIND', 'BAJFINANCE', 'WIPRO', 'TECHM',
    'TATAMOTORS', 'TATASTEEL', 'POWERGRID', 'NTPC', 'ONGC', 'COALINDIA',
    'ADANIENT', 'ADANIPORTS', 'HINDALCO', 'JSWSTEEL', 'INDUSINDBK',
    'HCLTECH', 'BAJAJFINSV', 'BRITANNIA', 'DIVISLAB', 'DRREDDY', 'EICHERMOT',
    'GRASIM', 'HEROMOTOCO', 'HINDUNILVR', 'CIPLA', 'SHREECEM', 'TATACONSUM',
    'APOLLOHOSP', 'BPCL', 'ADANIGREEN', 'SBILIFE', 'HDFCLIFE',
    
    # Mid/Small Cap Popular
    'YESBANK', 'SUZLON', 'VEDL', 'SAIL', 'RPOWER', 'IDEA', 'ZEEL', 'IRCTC',
    'PAYTM', 'NYKAA', 'ZOMATO', 'POLICYBZR', 'DMART', 'TATAPOWER', 'ADANIPOWER',
    'JINDALSTEL', 'NMDC', 'RECLTD', 'PFC', 'IRFC', 'RVNL', 'RAILTEL',
    'MOTHERSON', 'MPHASIS', 'PERSISTENT', 'COFORGE', 'LTTS', 'LTIM',
    'TATAELXSI', 'MINDTREE', 'OFSS', 'MFSL', 'CDSL', 'CAMS',
    
    # Penny Stocks (High Risk)
    'RCOM', 'JETAIRWAYS', 'PCJEWELLER', 'DHFL', 'RELCAPITAL', 'RELINFRA',
    'REPOWER', 'JPASSOCIAT', 'UNITECH', 'GTLINFRA', 'RNAVAL', 'WELCORP',
    'WELSPUNIND', 'GMRINFRA', 'ADANIGAS', 'ADANITRANS', 'IDFCFIRSTB',
    
    # Banking & Finance
    'BANKBARODA', 'PNB', 'CANBK', 'UNIONBANK', 'IDFCBANK', 'FEDERALBNK',
    'BANDHANBNK', 'RBLBANK', 'AUBANK', 'CHOLAFIN', 'M&MFIN', 'LICHSGFIN',
    'SRTRANSFIN', 'BAJAJHLDNG', 'ICICIGI', 'ICICIPRU', 'SBICARD',
    
    # IT & Tech
    'NAUKRI', 'ZOMATO', 'PAYTM', 'POLICYBZR', 'HAPPSTMNDS', 'ROUTE',
    'LATENTVIEW', 'MASTEK', 'CYIENT', 'KPITTECH', 'SONATSOFTW',
    
    # Auto
    'BAJAJ-AUTO', 'M&M', 'TVSMOTOR', 'ESCORTS', 'ASHOKLEY', 'BHARATFORG',
    'EXIDEIND', 'AMBUJACEM', 'BOSCHLTD', 'MRF', 'APOLLOTYRE',
    
    # Pharma
    'LUPIN', 'BIOCON', 'TORNTPHARM', 'ALKEM', 'AUROPHARMA', 'GLENMARK',
    'IPCALAB', 'LALPATHLAB', 'METROPOLIS', 'THYROCARE', 'DRLABS',
    
    # FMCG & Retail
    'DABUR', 'GODREJCP', 'MARICO', 'COLPAL', 'PGHH', 'VBL', 'TATACONSUM',
    'JUBLFOOD', 'WESTLIFE', 'SAPPHIRE', 'AVENUE', 'SHOPERSTOP',
    
    # Energy & Power
    'TORNTPOWER', 'CESC', 'NHPC', 'SJVN', 'TATAPOWER', 'ADANIGREEN',
    'ADANITRANS', 'ADANIPOWER', 'JSWENERGY', 'RELINFRA',
    
    # Telecom
    'BHARTIARTL', 'IDEA', 'TATACOMM', 'ROUTE', 'GTLINFRA',
    
    # Metals & Mining
    'HINDZINC', 'VEDL', 'NATIONALUM', 'JINDALSTEL', 'JSWSTEEL', 'TATASTEEL',
    'SAIL', 'NMDC', 'COALINDIA', 'MOIL', 'HINDALCO',
    
    # Infrastructure
    'IRCON', 'NBCC', 'NCC', 'GMRINFRA', 'IRBINVIT', 'INDHOTEL', 'LEMONTREE'
}

# Hype & Fraud keywords - Comprehensive list
HYPE_KEYWORDS = [
    # Pump signals
    'moon', 'rocket', 'squeeze', 'pump', 'breakout', 'explosion', 'parabolic',
    'to the moon', 'mooning', 'moonshot', 'skyrocket', 'blast off',
    
    # FOMO triggers
    'yolo', 'all in', 'buy the dip', 'btd', 'diamond hands', 'hold the line',
    'dont miss', "don't miss", 'last chance', 'limited time', 'urgent', 'now or never',
    
    # Guaranteed returns (fraud)
    'guaranteed', 'sure shot', 'confirmed', '100%', 'risk free', 'no risk',
    'guaranteed profit', 'guaranteed returns', 'pakka', 'sure thing',
    
    # Multibagger signals
    'multibagger', '10x', '100x', '1000x', 'bagger', 'jackpot', 'lottery',
    'life changing', 'retire early', 'financial freedom',
    
    # Insider/Operator signals (fraud)
    'insider', 'insider info', 'insider tip', 'operator', 'operator game',
    'big player', 'smart money', 'institutional buying', 'bulk deal',
    
    # Circuit breakers
    'upper circuit', 'lower circuit', 'circuit', 'locked', 'halt',
    
    # Target/Price action
    'target', 'price target', 'tp', 'book profit', 'profit booking',
    'stop loss', 'sl', 'entry', 'exit', 'breakout', 'breakdown',
    
    # Trading calls
    'calls', 'puts', 'options', 'btst', 'stbt', 'intraday', 'swing',
    'positional', 'delivery', 'futures', 'f&o',
    
    # Premium/Paid groups (fraud)
    'premium', 'paid group', 'vip', 'exclusive', 'members only',
    'join now', 'limited seats', 'subscription', 'premium tip',
    
    # Bullish sentiment
    'bullish', 'bull run', 'bull market', 'strong buy', 'accumulate',
    'buy', 'long', 'going up', 'uptrend', 'rally',
    
    # Bearish sentiment
    'bearish', 'bear market', 'crash', 'dump', 'sell', 'short',
    'going down', 'downtrend', 'correction', 'panic',
    
    # Technical analysis
    'golden cross', 'death cross', 'support', 'resistance', 'fibonacci',
    'rsi', 'macd', 'moving average', 'volume spike', 'breakout',
    
    # Fundamental triggers
    'earnings', 'results', 'dividend', 'bonus', 'split', 'buyback',
    'merger', 'acquisition', 'ipo', 'listing',
    
    # Hinglish (Indian)
    'pakka', 'zaroor', 'bilkul', 'ekdum', 'jaldi', 'abhi', 'karo',
    'lena', 'bechna', 'khareedna', 'paisa', 'lakh', 'crore'
]

class RedditHypeAnalyzer:
    def __init__(self):
        # ✅ FAIR: Search Reddit by keywords, not hardcoded subreddits
        # We search ALL of Reddit for pump/dump keywords
        self.search_keywords = [
            'penny stock india',
            'multibagger stock',
            'upper circuit stock',
            'guaranteed profit stock',
            'pakka stock tip',
            'operator stock india',
            'jackpot stock india'
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def extract_tickers(self, text: str) -> List[str]:
        """🔴 Extract Indian stock tickers from RUMOR SOURCE (UNTRUSTED)"""
        text_upper = text.upper()
        found = []
        for ticker in INDIAN_STOCKS:
            if re.search(r'\b' + ticker + r'\b', text_upper):
                found.append(ticker)
        return found
    
    def detect_hype(self, text: str) -> int:
        """🔴 Count hype keywords in RUMOR SOURCE text"""
        text_lower = text.lower()
        return sum(1 for keyword in HYPE_KEYWORDS if keyword in text_lower)
    
    def analyze_reddit_hype(self, limit: int = 500) -> Dict:
        """
        🔴 Analyze Reddit RUMOR SOURCE to find most hyped stocks (UNTRUSTED)
        ✅ FAIR: Search by keywords across ALL Reddit, not specific subreddits
        Returns: {ticker: {mentions, hype_score, posts}}
        Must be validated against yfinance/NSE data
        """
        ticker_data = {}
        all_posts = []
        
        # ✅ Search ALL of Reddit by keywords
        for keyword in self.search_keywords:
            try:
                url = f'https://www.reddit.com/search.json?q={keyword.replace(" ", "+")}&limit=50&sort=new'
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for post in data['data']['children']:
                        post_data = post['data']
                        title = post_data['title']
                        selftext = post_data.get('selftext', '')
                        full_text = f"{title} {selftext}"
                        
                        # Extract tickers
                        tickers = self.extract_tickers(full_text)
                        hype_score = self.detect_hype(full_text)
                        
                        if tickers:
                            post_info = {
                                'title': title,
                                'subreddit': post_data['subreddit'],
                                'score': post_data['score'],
                                'comments': post_data['num_comments'],
                                'url': f"https://reddit.com{post_data['permalink']}",
                                'tickers': tickers,
                                'hype_score': hype_score
                            }
                            all_posts.append(post_info)
                            
                            # Aggregate by ticker
                            for ticker in tickers:
                                if ticker not in ticker_data:
                                    ticker_data[ticker] = {
                                        'mentions': 0,
                                        'total_hype_score': 0,
                                        'total_upvotes': 0,
                                        'total_comments': 0,
                                        'posts': []
                                    }
                                
                                ticker_data[ticker]['mentions'] += 1
                                ticker_data[ticker]['total_hype_score'] += hype_score
                                ticker_data[ticker]['total_upvotes'] += post_data['score']
                                ticker_data[ticker]['total_comments'] += post_data['num_comments']
                                ticker_data[ticker]['posts'].append(post_info)
                
                logger.info(f"✅ Searched Reddit for: {keyword}")
            except Exception as e:
                logger.error(f"Error searching Reddit for '{keyword}': {e}")
        
        # Calculate final hype intensity for each ticker
        for ticker, data in ticker_data.items():
            # Hype intensity = mentions + avg_hype_score + engagement
            avg_hype = data['total_hype_score'] / data['mentions'] if data['mentions'] > 0 else 0
            engagement = (data['total_upvotes'] + data['total_comments']) / data['mentions']
            
            data['hype_intensity'] = round(
                (data['mentions'] * 10) + (avg_hype * 5) + (engagement / 10),
                2
            )
            data['avg_hype_score'] = round(avg_hype, 2)
            data['avg_engagement'] = round(engagement, 2)
        
        # Sort by hype intensity
        sorted_tickers = dict(
            sorted(ticker_data.items(), key=lambda x: x[1]['hype_intensity'], reverse=True)
        )
        
        return {
            'top_hyped_stocks': sorted_tickers,
            'total_posts_analyzed': len(all_posts),
            'total_tickers_found': len(ticker_data)
        }
    
    def get_top_hyped(self, limit: int = 10) -> List[Dict]:
        """Get top N most hyped stocks"""
        analysis = self.analyze_reddit_hype()
        top_stocks = []
        
        for ticker, data in list(analysis['top_hyped_stocks'].items())[:limit]:
            top_stocks.append({
                'ticker': ticker,
                'mentions': data['mentions'],
                'hype_intensity': data['hype_intensity'],
                'avg_hype_score': data['avg_hype_score'],
                'total_upvotes': data['total_upvotes'],
                'total_comments': data['total_comments'],
                'sample_posts': data['posts'][:3]  # Top 3 posts
            })
        
        return top_stocks


if __name__ == "__main__":
    analyzer = RedditHypeAnalyzer()
    result = analyzer.analyze_reddit_hype()
    
    print("\n🔥 TOP HYPED STOCKS ON REDDIT (Keyword Search):")
    print("✅ FAIR: Searched ALL Reddit by keywords, not specific subreddits")
    for ticker, data in list(result['top_hyped_stocks'].items())[:10]:
        print(f"\n{ticker}:")
        print(f"  Mentions: {data['mentions']}")
        print(f"  Hype Intensity: {data['hype_intensity']}")
        print(f"  Avg Hype Score: {data['avg_hype_score']}")
        print(f"  Engagement: {data['avg_engagement']}")
