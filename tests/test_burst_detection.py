"""
Test Mention Burst Detection
Demonstrates: 5-min baseline vs current 5-min window
Catches pumps BEFORE price spike
"""
from datetime import datetime, timedelta
import sys
sys.path.append('..')

from core.mention_burst_detector import MentionBurstDetector

def test_burst_detection():
    detector = MentionBurstDetector()
    
    print("\n" + "="*80)
    print("MENTION BURST DETECTION - Early Warning System")
    print("="*80)
    
    # SCENARIO 1: Normal baseline activity
    print("\n📊 SCENARIO 1: Establishing Baseline (30 min history)")
    print("-" * 80)
    
    now = datetime.now()
    ticker = "RELIANCE"
    
    # Simulate normal activity: 1 mention every 5 minutes (baseline)
    for i in range(6):
        timestamp = now - timedelta(minutes=30 - i*5)
        detector.add_mention(ticker, timestamp)
        print(f"  ✓ Mention at {timestamp.strftime('%H:%M')} (baseline)")
    
    result = detector.detect_burst(ticker)
    print(f"\n📈 Current Activity: {result['current_rate']} mentions in last 5 min")
    print(f"📊 Baseline Rate: {result['baseline_rate']} mentions per 5 min")
    print(f"⚡ Velocity: {result['velocity_multiplier']}x baseline")
    print(f"🚨 Burst Score: {result['burst_score']}/100")
    print(f"✅ Status: {result['alert_level']}")
    
    # SCENARIO 2: Sudden pump activity
    print("\n" + "="*80)
    print("📊 SCENARIO 2: PUMP DETECTED - Sudden Burst!")
    print("-" * 80)
    
    # Simulate pump: 15 mentions in last 5 minutes
    for i in range(15):
        timestamp = now - timedelta(minutes=4 - i*0.3)
        detector.add_mention(ticker, timestamp)
        print(f"  🔴 Rapid mention at {timestamp.strftime('%H:%M:%S')}")
    
    result = detector.detect_burst(ticker)
    print(f"\n📈 Current Activity: {result['current_rate']} mentions in last 5 min")
    print(f"📊 Baseline Rate: {result['baseline_rate']} mentions per 5 min")
    print(f"⚡ Velocity: {result['velocity_multiplier']}x baseline")
    print(f"🚨 Burst Score: {result['burst_score']}/100")
    print(f"🚨 Status: {result['alert_level']}")
    
    if result['burst_detected']:
        print(f"\n⚠️  ALERT: Pump activity detected BEFORE price spike!")
        print(f"    Mention rate increased {result['velocity_multiplier']}x in last 5 minutes")
    
    # SCENARIO 3: Multiple tickers comparison
    print("\n" + "="*80)
    print("📊 SCENARIO 3: Multi-Ticker Comparison")
    print("-" * 80)
    
    # Add activity for other tickers
    tickers = ["TATA", "INFY", "HDFC", "WIPRO"]
    
    for ticker in tickers:
        # Normal baseline
        for i in range(3):
            detector.add_mention(ticker, now - timedelta(minutes=20 - i*5))
        
        # TATA gets pumped
        if ticker == "TATA":
            for i in range(12):
                detector.add_mention(ticker, now - timedelta(minutes=4 - i*0.3))
    
    print("\nTicker Analysis:")
    print("-" * 80)
    for ticker in ["RELIANCE", "TATA", "INFY", "HDFC", "WIPRO"]:
        result = detector.detect_burst(ticker)
        status_icon = "🔴" if result['burst_detected'] else "✅"
        print(f"{status_icon} {ticker:10} | Current: {result['current_rate']:2} | "
              f"Baseline: {result['baseline_rate']:4.1f} | "
              f"Velocity: {result['velocity_multiplier']:4.1f}x | "
              f"Score: {result['burst_score']:3}/100 | "
              f"{result['alert_level']}")
    
    # SCENARIO 4: Trending tickers
    print("\n" + "="*80)
    print("📊 SCENARIO 4: Trending Tickers (Burst Score >= 50)")
    print("-" * 80)
    
    trending = detector.get_trending_tickers(min_burst_score=50)
    
    if trending:
        print(f"\n🔥 {len(trending)} tickers showing burst activity:\n")
        for i, t in enumerate(trending, 1):
            print(f"{i}. {t['ticker']:10} | Score: {t['burst_score']:3}/100 | "
                  f"Velocity: {t['velocity_multiplier']:4.1f}x | "
                  f"Alert: {t['alert_level']}")
    else:
        print("\n✅ No burst activity detected")
    
    print("\n" + "="*80)
    print("✅ Burst detection test completed!")
    print("="*80)
    print("\n💡 Key Insight: Burst detection catches pumps BEFORE price moves")
    print("   Social media hype → (burst detected) → Price spike")
    print("   This gives early warning (minutes to hours ahead)\n")

if __name__ == "__main__":
    test_burst_detection()
