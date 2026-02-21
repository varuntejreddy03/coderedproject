"""
Quick Test - Get videos from specific channel (last 1 day)
Usage: python test_youtube_simple.py
"""
import requests
import re

def get_videos_last_day(channel_handle):
    """Get videos from last 1 day"""
    url = f"https://www.youtube.com/{channel_handle}/videos"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        titles = re.findall(r'"title":{"runs":\[{"text":"([^"]+)"}', response.text)
        video_ids = re.findall(r'"videoId":"([^"]+)"', response.text)
        times = re.findall(r'"publishedTimeText":{"simpleText":"([^"]+)"}', response.text)
        
        print(f"\n📺 Channel: {channel_handle}")
        print("=" * 60)
        
        count = 0
        for title, vid_id, pub_time in zip(titles[:20], video_ids[:20], times[:20]):
            # Check if uploaded in last 1 day
            if any(x in pub_time.lower() for x in ['hour', 'hours', 'minute', 'minutes', '1 day']):
                count += 1
                print(f"\n{count}. {title}")
                print(f"   ⏰ {pub_time}")
                print(f"   🔗 https://youtube.com/watch?v={vid_id}")
        
        if count == 0:
            print("⚠️  No videos uploaded in last 1 day")
        else:
            print(f"\n✅ Total: {count} videos from last 1 day")
    else:
        print(f"❌ Error: {response.status_code}")


# Test with 🔴 RUMOR SOURCE channels (stock tip/pump channels)
print("🔍 Testing YouTube Channels (Last 1 Day)")
print("🔴 RUMOR SOURCES: Stock tip channels (UNTRUSTED)")
print("=" * 60)

channels = [
    '@StockMarketHindi',
    '@ShareMarketKaFunda', 
    '@PennyStockIndia',
    '@IntradayTips',
    '@MultibaggerStocks'
]

for channel in channels:
    get_videos_last_day(channel)
    print()
