"""
Mention Burst Detection - Early Warning System
Tracks mention rate per ticker: 5-min baseline vs current 5-min window
Catches pumps BEFORE price spike
"""
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class MentionBurstDetector:
    def __init__(self):
        # Store timestamps per ticker: {ticker: [timestamp1, timestamp2, ...]}
        self.mention_history = defaultdict(list)
        self.baseline_window = timedelta(minutes=30)  # Historical baseline
        self.current_window = timedelta(minutes=5)    # Current activity
    
    def add_mention(self, ticker: str, timestamp: datetime = None):
        """Record a ticker mention"""
        if timestamp is None:
            timestamp = datetime.now()
        self.mention_history[ticker].append(timestamp)
        self._cleanup_old_mentions(ticker)
    
    def _cleanup_old_mentions(self, ticker: str):
        """Remove mentions older than baseline window"""
        cutoff = datetime.now() - self.baseline_window
        self.mention_history[ticker] = [
            ts for ts in self.mention_history[ticker] if ts > cutoff
        ]
    
    def detect_burst(self, ticker: str) -> Dict:
        """
        Detect mention burst: current 5-min vs baseline
        Returns burst score 0-100
        """
        now = datetime.now()
        timestamps = self.mention_history.get(ticker, [])
        
        if len(timestamps) < 3:
            return {
                "burst_detected": False,
                "burst_score": 0,
                "current_rate": 0,
                "baseline_rate": 0,
                "velocity_multiplier": 0
            }
        
        # Current 5-min window
        current_cutoff = now - self.current_window
        current_mentions = [ts for ts in timestamps if ts > current_cutoff]
        current_rate = len(current_mentions)
        
        # Baseline: 30-min history excluding current 5-min
        baseline_cutoff = now - self.baseline_window
        baseline_mentions = [ts for ts in timestamps if baseline_cutoff < ts <= current_cutoff]
        baseline_rate = len(baseline_mentions) / 5 if baseline_mentions else 0.5  # Avg per 5-min
        
        # Calculate velocity multiplier
        velocity_multiplier = current_rate / baseline_rate if baseline_rate > 0 else current_rate
        
        # Burst score (0-100)
        if velocity_multiplier >= 5:
            burst_score = 100
        elif velocity_multiplier >= 3:
            burst_score = 75
        elif velocity_multiplier >= 2:
            burst_score = 50
        elif velocity_multiplier >= 1.5:
            burst_score = 25
        else:
            burst_score = 0
        
        burst_detected = velocity_multiplier >= 3
        
        return {
            "burst_detected": burst_detected,
            "burst_score": int(burst_score),
            "current_rate": current_rate,
            "baseline_rate": round(baseline_rate, 1),
            "velocity_multiplier": round(velocity_multiplier, 1),
            "alert_level": "CRITICAL" if velocity_multiplier >= 5 else "HIGH" if velocity_multiplier >= 3 else "MEDIUM" if velocity_multiplier >= 2 else "LOW"
        }
    
    def get_trending_tickers(self, min_burst_score: int = 50) -> List[Dict]:
        """Get all tickers with burst activity"""
        trending = []
        for ticker in self.mention_history.keys():
            result = self.detect_burst(ticker)
            if result['burst_score'] >= min_burst_score:
                trending.append({"ticker": ticker, **result})
        return sorted(trending, key=lambda x: x['burst_score'], reverse=True)

# Global instance
burst_detector = MentionBurstDetector()
