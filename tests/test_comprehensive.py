"""
Test Comprehensive Ticker Analysis
Demonstrates all UI parameters
"""
import requests
import json

BASE_URL = "http://localhost:8080"
TICKER = "YESBANK"

def test_comprehensive_analysis():
    print("=" * 80)
    print("COMPREHENSIVE TICKER ANALYSIS TEST")
    print("=" * 80)
    print(f"\nTicker: {TICKER}")
    print(f"Endpoint: {BASE_URL}/ticker-analysis/{TICKER}\n")
    
    try:
        response = requests.get(f"{BASE_URL}/ticker-analysis/{TICKER}", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # 1. RISK ASSESSMENT
            print("\n" + "=" * 80)
            print("RISK ASSESSMENT")
            print("=" * 80)
            risk = data['risk_assessment']
            print(f"Score: {risk['score']}/100")
            print(f"Level: {risk['level']}")
            print(f"Color: {risk['color']}")
            
            # 2. MARKET DATA
            print("\n" + "=" * 80)
            print("MARKET DATA")
            print("=" * 80)
            market = data['market_data']
            print(f"Price: ₹{market['price']}")
            print(f"Change: {market['change_percent']:+.2f}%")
            print(f"Volume: {market['volume']:,}")
            print(f"Avg Volume: {market['avg_volume']:,}")
            print(f"Z-Score: {market['z_score']}")
            
            # 3. SOCIAL ACTIVITY
            print("\n" + "=" * 80)
            print("SOCIAL ACTIVITY")
            print("=" * 80)
            
            telegram = data['social_activity']['telegram']
            print(f"\nTelegram: {telegram['mention_count']} mentions")
            print(f"  Sentiment: {telegram['sentiment']}")
            print(f"  Keywords: {', '.join(telegram['keywords'])}")
            
            reddit = data['social_activity']['reddit']
            print(f"\nReddit: {reddit['mention_count']} mentions")
            print(f"  Sentiment: {reddit['sentiment']}")
            print(f"  Keywords: {', '.join(reddit['keywords'])}")
            
            # 4. AI ANALYSIS
            print("\n" + "=" * 80)
            print("AI ANALYSIS")
            print("=" * 80)
            print(data['ai_analysis'])
            
            # 5. RISK BREAKDOWN
            print("\n" + "=" * 80)
            print("RISK BREAKDOWN")
            print("=" * 80)
            breakdown = data['risk_breakdown']
            for key, component in breakdown.items():
                bar = "█" * (component['value'] // 5)
                print(f"{component['label']:.<30} {component['value']:>3}% {bar}")
            
            # 6. LEGITIMACY CHECK
            print("\n" + "=" * 80)
            print("LEGITIMACY VALIDATION (Rumor vs Reality)")
            print("=" * 80)
            legit = data['legitimacy']
            print(f"Verdict: {legit['verdict']}")
            print(f"Legitimacy Score: {legit['legitimacy_score']}/100")
            print(f"Color: {legit['color_indicator']}")
            
            if legit['red_flags']:
                print("\n🚨 RED FLAGS:")
                for flag in legit['red_flags']:
                    print(f"  - {flag}")
            
            if legit['green_flags']:
                print("\n✅ GREEN FLAGS:")
                for flag in legit['green_flags']:
                    print(f"  - {flag}")
            
            print(f"\nRecommendation: {legit['recommendation']}")
            
            # Save full response
            with open(f'ticker_analysis_{TICKER}.json', 'w') as f:
                json.dump(data, f, indent=2)
            print(f"\n✅ Full response saved to: ticker_analysis_{TICKER}.json")
            
        elif response.status_code == 404:
            print(f"❌ No data found for {TICKER}")
            print("Tip: Send a message to Telegram first, then call /refresh")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - Is the server running?")
        print("Start server: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_comprehensive_analysis()
