"""
Intelligence Engine - Advanced Fraud Detection

🔴 ANALYZES RUMOR SOURCES (Untrusted):
   - Telegram messages (pump groups)
   - Reddit posts (speculation)

DETECTS:
   - Sentiment (bullish/bearish)
   - Fraud triggers ("pakka", "guaranteed", "upper circuit")
   - Hinglish variants
   - Hype intensity
   - Bot coordination patterns

OUTPUT: Risk indicators that are validated against trusted sources (yfinance/NSE)
"""
import re
from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict

# 1️⃣ Sentiment Layer - Weighted Keywords
SENTIMENT_KEYWORDS = {
    # Positive (bullish)
    'positive': {
        'rocket': 0.8, 'moon': 0.7, 'bullish': 0.6, 'buy': 0.5, 'profit': 0.6,
        'gain': 0.5, 'up': 0.4, 'high': 0.4, 'strong': 0.5, 'breakout': 0.7
    },
    # Negative (bearish)
    'negative': {
        'crash': -0.8, 'dump': -0.7, 'loss': -0.6, 'sell': -0.5, 'down': -0.4,
        'weak': -0.5, 'bearish': -0.6, 'fall': -0.5, 'drop': -0.6
    }
}

# 2️⃣ Fraud Trigger Engine - Weighted Phrases (from RUMOR SOURCES)
# These keywords indicate potential pump & dump schemes on Telegram/Reddit
FRAUD_TRIGGERS = {
    # High risk (weight: 3)
    'upper circuit pakka': 3, 'operator game': 3, 'sure shot': 3,
    'guaranteed profit': 3, '100% confirmed': 3, 'insider info': 3,
    
    # Medium risk (weight: 2)
    'multibagger confirmed': 2, 'rocket stock': 2, 'jackpot': 2,
    'dont miss': 2, 'last chance': 2, 'limited seats': 2,
    'premium tip': 2, 'paid group': 2, 'urgent': 2,
    
    # Low risk (weight: 1)
    'target': 1, 'book profit': 1, 'btst': 1, 'intraday': 1,
    'call': 1, 'tip': 1, 'recommendation': 1
}

# 3️⃣ Hinglish Normalization Map
HINGLISH_VARIANTS = {
    # Pakka variants
    'pakkaaa': 'pakka', 'pukka': 'pakka', 'pakaaa': 'pakka', 'pakkaa': 'pakka',
    'paka': 'pakka', 'pakaa': 'pakka',
    
    # Guaranteed variants
    'guaranteed': 'guaranteed', 'guaranted': 'guaranteed', 'guranteed': 'guaranteed',
    'garunteed': 'guaranteed', 'gauranteed': 'guaranteed',
    
    # Other common Hinglish
    'zaroor': 'sure', 'zarur': 'sure', 'jarur': 'sure',
    'bilkul': 'absolutely', 'bilkull': 'absolutely',
    'ekdum': 'totally', 'ekdam': 'totally',
    'bahut': 'very', 'bohot': 'very', 'bhot': 'very',
    'accha': 'good', 'acha': 'good', 'achha': 'good',
    'kharab': 'bad', 'kharaab': 'bad',
    'jaldi': 'quick', 'jaldee': 'quick',
    'abhi': 'now', 'abi': 'now',
    'karo': 'do', 'kro': 'do',
    'lena': 'take', 'lelo': 'take',
    'bechna': 'sell', 'becho': 'sell',
    'khareedna': 'buy', 'kharidna': 'buy'
}


class IntelligenceEngine:
    def __init__(self):
        self.ticker_history = defaultdict(list)  # Track mentions over time
        from core.vernacular_detector import vernacular_detector
        self.vernacular = vernacular_detector
        
    def normalize_hinglish(self, text: str) -> str:
        """Normalize Hinglish variants"""
        text = text.lower()
        words = text.split()
        normalized = []
        
        for word in words:
            # Remove repeated characters (e.g., "pakkaaa" -> "pakka")
            cleaned = re.sub(r'(.)\1{2,}', r'\1\1', word)
            # Map to standard form
            normalized.append(HINGLISH_VARIANTS.get(cleaned, cleaned))
        
        return ' '.join(normalized)
    
    def calculate_sentiment(self, text: str) -> float:
        """Calculate sentiment score (-1 to +1)"""
        text = text.lower()
        score = 0.0
        count = 0
        
        # Positive keywords
        for word, weight in SENTIMENT_KEYWORDS['positive'].items():
            if word in text:
                score += weight
                count += 1
        
        # Negative keywords
        for word, weight in SENTIMENT_KEYWORDS['negative'].items():
            if word in text:
                score += weight
                count += 1
        
        # Normalize to -1 to +1 range
        if count > 0:
            score = max(-1.0, min(1.0, score / count))
        
        return round(score, 2)
    
    def detect_fraud_triggers(self, text: str) -> Dict:
        """Detect fraud triggers with weighted scoring"""
        text = text.lower()
        detected = {}
        total_weight = 0
        
        for phrase, weight in FRAUD_TRIGGERS.items():
            if phrase in text:
                detected[phrase] = weight
                total_weight += weight
        
        return {
            'triggers': list(detected.keys()),
            'weights': detected,
            'total_score': total_weight
        }
    
    def track_ticker_mention(self, ticker: str, timestamp):
        """Track ticker mentions for velocity calculation"""
        # Convert string to datetime if needed
        if isinstance(timestamp, str):
            from dateutil import parser
            timestamp = parser.parse(timestamp)
        
        # Make timestamp timezone-aware if it isn't
        if timestamp.tzinfo is None:
            from datetime import timezone
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        
        self.ticker_history[ticker].append(timestamp)
        
        # Keep only last 24 hours
        from datetime import timezone
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        self.ticker_history[ticker] = [
            ts for ts in self.ticker_history[ticker] if ts > cutoff
        ]
    
    def calculate_mention_velocity(self, ticker: str) -> Dict:
        """Calculate mention acceleration rate"""
        if ticker not in self.ticker_history:
            return {'velocity': 0, 'acceleration': 0}
        
        mentions = self.ticker_history[ticker]
        from datetime import timezone
        now = datetime.now(timezone.utc)
        
        # Last hour vs previous hour
        last_hour = sum(1 for ts in mentions if now - ts < timedelta(hours=1))
        prev_hour = sum(1 for ts in mentions if timedelta(hours=1) <= now - ts < timedelta(hours=2))
        
        velocity = last_hour
        acceleration = last_hour - prev_hour if prev_hour > 0 else 0
        
        return {
            'velocity': int(velocity),
            'acceleration': int(acceleration),
            'total_24h': int(len(mentions))
        }
    
    def calculate_hype_intensity(self, ticker: str, messages: List[Dict]) -> Dict:
        """
        🔴 Hype Intensity Score from RUMOR SOURCES (Telegram/Reddit)
        Combines: mention count, velocity, trigger density, sentiment spike
        OUTPUT: Risk score that must be validated against yfinance/NSE data
        """
        if not messages:
            return {'hype_score': 0, 'risk_level': 'low'}
        
        # 1. Mention count (normalized to 0-25)
        mention_count = len(messages)
        mention_score = min(25, mention_count)
        
        # 2. Message acceleration rate (0-25)
        velocity_data = self.calculate_mention_velocity(ticker)
        acceleration_score = min(25, velocity_data['acceleration'] * 5)
        
        # 3. Trigger density (0-25)
        total_triggers = sum(
            self.detect_fraud_triggers(msg.get('text', ''))['total_score']
            for msg in messages
        )
        trigger_score = min(25, total_triggers)
        
        # 4. Sentiment spike (0-25)
        sentiments = [self.calculate_sentiment(msg.get('text', '')) for msg in messages]
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        sentiment_score = abs(avg_sentiment) * 25  # Extreme sentiment = high hype
        
        # Total hype score (0-100)
        hype_score = mention_score + acceleration_score + trigger_score + sentiment_score
        
        # Risk level
        if hype_score >= 70:
            risk_level = 'critical'
        elif hype_score >= 50:
            risk_level = 'high'
        elif hype_score >= 30:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'hype_score': float(round(hype_score, 1)),
            'risk_level': risk_level,
            'breakdown': {
                'mention_score': float(round(mention_score, 1)),
                'acceleration_score': float(round(acceleration_score, 1)),
                'trigger_score': float(round(trigger_score, 1)),
                'sentiment_score': float(round(sentiment_score, 1))
            },
            'metrics': {
                'mention_count': int(mention_count),
                'velocity': int(velocity_data['velocity']),
                'acceleration': int(velocity_data['acceleration']),
                'avg_sentiment': float(round(avg_sentiment, 2)),
                'trigger_density': float(round(total_triggers / mention_count, 2)) if mention_count > 0 else 0.0
            }
        }
    
    def analyze_message(self, text: str, tickers: List[str], timestamp) -> Dict:
        """🔴 Analyze RUMOR SOURCE message (Telegram/Reddit) - UNTRUSTED"""
        # Vernacular detection (Hinglish/Hindi/Telugu/Tamil)
        vernacular_result = self.vernacular.detect_vernacular_fraud(text)
        
        # Normalize Hinglish
        normalized = self.normalize_hinglish(text)
        
        # Sentiment
        sentiment = self.calculate_sentiment(normalized)
        
        # Fraud triggers (original + vernacular)
        fraud_data = self.detect_fraud_triggers(normalized)
        total_fraud_score = fraud_data['total_score'] + vernacular_result['fraud_score']
        
        # Track tickers
        for ticker in tickers:
            self.track_ticker_mention(ticker, timestamp)
        
        return {
            'normalized_text': normalized,
            'sentiment_score': float(sentiment),
            'fraud_triggers': fraud_data['triggers'] + vernacular_result['detected_phrases'],
            'fraud_score': int(total_fraud_score),
            'sentiment_label': 'bullish' if sentiment > 0.2 else 'bearish' if sentiment < -0.2 else 'neutral',
            'vernacular_detection': vernacular_result,
            'vernacular_explanation': self.vernacular.get_fraud_explanation(vernacular_result)
        }
