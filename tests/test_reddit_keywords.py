"""
✅ FAIR APPROACH: Search Reddit by KEYWORDS, not specific subreddits
We analyze content type across ALL Reddit, not target specific communities
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scrapers.reddit_hype_analyzer import RedditHypeAnalyzer

print("=" * 60)
print("🔍 REDDIT KEYWORD SEARCH - FAIR APPROACH")
print("=" * 60)
print("✅ We search ALL Reddit by KEYWORDS")
print("✅ We DON'T target specific subreddits")
print("✅ ANY subreddit with pump/dump content gets analyzed")
print("=" * 60)

analyzer = RedditHypeAnalyzer()

print("\n🔍 Searching Reddit for pump/dump keywords...")
print("Keywords: penny stock, multibagger, upper circuit, etc.")
print()

result = analyzer.analyze_reddit_hype()

print("\n" + "=" * 60)
print("📊 RESULTS")
print("=" * 60)
print(f"Total posts analyzed: {result['total_posts_analyzed']}")
print(f"Total tickers found: {result['total_tickers_found']}")

print("\n🔥 TOP 10 HYPED STOCKS:")
for i, (ticker, data) in enumerate(list(result['top_hyped_stocks'].items())[:10], 1):
    print(f"\n{i}. {ticker}")
    print(f"   Mentions: {data['mentions']}")
    print(f"   Hype Intensity: {data['hype_intensity']}")
    print(f"   Avg Hype Score: {data['avg_hype_score']}")
    print(f"   Sample post: {data['posts'][0]['title'][:60]}...")
    print(f"   Subreddit: r/{data['posts'][0]['subreddit']}")

print("\n" + "=" * 60)
print("✅ FAIR APPROACH SUMMARY:")
print("=" * 60)
print("✅ Searched by content keywords (multibagger, penny stock, etc.)")
print("✅ Analyzed posts from ANY subreddit")
print("✅ No specific communities targeted")
print("✅ Claims will be validated against yfinance/NSE data")
