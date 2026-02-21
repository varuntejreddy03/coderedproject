"""
Risk Analysis Module - Anomaly Detection & Bot Activity

🔴 ANALYZES RUMOR SOURCES (Untrusted):
   - Telegram messages (for bot detection)
   - Reddit posts (for coordination patterns)

✅ VALIDATES WITH TRUSTED SOURCES:
   - yfinance volume data (for Z-score anomaly detection)
   - Historical market data (statistical analysis)

Implements:
   - Z-score volume analysis (using yfinance)
   - Coordinated manipulation detection
   - Bot activity patterns
   - Unified risk scoring
"""
import yfinance as yf
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class RiskAnalyzer:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = timedelta(minutes=5)
    
    def detect_volume_anomaly(self, ticker: str) -> Dict:
        """
        ✅ Advanced anomaly detection using TRUSTED yfinance data
        Uses: Z-score + MAD-based robust Z-score + Isolation Forest
        Returns anomaly confidence: high/medium/low
        """
        try:
            stock = yf.Ticker(f"{ticker}.NS")
            hist = stock.history(period="3mo")
            
            if hist.empty or len(hist) < 20:
                return {"anomaly_detected": False, "confidence": "low", "reason": "Insufficient data"}
            
            volumes = hist['Volume'].values
            recent_volume = volumes[-1]
            
            # Method 1: Standard Z-score
            mean_volume = np.mean(volumes[:-1])
            std_volume = np.std(volumes[:-1])
            z_score = (recent_volume - mean_volume) / std_volume if std_volume > 0 else 0
            
            # Method 2: MAD-based robust Z-score (handles outliers better)
            median_volume = np.median(volumes[:-1])
            mad = np.median(np.abs(volumes[:-1] - median_volume))
            robust_z_score = 0.6745 * (recent_volume - median_volume) / mad if mad > 0 else 0
            
            # Method 3: Isolation Forest (ML-based)
            if len(volumes) >= 30:
                # Reshape for sklearn
                X = volumes[:-1].reshape(-1, 1)
                X_test = np.array([[recent_volume]])
                
                # Train Isolation Forest
                iso_forest = IsolationForest(contamination=0.1, random_state=42)
                iso_forest.fit(X)
                
                # Predict (-1 = anomaly, 1 = normal)
                prediction = iso_forest.predict(X_test)[0]
                anomaly_score = iso_forest.score_samples(X_test)[0]
                
                is_anomaly_ml = prediction == -1
            else:
                is_anomaly_ml = False
                anomaly_score = 0
            
            # Combine all methods for confidence
            anomaly_signals = 0
            
            if abs(z_score) > 3:
                anomaly_signals += 1
            if abs(robust_z_score) > 3:
                anomaly_signals += 1
            if is_anomaly_ml:
                anomaly_signals += 1
            
            # Determine confidence
            if anomaly_signals >= 3:
                confidence = "high"
                anomaly_detected = True
            elif anomaly_signals == 2:
                confidence = "medium"
                anomaly_detected = True
            elif anomaly_signals == 1:
                confidence = "low"
                anomaly_detected = True
            else:
                confidence = "none"
                anomaly_detected = False
            
            return {
                "anomaly_detected": bool(anomaly_detected),
                "confidence": confidence,
                "z_score": float(round(float(z_score), 2)),
                "robust_z_score": float(round(float(robust_z_score), 2)),
                "ml_anomaly": bool(is_anomaly_ml),
                "ml_score": float(round(float(anomaly_score), 4)),
                "recent_volume": int(recent_volume),
                "avg_volume": int(mean_volume),
                "median_volume": int(median_volume),
                "volume_spike_percent": float(round(((recent_volume - mean_volume) / mean_volume) * 100, 2)) if mean_volume > 0 else 0.0,
                "methods_triggered": anomaly_signals,
                "reason": f"{anomaly_signals}/3 methods detected anomaly" if anomaly_detected else "Normal volume"
            }
        except Exception as e:
            logger.error(f"Error detecting anomaly for {ticker}: {e}")
            return {"anomaly_detected": False, "confidence": "error", "reason": f"Error: {str(e)}"}
    
    def detect_bot_activity(self, ticker: str, messages: List[Dict]) -> Dict:
        """
        🔴 Detect pump-and-dump fingerprints from RUMOR SOURCES (Telegram/Reddit)
        Detects: cross-channel coordination, copy-paste campaigns, call-to-action patterns, new accounts
        """
        if not messages:
            return {"bot_activity_detected": False, "confidence": 0, "indicators": [], "fingerprints": []}
        
        indicators = []
        fingerprints = []
        confidence = 0
        
        # FINGERPRINT 1: Cross-channel coordination (same ticker pushed across multiple channels within short window)
        channels_by_time = {}
        for msg in messages:
            if msg.get('channel') and msg.get('date'):
                date = msg['date']
                # Convert string to datetime if needed
                if isinstance(date, str):
                    try:
                        from dateutil import parser
                        date = parser.parse(date)
                    except:
                        continue
                
                time_bucket = date.replace(second=0, microsecond=0)  # Group by minute
                if time_bucket not in channels_by_time:
                    channels_by_time[time_bucket] = set()
                channels_by_time[time_bucket].add(msg['channel'])
        
        for time_bucket, channels in channels_by_time.items():
            if len(channels) >= 3:
                fingerprints.append(f"Cross-channel: {len(channels)} channels within 1 min")
                indicators.append(f"Coordinated push across {len(channels)} channels")
                confidence += 35
                break
        
        # FINGERPRINT 2: Copy-paste campaigns (similar phrases reused)
        texts = [msg.get('text', '').lower() for msg in messages]
        if len(texts) >= 2:
            similar_pairs = 0
            for i in range(len(texts)):
                for j in range(i+1, len(texts)):
                    words_i = set(texts[i].split())
                    words_j = set(texts[j].split())
                    if words_i and words_j:
                        similarity = len(words_i & words_j) / len(words_i | words_j)
                        if similarity > 0.7:
                            similar_pairs += 1
            
            if similar_pairs >= 2:
                fingerprints.append(f"Copy-paste: {similar_pairs} duplicate messages")
                indicators.append(f"{similar_pairs} copy-pasted messages detected")
                confidence += 30
        
        # FINGERPRINT 3: Call-to-action patterns
        cta_patterns = [
            'buy now', 'buy karo', 'target', 'uc pakka', 'upper circuit', 
            'operator game', 'operator stock', 'multibagger', 'book profit',
            'exit', 'sell karo', 'last chance', 'don\'t miss', 'urgent'
        ]
        cta_count = 0
        cta_found = []
        for msg in messages:
            text = msg.get('text', '').lower()
            for pattern in cta_patterns:
                if pattern in text:
                    cta_count += 1
                    if pattern not in cta_found:
                        cta_found.append(pattern)
        
        if cta_count >= 3:
            fingerprints.append(f"Call-to-action: {len(cta_found)} patterns ({', '.join(cta_found[:3])})")
            indicators.append(f"Aggressive call-to-action detected: {', '.join(cta_found[:2])}")
            confidence += 25
        
        # FINGERPRINT 4: Rapid posting (multiple posts within 5 minutes)
        timestamps = [msg.get('date') for msg in messages if msg.get('date') and not isinstance(msg.get('date'), str)]
        if len(timestamps) >= 3:
            timestamps.sort()
            rapid_bursts = 0
            for i in range(len(timestamps) - 2):
                time_window = (timestamps[i+2] - timestamps[i]).total_seconds() / 60
                if time_window <= 5:
                    rapid_bursts += 1
            
            if rapid_bursts >= 1:
                fingerprints.append(f"Rapid posting: {rapid_bursts} bursts detected")
                indicators.append(f"{rapid_bursts} rapid posting bursts (3+ msgs in 5 min)")
                confidence += 20
        
        # FINGERPRINT 5: New/suspicious accounts (if metadata exists)
        new_accounts = 0
        for msg in messages:
            user_id = msg.get('user_id')
            # Check if user_id looks suspicious (very high numbers = new accounts)
            if user_id and isinstance(user_id, int) and user_id > 5000000000:
                new_accounts += 1
        
        if new_accounts >= 2:
            fingerprints.append(f"New accounts: {new_accounts} suspicious IDs")
            indicators.append(f"{new_accounts} new/suspicious accounts posting")
            confidence += 15
        
        bot_detected = confidence >= 50
        
        return {
            "bot_activity_detected": bool(bot_detected),
            "confidence": int(min(confidence, 100)),
            "indicators": indicators,
            "fingerprints": fingerprints,
            "risk_level": "HIGH" if confidence >= 70 else "MEDIUM" if confidence >= 50 else "LOW"
        }
    
    def calculate_unified_risk_score(self, ticker: str, hype_score: float, fraud_score: int, 
                                     anomaly_data: Dict, bot_data: Dict) -> Dict:
        """
        Unified Risk Score (0-100)
        Combines: hype intensity + fraud signals + volume anomaly + bot activity
        """
        # Normalize inputs to 0-25 scale
        hype_component = min(hype_score / 4, 25)  # Hype score 0-100 -> 0-25
        fraud_component = min(fraud_score * 2.5, 25)  # Fraud score 0-10 -> 0-25
        anomaly_component = min(anomaly_data.get('z_score', 0) * 5, 25) if anomaly_data.get('anomaly_detected') else 0
        bot_component = min(bot_data.get('confidence', 0) / 4, 25)  # Bot confidence 0-100 -> 0-25
        
        # Total risk score
        risk_score = hype_component + fraud_component + anomaly_component + bot_component
        
        # Risk level
        if risk_score >= 75:
            risk_level = "CRITICAL"
            color = "RED"
        elif risk_score >= 50:
            risk_level = "HIGH"
            color = "RED"
        elif risk_score >= 30:
            risk_level = "MEDIUM"
            color = "AMBER"
        else:
            risk_level = "LOW"
            color = "GREEN"
        
        return {
            "ticker": ticker,
            "risk_score": float(round(risk_score, 1)),
            "risk_level": risk_level,
            "color_indicator": color,
            "components": {
                "hype": float(round(hype_component, 1)),
                "fraud": float(round(fraud_component, 1)),
                "anomaly": float(round(anomaly_component, 1)),
                "bot_activity": float(round(bot_component, 1))
            }
        }
    
    def generate_risk_explanation(self, ticker: str, risk_data: Dict, anomaly_data: Dict, 
                                  bot_data: Dict, fraud_triggers: List[str]) -> str:
        """
        Generate natural language explanation for why stock is risky
        """
        risk_score = risk_data['risk_score']
        risk_level = risk_data['risk_level']
        
        if risk_score < 30:
            return f"✅ {ticker} shows LOW risk. No significant manipulation signals detected. Normal trading activity observed."
        
        reasons = []
        
        # Hype component
        if risk_data['components']['hype'] > 15:
            reasons.append(f"High social media hype (score: {risk_data['components']['hype']:.0f}/25)")
        
        # Fraud component
        if fraud_triggers:
            reasons.append(f"Detected {len(fraud_triggers)} fraud keywords: {', '.join(fraud_triggers[:3])}")
        
        # Anomaly component
        if anomaly_data.get('anomaly_detected'):
            reasons.append(f"Unusual volume spike: {anomaly_data['volume_spike_percent']:.0f}% above average ({anomaly_data['z_score']:.1f}σ)")
        
        # Bot component
        if bot_data.get('bot_activity_detected'):
            reasons.append(f"Coordinated bot activity detected: {', '.join(bot_data['indicators'][:2])}")
        
        if not reasons:
            reasons.append("Multiple risk factors detected")
        
        explanation = f"⚠️ {ticker} shows {risk_level} risk (score: {risk_score:.0f}/100). "
        explanation += " | ".join(reasons)
        explanation += f". Recommendation: {'AVOID - High manipulation risk' if risk_score >= 70 else 'CAUTION - Verify before trading' if risk_score >= 50 else 'Monitor closely'}."
        
        return explanation


def get_all_anomalies(tickers: List[str]) -> List[Dict]:
    """Get volume anomalies for multiple tickers"""
    analyzer = RiskAnalyzer()
    anomalies = []
    
    for ticker in tickers:
        result = analyzer.detect_volume_anomaly(ticker)
        if result['anomaly_detected']:
            anomalies.append({
                "ticker": ticker,
                **result
            })
    
    return sorted(anomalies, key=lambda x: x['z_score'], reverse=True)
