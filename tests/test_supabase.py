"""
Test Supabase Connection
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load .env file
from dotenv import load_dotenv
load_dotenv()

from core.supabase_db import SupabaseDB
from datetime import datetime

print("=" * 60)
print("🔌 TESTING SUPABASE CONNECTION")
print("=" * 60)

# Debug: Check if env vars are loaded
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
print(f"\n🔍 URL loaded: {url[:30] if url else 'NOT FOUND'}...")
print(f"🔍 KEY loaded: {key[:30] if key else 'NOT FOUND'}...\n")

try:
    db = SupabaseDB()
    print("✅ Connected to Supabase")
    
    # Test 1: Store a test rumor source
    print("\n📝 Test 1: Storing test Telegram message...")
    test_message = {
        'channel': 'test_channel',
        'text': 'YESBANK pakka upper circuit tomorrow',
        'tickers': ['YESBANK'],
        'fraud_score': 3,
        'date': datetime.now().isoformat()
    }
    
    result = db.store_telegram_message(test_message)
    print(f"✅ Stored message ID: {result.data[0]['id']}")
    
    # Test 2: Query high risk tickers
    print("\n📊 Test 2: Querying high risk tickers...")
    high_risk = db.get_high_risk_tickers(min_risk=70)
    print(f"✅ Found {len(high_risk.data)} high risk tickers")
    
    if high_risk.data:
        for ticker in high_risk.data[:5]:
            print(f"   - {ticker['ticker']}: Risk {ticker['risk_score']}")
    
    # Test 3: Query rumor sources
    print("\n🔍 Test 3: Querying rumor sources for YESBANK...")
    rumors = db.get_rumor_sources_by_ticker('YESBANK')
    print(f"✅ Found {len(rumors.data)} rumor sources")
    
    if rumors.data:
        for rumor in rumors.data[:3]:
            print(f"   - {rumor['source']}: {rumor.get('text', rumor.get('title', ''))[:50]}...")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n💡 Make sure:")
    print("   1. SUPABASE_URL is set in .env")
    print("   2. SUPABASE_KEY is set in .env")
    print("   3. Tables are created (run schema.sql)")
    print("   4. pip install supabase")
