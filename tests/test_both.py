"""
Test Both Reddit & YouTube - Keyword Search Approach
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scrapers.reddit_hype_analyzer import RedditHypeAnalyzer
from scrapers.youtube_scraper import YouTubeScraperNoAPI

print("=" * 70)
print("🔍 TESTING REDDIT + YOUTUBE - KEYWORD SEARCH (FAIR APPROACH)")
print("=" * 70)
print("✅ We search by KEYWORDS, not target specific channels/subreddits")
print("=" * 70)

# ==================== REDDIT TEST ====================
print("\n\n📱 REDDIT ANALYSIS")
print("=" * 70)

reddit_analyzer = RedditHypeAnalyzer()
print("🔍 Searching Reddit for: penny stock, multibagger, upper circuit...")

reddit_result = reddit_analyzer.analyze_reddit_hype()

print(f"\n✅ Reddit Results:")
print(f"   Posts analyzed: {reddit_result['total_posts_analyzed']}")
print(f"   Tickers found: {reddit_result['total_tickers_found']}")

print(f"\n🔥 Top 5 Reddit Stocks:")
for i, (ticker, data) in enumerate(list(reddit_result['top_hyped_stocks'].items())[:5], 1):
    print(f"\n{i}. {ticker}")
    print(f"   Mentions: {data['mentions']}")
    print(f"   Hype: {data['hype_intensity']}")
    print(f"   Sample: {data['posts'][0]['title'][:50]}...")

# ==================== YOUTUBE TEST ====================
print("\n\n📺 YOUTUBE ANALYSIS")
print("=" * 70)

youtube_scraper = YouTubeScraperNoAPI()
print("🔍 Searching YouTube for: penny stock india, multibagger...")

youtube_result = youtube_scraper.analyze_youtube_hype()

print(f"\n✅ YouTube Results:")
print(f"   Tickers found: {youtube_result['total_tickers_found']}")

print(f"\n🔥 Top 5 YouTube Stocks:")
for i, (ticker, data) in enumerate(list(youtube_result['top_hyped_stocks'].items())[:5], 1):
    print(f"\n{i}. {ticker}")
    print(f"   Mentions: {data['mentions']}")
    print(f"   Hype: {data['hype_intensity']}")
    print(f"   Videos: {len(data['videos'])}")
    if data['videos']:
        print(f"   Sample: {data['videos'][0][:50]}...")

# ==================== COMBINED SUMMARY ====================
print("\n\n" + "=" * 70)
print("📊 COMBINED SUMMARY")
print("=" * 70)

# Merge tickers from both sources
all_tickers = {}

for ticker, data in reddit_result['top_hyped_stocks'].items():
    all_tickers[ticker] = {
        'reddit_mentions': data['mentions'],
        'reddit_hype': data['hype_intensity'],
        'youtube_mentions': 0,
        'youtube_hype': 0
    }

for ticker, data in youtube_result['top_hyped_stocks'].items():
    if ticker in all_tickers:
        all_tickers[ticker]['youtube_mentions'] = data['mentions']
        all_tickers[ticker]['youtube_hype'] = data['hype_intensity']
    else:
        all_tickers[ticker] = {
            'reddit_mentions': 0,
            'reddit_hype': 0,
            'youtube_mentions': data['mentions'],
            'youtube_hype': data['hype_intensity']
        }

# Calculate combined hype
for ticker in all_tickers:
    all_tickers[ticker]['total_hype'] = (
        all_tickers[ticker]['reddit_hype'] + 
        all_tickers[ticker]['youtube_hype']
    )

# Sort by total hype
sorted_tickers = sorted(all_tickers.items(), key=lambda x: x[1]['total_hype'], reverse=True)

print("\n🔥 TOP 10 MOST HYPED STOCKS (Combined):")
print("-" * 70)
print(f"{'Rank':<6} {'Ticker':<12} {'Reddit':<15} {'YouTube':<15} {'Total':<10}")
print("-" * 70)

for i, (ticker, data) in enumerate(sorted_tickers[:10], 1):
    reddit_str = f"{data['reddit_mentions']}m ({data['reddit_hype']:.0f})"
    youtube_str = f"{data['youtube_mentions']}m ({data['youtube_hype']:.0f})"
    total_str = f"{data['total_hype']:.0f}"
    print(f"{i:<6} {ticker:<12} {reddit_str:<15} {youtube_str:<15} {total_str:<10}")

print("\n" + "=" * 70)
print("✅ NEXT STEP: Validate these against yfinance/NSE data")
print("=" * 70)
print("🔴 High hype + NO official filings = LIKELY RUMOR")
print("✅ High hype + Official filings = LEGITIMATE")
