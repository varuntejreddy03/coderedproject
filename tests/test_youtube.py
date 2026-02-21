"""
Test YouTube Scraper - Get all videos uploaded in last 1 day
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scrapers.youtube_scraper import YouTubeScraperNoAPI
from datetime import datetime, timedelta
import requests
import re

# 🔴 RUMOR SOURCE: Search YouTube by KEYWORDS, not specific channels
# This is fair - we analyze ANY video with pump/dump keywords
# We don't target specific channels - we search by content type

# Search keywords that indicate potential pump & dump content
SEARCH_KEYWORDS = [
    'penny stock india today',
    'multibagger stock 2024', 
    'upper circuit stock today',
    'guaranteed profit stock india',
    'best stock to buy now india',
    'intraday stock tip today',
    'share market jackpot stock',
    'hidden gem stock india',
    'stock recommendation today india',
    'operator stock india',
    'sure shot stock india',
    'pakka stock tip india'
]

# We DON'T monitor specific channels
# We search by keywords and analyze whoever posts such content


def test_youtube_channels():
    """✅ FAIR: Search by keywords, analyze ANY channel posting pump content"""
    print("=" * 60)
    print("📺 YOUTUBE KEYWORD SEARCH - FAIR APPROACH")
    print("=" * 60)
    print("✅ We search by KEYWORDS (multibagger, penny stock, etc.)")
    print("✅ We DON'T target specific channels")
    print("✅ ANY channel posting such content gets analyzed")
    print("=" * 60)
    
    all_videos = []
    scraper = YouTubeScraperNoAPI()
    
    # Search by keywords, not channels
    for keyword in SEARCH_KEYWORDS[:3]:  # Test first 3 keywords
        print(f"\n🔍 Searching: '{keyword}'")
        videos = scraper.search_video_titles(keyword)
        
        if videos:
            print(f"✅ Found {len(videos)} videos")
            for video in videos[:3]:  # Show top 3
                print(f"   📹 {video['title'][:60]}...")
                if video['tickers']:
                    print(f"      📊 Tickers: {', '.join(video['tickers'])}")
                if video['hype_score'] > 0:
                    print(f"      🚨 Hype Score: {video['hype_score']}")
            all_videos.extend(videos)
        else:
            print(f"⚠️  No videos found")
    
    print("\n" + "=" * 60)
    print(f"📊 SUMMARY")
    print("=" * 60)
    print(f"Keywords searched: {len(SEARCH_KEYWORDS[:3])}")
    print(f"Total videos found: {len(all_videos)}")
    print("\n✅ FAIR APPROACH:")
    print("   - Search by content keywords")
    print("   - Don't target specific channels")
    print("   - Analyze whoever posts pump/dump content")
    print("   - Validate against yfinance/NSE data")
    
    # Aggregate tickers
    ticker_count = {}
    for video in all_videos:
        tickers = scraper.extract_tickers(video['title'])
        for ticker in tickers:
            ticker_count[ticker] = ticker_count.get(ticker, 0) + 1
    
    if ticker_count:
        print(f"\n🔥 Most mentioned tickers:")
        for ticker, count in sorted(ticker_count.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {ticker}: {count} mentions")


if __name__ == "__main__":
    test_youtube_channels()
