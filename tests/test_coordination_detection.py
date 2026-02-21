"""
Test Pump-and-Dump Fingerprint Detection
Demonstrates coordination/manipulation detection signals
"""
from datetime import datetime, timedelta
import sys
sys.path.append('..')

from core.risk_analyzer import RiskAnalyzer

def test_coordination_detection():
    analyzer = RiskAnalyzer()
    
    # SCENARIO 1: Cross-channel coordinated pump
    print("\n" + "="*80)
    print("SCENARIO 1: Cross-Channel Coordinated Pump")
    print("="*80)
    
    now = datetime.now()
    coordinated_messages = [
        {"ticker": "RELIANCE", "text": "RELIANCE buy now! Target 3000! UC pakka!", "channel": "channel1", "date": now, "user_id": 123456},
        {"ticker": "RELIANCE", "text": "RELIANCE buy now! Target 3000! UC pakka!", "channel": "channel2", "date": now, "user_id": 234567},
        {"ticker": "RELIANCE", "text": "RELIANCE buy now! Target 3000! UC pakka!", "channel": "channel3", "date": now, "user_id": 345678},
        {"ticker": "RELIANCE", "text": "RELIANCE buy now! Target 3000! UC pakka!", "channel": "channel4", "date": now + timedelta(seconds=30), "user_id": 456789},
    ]
    
    result = analyzer.detect_bot_activity("RELIANCE", coordinated_messages)
    print(f"\n✅ Bot Activity Detected: {result['bot_activity_detected']}")
    print(f"📊 Confidence: {result['confidence']}%")
    print(f"🚨 Risk Level: {result['risk_level']}")
    print(f"\n🔍 Fingerprints Detected:")
    for fp in result['fingerprints']:
        print(f"   • {fp}")
    print(f"\n📋 Indicators:")
    for ind in result['indicators']:
        print(f"   • {ind}")
    
    # SCENARIO 2: Copy-paste campaign
    print("\n" + "="*80)
    print("SCENARIO 2: Copy-Paste Campaign")
    print("="*80)
    
    copypaste_messages = [
        {"ticker": "TATA", "text": "TATA Motors operator game! Buy karo urgent! Last chance!", "channel": "tips1", "date": now, "user_id": 111111},
        {"ticker": "TATA", "text": "TATA Motors operator game! Buy karo urgent! Last chance!", "channel": "tips2", "date": now + timedelta(minutes=2), "user_id": 222222},
        {"ticker": "TATA", "text": "TATA Motors operator game! Buy karo urgent! Last chance!", "channel": "tips3", "date": now + timedelta(minutes=3), "user_id": 333333},
    ]
    
    result = analyzer.detect_bot_activity("TATA", copypaste_messages)
    print(f"\n✅ Bot Activity Detected: {result['bot_activity_detected']}")
    print(f"📊 Confidence: {result['confidence']}%")
    print(f"🚨 Risk Level: {result['risk_level']}")
    print(f"\n🔍 Fingerprints Detected:")
    for fp in result['fingerprints']:
        print(f"   • {fp}")
    
    # SCENARIO 3: Call-to-action spam
    print("\n" + "="*80)
    print("SCENARIO 3: Aggressive Call-to-Action Patterns")
    print("="*80)
    
    cta_messages = [
        {"ticker": "INFY", "text": "INFY buy now! Don't miss this multibagger!", "channel": "pump1", "date": now, "user_id": 444444},
        {"ticker": "INFY", "text": "INFY target 2000! Upper circuit pakka! Book profit!", "channel": "pump2", "date": now + timedelta(minutes=1), "user_id": 555555},
        {"ticker": "INFY", "text": "INFY urgent buy! Last chance before operator exit!", "channel": "pump3", "date": now + timedelta(minutes=2), "user_id": 666666},
    ]
    
    result = analyzer.detect_bot_activity("INFY", cta_messages)
    print(f"\n✅ Bot Activity Detected: {result['bot_activity_detected']}")
    print(f"📊 Confidence: {result['confidence']}%")
    print(f"🚨 Risk Level: {result['risk_level']}")
    print(f"\n🔍 Fingerprints Detected:")
    for fp in result['fingerprints']:
        print(f"   • {fp}")
    
    # SCENARIO 4: Rapid posting burst
    print("\n" + "="*80)
    print("SCENARIO 4: Rapid Posting Burst")
    print("="*80)
    
    rapid_messages = [
        {"ticker": "WIPRO", "text": "WIPRO going up!", "channel": "fast1", "date": now, "user_id": 777777},
        {"ticker": "WIPRO", "text": "WIPRO breakout!", "channel": "fast1", "date": now + timedelta(minutes=1), "user_id": 777777},
        {"ticker": "WIPRO", "text": "WIPRO target hit!", "channel": "fast1", "date": now + timedelta(minutes=2), "user_id": 777777},
        {"ticker": "WIPRO", "text": "WIPRO next level!", "channel": "fast1", "date": now + timedelta(minutes=3), "user_id": 777777},
    ]
    
    result = analyzer.detect_bot_activity("WIPRO", rapid_messages)
    print(f"\n✅ Bot Activity Detected: {result['bot_activity_detected']}")
    print(f"📊 Confidence: {result['confidence']}%")
    print(f"🚨 Risk Level: {result['risk_level']}")
    print(f"\n🔍 Fingerprints Detected:")
    for fp in result['fingerprints']:
        print(f"   • {fp}")
    
    # SCENARIO 5: New suspicious accounts
    print("\n" + "="*80)
    print("SCENARIO 5: New/Suspicious Accounts")
    print("="*80)
    
    new_account_messages = [
        {"ticker": "HDFC", "text": "HDFC buy now!", "channel": "new1", "date": now, "user_id": 5000000001},  # Suspicious high ID
        {"ticker": "HDFC", "text": "HDFC target 2000!", "channel": "new2", "date": now + timedelta(minutes=1), "user_id": 5000000002},
        {"ticker": "HDFC", "text": "HDFC operator game!", "channel": "new3", "date": now + timedelta(minutes=2), "user_id": 5000000003},
    ]
    
    result = analyzer.detect_bot_activity("HDFC", new_account_messages)
    print(f"\n✅ Bot Activity Detected: {result['bot_activity_detected']}")
    print(f"📊 Confidence: {result['confidence']}%")
    print(f"🚨 Risk Level: {result['risk_level']}")
    print(f"\n🔍 Fingerprints Detected:")
    for fp in result['fingerprints']:
        print(f"   • {fp}")
    
    # SCENARIO 6: Legitimate activity (no manipulation)
    print("\n" + "="*80)
    print("SCENARIO 6: Legitimate Activity (Control)")
    print("="*80)
    
    legit_messages = [
        {"ticker": "TCS", "text": "TCS quarterly results look good", "channel": "news1", "date": now, "user_id": 123456},
        {"ticker": "TCS", "text": "TCS dividend announced", "channel": "news2", "date": now + timedelta(hours=2), "user_id": 234567},
    ]
    
    result = analyzer.detect_bot_activity("TCS", legit_messages)
    print(f"\n✅ Bot Activity Detected: {result['bot_activity_detected']}")
    print(f"📊 Confidence: {result['confidence']}%")
    print(f"🚨 Risk Level: {result['risk_level']}")
    print(f"\n🔍 Fingerprints Detected:")
    if result['fingerprints']:
        for fp in result['fingerprints']:
            print(f"   • {fp}")
    else:
        print("   None - Normal activity")
    
    print("\n" + "="*80)
    print("✅ All coordination detection tests completed!")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_coordination_detection()
