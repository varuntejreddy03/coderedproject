"""
Test Advanced Anomaly Detection
Z-score + MAD + Isolation Forest
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.risk_analyzer import RiskAnalyzer

print("=" * 70)
print("🧠 ADVANCED ANOMALY DETECTION TEST")
print("=" * 70)
print("Methods: Z-score + MAD-based Robust Z-score + Isolation Forest (ML)")
print("=" * 70)

analyzer = RiskAnalyzer()

# Test tickers
tickers = ['YESBANK', 'SUZLON', 'RELIANCE', 'TCS', 'TATAMOTORS']

for ticker in tickers:
    print(f"\n📊 Testing: {ticker}")
    print("-" * 70)
    
    result = analyzer.detect_volume_anomaly(ticker)
    
    if result['anomaly_detected']:
        print(f"🚨 ANOMALY DETECTED")
        print(f"   Confidence: {result['confidence'].upper()}")
        print(f"   Methods triggered: {result['methods_triggered']}/3")
        print(f"\n   📈 Metrics:")
        print(f"      Z-score: {result['z_score']}")
        print(f"      Robust Z-score (MAD): {result['robust_z_score']}")
        print(f"      ML Anomaly: {'YES' if result['ml_anomaly'] else 'NO'}")
        print(f"      ML Score: {result['ml_score']}")
        print(f"\n   📊 Volume:")
        print(f"      Recent: {result['recent_volume']:,}")
        print(f"      Average: {result['avg_volume']:,}")
        print(f"      Median: {result['median_volume']:,}")
        print(f"      Spike: {result['volume_spike_percent']}%")
    else:
        print(f"✅ Normal volume")
        print(f"   Z-score: {result.get('z_score', 0)}")
        print(f"   Confidence: {result.get('confidence', 'none')}")

print("\n" + "=" * 70)
print("📚 EXPLANATION")
print("=" * 70)
print("""
1. Z-score: Standard deviation method
   - Anomaly if |Z| > 3 (99.7% confidence)

2. MAD-based Robust Z-score: Handles outliers better
   - Uses median instead of mean
   - More resistant to extreme values

3. Isolation Forest (ML): Unsupervised learning
   - Detects anomalies in multi-dimensional space
   - No training data needed

Confidence Levels:
- HIGH: All 3 methods agree (3/3)
- MEDIUM: 2 methods agree (2/3)
- LOW: Only 1 method detected (1/3)
- NONE: No anomaly detected (0/3)
""")
