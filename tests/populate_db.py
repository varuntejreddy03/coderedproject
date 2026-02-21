"""
Populate Supabase with Real Data
Scrapes Telegram/Reddit/YouTube and stores in database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from core.supabase_db import SupabaseDB
from scrapers.reddit_hype_analyzer import RedditHypeAnalyzer
from scrapers.youtube_scraper import YouTubeScraperNoAPI
import asyncio

print("=" * 70)
print("\ud83d\udce5 POPULATING SUPABASE WITH REAL DATA")
print("=" * 70)

db = SupabaseDB()

# ==================== REDDIT DATA ====================
print("\n\ud83d\udcf1 Scraping Reddit...")
reddit = RedditHypeAnalyzer()
reddit_result = reddit.analyze_reddit_hype()

print(f"\u2705 Found {reddit_result['total_posts_analyzed']} Reddit posts")
print("\ud83d\udcbe Storing in Supabase...")

stored_reddit = 0
for ticker, data in reddit_result['top_hyped_stocks'].items():
    for post in data['posts'][:5]:  # Store top 5 posts per ticker
        try:
            db.store_reddit_post(post)
            stored_reddit += 1
        except Exception as e:
            print(f"\u26a0\ufe0f Error storing Reddit post: {e}")

print(f"\u2705 Stored {stored_reddit} Reddit posts")

# ==================== YOUTUBE DATA ====================
print("\n\ud83d\udcfa Scraping YouTube...")
youtube = YouTubeScraperNoAPI()
youtube_result = youtube.analyze_youtube_hype()

print(f"\u2705 Found {youtube_result['total_tickers_found']} tickers on YouTube")
print("\ud83d\udcbe Storing in Supabase...")

stored_youtube = 0
for ticker, data in youtube_result['top_hyped_stocks'].items():
    for video_title in data['videos'][:3]:  # Store top 3 videos per ticker
        try:
            video_data = {
                'title': video_title,
                'channel': 'Unknown',
                'tickers': [ticker],
                'hype_score': data['avg_hype_score'],
                'url': f'https://youtube.com/results?search_query={ticker}'
            }
            db.store_youtube_video(video_data)
            stored_youtube += 1
        except Exception as e:
            print(f"\u26a0\ufe0f Error storing YouTube video: {e}")

print(f"\u2705 Stored {stored_youtube} YouTube videos")

# ==================== TELEGRAM DATA ====================
print("\n\ud83d\udce8 Scraping Telegram...")
from scrapers.simple_telegram import SimpleTelegramScraper

async def scrape_telegram():
    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    channels = [c.strip() for c in os.getenv("CHANNELS", "").split(",") if c.strip()]
    
    if not channels:
        print("\u26a0\ufe0f No Telegram channels configured")
        return 0
    
    scraper = SimpleTelegramScraper(api_id, api_hash, channels)
    await scraper.connect()
    messages = await scraper.fetch_messages(limit=50)
    await scraper.disconnect()
    
    print(f"\u2705 Found {len(messages)} Telegram messages")
    print("\ud83d\udcbe Storing in Supabase...")
    
    stored_telegram = 0
    for msg in messages:
        try:
            db.store_telegram_message(msg)
            stored_telegram += 1
        except Exception as e:
            print(f"\u26a0\ufe0f Error storing Telegram message: {e}")
    
    return stored_telegram

stored_telegram = asyncio.run(scrape_telegram())
print(f"\u2705 Stored {stored_telegram} Telegram messages")

# ==================== SUMMARY ====================
print("\n" + "=" * 70)
print("\ud83d\udcca SUMMARY")
print("=" * 70)
print(f"Reddit posts stored: {stored_reddit}")
print(f"YouTube videos stored: {stored_youtube}")
print(f"Telegram messages stored: {stored_telegram}")
print(f"Total records: {stored_reddit + stored_youtube + stored_telegram}")
print("\n\u2705 Database populated with real data!")
print("\nView data: Supabase Dashboard \u2192 Table Editor \u2192 rumor_sources")
