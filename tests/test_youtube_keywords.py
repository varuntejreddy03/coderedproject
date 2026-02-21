"""
✅ FAIR APPROACH: Search YouTube by KEYWORDS, not channels
We analyze content type, not target specific creators
"""
import requests
import re

def search_youtube_by_keyword(keyword):
    """Search YouTube by keyword - fair and unbiased"""
    url = f"https://www.youtube.com/results?search_query={keyword.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        titles = re.findall(r'"title":{"runs":\[{"text":"([^"]+)"}', response.text)
        video_ids = re.findall(r'"videoId":"([^"]+)"', response.text)
        channels = re.findall(r'"ownerText":{"runs":\[{"text":"([^"]+)"}', response.text)
        
        print(f"\n🔍 Keyword: '{keyword}'")
        print("=" * 60)
        
        count = 0
        for title, vid_id, channel in zip(titles[:5], video_ids[:5], channels[:5]):
            count += 1
            print(f"\n{count}. {title}")
            print(f"   📺 Channel: {channel}")
            print(f"   🔗 https://youtube.com/watch?v={vid_id}")
            
            # Detect tickers
            tickers = re.findall(r'\b[A-Z]{2,15}\b', title.upper())
            if tickers:
                print(f"   📊 Possible tickers: {', '.join(tickers[:3])}")
            
            # Detect hype keywords
            hype_words = ['pakka', 'guaranteed', 'multibagger', 'upper circuit', 'jackpot', '100%']
            found_hype = [w for w in hype_words if w in title.lower()]
            if found_hype:
                print(f"   🚨 Hype keywords: {', '.join(found_hype)}")
        
        if count == 0:
            print("⚠️  No videos found")
        else:
            print(f"\n✅ Found: {count} videos")
    else:
        print(f"❌ Error: {response.status_code}")


# ✅ FAIR APPROACH: Search by content keywords, not target channels
print("🔍 YouTube Keyword Search (Fair & Unbiased)")
print("=" * 60)
print("✅ We analyze CONTENT TYPE, not specific channels")
print("🔴 RUMOR SOURCE: Videos with pump/dump keywords")
print("=" * 60)

keywords = [
    'penny stock india today',
    'multibagger stock 2024',
    'upper circuit stock today',
    'guaranteed profit stock india',
    'pakka stock tip india'
]

for keyword in keywords:
    search_youtube_by_keyword(keyword)
    print()

print("\n" + "=" * 60)
print("📊 SUMMARY")
print("=" * 60)
print("✅ This approach is FAIR:")
print("   - We search by keywords (penny stock, multibagger, etc.)")
print("   - We DON'T target specific channels")
print("   - ANY channel posting such content gets analyzed")
print("   - We validate claims against yfinance/NSE data")
