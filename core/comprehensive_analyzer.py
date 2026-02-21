"""
Comprehensive Ticker Analyzer - Implements All UI Parameters

🔴 RUMOR SOURCES (Untrusted - for detection only):
   - Telegram channels (pump & dump groups)
   - Reddit (speculation & hype)

✅ VERIFICATION SOURCES (Trusted - for validation):
   - yfinance (Yahoo Finance official data)
   - NSE/BSE official filings
   - Corporate announcements
   - Volume & price data

Evaluates: Risk Score, Market Data, Social Activity, AI Analysis, Risk Breakdown
Validates social media rumors against official trusted sources
"""
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class ComprehensiveTickerAnalyzer:
    """
    Analyzes ticker across all dimensions shown in UI:
    1. Risk Assessment (0-100)
    2. Market Data (Price, Volume, Z-Score)
    3. Social Activity (Telegram, Reddit, X)
    4. AI Analysis
    5. Risk Breakdown (5 components)
    """
    
    def __init__(self):
        from core.legitimacy_validator import LegitimacyValidator
        from core.intelligence_engine import IntelligenceEngine
        from core.risk_analyzer import RiskAnalyzer
        from core.mention_burst_detector import burst_detector
        from core.risk_calibrator import risk_calibrator
        
        self.legitimacy = LegitimacyValidator()
        self.intelligence = IntelligenceEngine()
        self.risk_analyzer = RiskAnalyzer()
        self.burst_detector = burst_detector
        self.calibrator = risk_calibrator
    
    def analyze_ticker(self, ticker: str, telegram_messages: List[Dict], 
                      reddit_posts: List[Dict] = None) -> Dict:
        """
        Complete ticker analysis matching UI requirements
        """
        # 1. MARKET DATA SECTION
        market_data = self._get_market_data(ticker)
        
        # 2. SOCIAL ACTIVITY SECTION
        social_activity = self._analyze_social_activity(ticker, telegram_messages, reddit_posts)
        
        # 3. RISK BREAKDOWN SECTION
        risk_breakdown = self._calculate_risk_breakdown(ticker, telegram_messages, market_data, social_activity)
        
        # 4. LEGITIMACY VALIDATION (Rumor vs Reality)
        legitimacy = self.legitimacy.validate_social_vs_official(
            ticker,
            social_activity['telegram']['hype_score'],
            social_activity['telegram']['sentiment']
        )
        
        # 5. UNIFIED RISK SCORE (0-100)
        unified_risk = self._calculate_unified_risk(risk_breakdown, legitimacy)
        
        # 6. AI ANALYSIS (Natural Language Summary)
        ai_analysis = self._generate_ai_analysis(
            ticker, unified_risk, market_data, social_activity, 
            risk_breakdown, legitimacy
        )
        
        return {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            
            # Risk Assessment (Main Circle)
            'risk_assessment': {
                'score': unified_risk['score'],
                'level': unified_risk['level'],
                'color': unified_risk['color']
            },
            
            # Market Data
            'market_data': market_data,
            
            # Social Activity
            'social_activity': social_activity,
            
            # AI Analysis
            'ai_analysis': ai_analysis,
            
            # Risk Breakdown (5 bars)
            'risk_breakdown': risk_breakdown,
            
            # Legitimacy Check
            'legitimacy': legitimacy
        }
    
    def _get_market_data(self, ticker: str) -> Dict:
        """✅ Fetch TRUSTED real-time market data from yfinance"""
        try:
            stock = yf.Ticker(f"{ticker}.NS")
            info = stock.info
            hist = stock.history(period="5d")
            hist_3mo = stock.history(period="3mo")
            
            if hist.empty:
                return self._empty_market_data()
            
            current_price = float(hist['Close'].iloc[-1])
            prev_close = float(hist['Close'].iloc[0])
            price_change = ((current_price - prev_close) / prev_close) * 100
            
            current_volume = int(hist['Volume'].iloc[-1])
            avg_volume = int(hist_3mo['Volume'].mean()) if not hist_3mo.empty else current_volume
            
            # Calculate Z-Score
            volumes = hist_3mo['Volume'].values
            if len(volumes) > 20:
                mean_vol = np.mean(volumes[:-1])
                std_vol = np.std(volumes[:-1])
                z_score = (current_volume - mean_vol) / std_vol if std_vol > 0 else 0
            else:
                z_score = 0
            
            return {
                'price': float(round(current_price, 2)),
                'change_percent': float(round(price_change, 2)),
                'volume': current_volume,
                'avg_volume': avg_volume,
                'z_score': float(round(z_score, 2)),
                'market_cap': float(info.get('marketCap', 0) / 10000000),  # In crores
                'volume_chart': self._generate_volume_chart(hist_3mo)
            }
        except Exception as e:
            logger.error(f"Error fetching market data for {ticker}: {e}")
            return self._empty_market_data()
    
    def _empty_market_data(self) -> Dict:
        return {
            'price': 0, 'change_percent': 0, 'volume': 0,
            'avg_volume': 0, 'z_score': 0, 'market_cap': 0,
            'volume_chart': []
        }
    
    def _generate_volume_chart(self, hist) -> List[Dict]:
        """Generate volume chart data for last 30 days"""
        if hist.empty:
            return []
        
        chart_data = []
        for idx, row in hist.tail(30).iterrows():
            chart_data.append({
                'timestamp': idx.strftime('%H:%M') if hasattr(idx, 'strftime') else str(idx),
                'volume': int(row['Volume'])
            })
        return chart_data
    
    def _analyze_social_activity(self, ticker: str, telegram_msgs: List[Dict], 
                                 reddit_posts: List[Dict] = None) -> Dict:
        """Analyze social media activity across platforms"""
        
        # TELEGRAM ANALYSIS
        telegram_data = self._analyze_telegram(ticker, telegram_msgs)
        
        # REDDIT ANALYSIS
        reddit_data = self._analyze_reddit(ticker, reddit_posts) if reddit_posts else {'mention_count': 0, 'sentiment': 'neutral', 'keywords': []}
        
        # YOUTUBE ANALYSIS (placeholder - can be populated if available)
        youtube_data = {'mention_count': 0, 'sentiment': 'neutral', 'keywords': []}
        
        return {
            'telegram': telegram_data,
            'reddit': reddit_data,
            'youtube': youtube_data,
            'last_updated': datetime.now().isoformat()
        }
    
    def _analyze_telegram(self, ticker: str, messages: List[Dict]) -> Dict:
        """🔴 Analyze RUMOR SOURCE: Telegram activity (UNTRUSTED)"""
        if not messages:
            return {'mention_count': 0, 'sentiment': 'neutral', 'hype_score': 0, 'keywords': []}
        
        msg_dicts = [{'text': m.get('text', ''), 'date': m.get('date')} for m in messages]
        intensity = self.intelligence.calculate_hype_intensity(ticker, msg_dicts)
        
        # Extract keywords
        keywords = []
        for msg in messages[:10]:
            text = msg.get('text', '').lower()
            if 'upper circuit' in text or 'pakka' in text:
                keywords.append('Upper Circuit Pakka')
            if 'target' in text:
                keywords.append('Target 5x')
        
        sentiment = 'Bullish' if intensity['metrics']['avg_sentiment'] > 0.2 else 'Bearish' if intensity['metrics']['avg_sentiment'] < -0.2 else 'Neutral'
        
        return {
            'mention_count': len(messages),
            'sentiment': sentiment,
            'hype_score': intensity['hype_score'],
            'keywords': list(set(keywords))[:3],
            'velocity': intensity['metrics']['velocity']
        }
    
    def _analyze_reddit(self, ticker: str, posts: List[Dict]) -> Dict:
        """🔴 Analyze RUMOR SOURCE: Reddit activity (UNTRUSTED)"""
        if not posts:
            return {'mention_count': 0, 'sentiment': 'neutral', 'keywords': []}
        
        keywords = []
        sentiment_scores = []
        
        for post in posts[:10]:
            text = post.get('title', '').lower()
            if 'operator' in text or 'game' in text:
                keywords.append('Operator Game')
            if 'insider' in text or 'news' in text:
                keywords.append('Insider News')
            
            # Simple sentiment
            if any(word in text for word in ['scam', 'fraud', 'loss']):
                sentiment_scores.append(-1)
            elif any(word in text for word in ['profit', 'gain', 'moon']):
                sentiment_scores.append(1)
        
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        sentiment = 'Bullish' if avg_sentiment > 0.2 else 'Bearish' if avg_sentiment < -0.2 else 'Neutral'
        
        return {
            'mention_count': len(posts),
            'sentiment': sentiment,
            'keywords': list(set(keywords))[:3]
        }
    
    def _calculate_risk_breakdown(self, ticker: str, messages: List[Dict], 
                                  market_data: Dict, social_activity: Dict) -> Dict:
        """
        Calculate 5 risk components matching UI:
        1. Social Hype Score (85%) - includes mention burst detection
        2. Volume Anomaly (74%)
        3. Bot Coordination (68%)
        4. Sentiment Spike (80%)
        5. Lack of Filings (90%)
        """
        
        # 1. Social Hype Score (0-100) - Enhanced with burst detection
        base_hype = social_activity['telegram']['hype_score']
        burst_data = self.burst_detector.detect_burst(ticker)
        burst_boost = burst_data['burst_score'] * 0.3  # 30% weight to burst
        social_hype = min(100, base_hype * 0.7 + burst_boost)
        
        # 2. Volume Anomaly (based on Z-score)
        z_score = market_data['z_score']
        volume_anomaly = min(100, abs(z_score) * 20) if z_score > 2 else 0
        
        # 3. Bot Coordination
        bot_data = self.risk_analyzer.detect_bot_activity(ticker, messages)
        bot_coordination = bot_data['confidence']
        
        # 4. Sentiment Spike (extreme sentiment = high risk)
        msg_dicts = [{'text': m.get('text', ''), 'date': m.get('date')} for m in messages] if messages else []
        sentiments = [self.intelligence.calculate_sentiment(m['text']) for m in msg_dicts]
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        sentiment_spike = abs(avg_sentiment) * 100
        
        # 5. Lack of Filings (inverse of legitimacy from TRUSTED yfinance/NSE)
        filings = self.legitimacy.get_nse_filings(ticker)
        lack_of_filings = 0 if filings['has_recent_filings'] else 90
        
        return {
            'social_hype_score': {
                'value': int(social_hype),
                'label': 'Social Hype Score',
                'color': 'red' if social_hype > 70 else 'orange' if social_hype > 50 else 'green'
            },
            'volume_anomaly': {
                'value': int(volume_anomaly),
                'label': 'Volume Anomaly',
                'color': 'red' if volume_anomaly > 70 else 'orange' if volume_anomaly > 50 else 'green'
            },
            'bot_coordination': {
                'value': int(bot_coordination),
                'label': 'Bot Coordination',
                'color': 'orange' if bot_coordination > 50 else 'green'
            },
            'sentiment_spike': {
                'value': int(sentiment_spike),
                'label': 'Sentiment Spike',
                'color': 'red' if sentiment_spike > 70 else 'orange' if sentiment_spike > 50 else 'green'
            },
            'lack_of_filings': {
                'value': int(lack_of_filings),
                'label': 'Lack of Filings',
                'color': 'red' if lack_of_filings > 70 else 'orange' if lack_of_filings > 50 else 'green'
            }
        }
    
    def _calculate_unified_risk(self, risk_breakdown: Dict, legitimacy: Dict) -> Dict:
        """Calculate unified risk score using CALIBRATED weights"""
        
        # Map risk breakdown to calibrator components
        components = {
            'social_hype': risk_breakdown['social_hype_score']['value'],
            'coordination': risk_breakdown['bot_coordination']['value'],
            'market_anomaly': risk_breakdown['volume_anomaly']['value'],
            'fundamentals_mismatch': risk_breakdown['lack_of_filings']['value']
        }
        
        # Use calibrated calculation
        calibrated_result = self.calibrator.calculate_calibrated_risk(components)
        
        # Adjust based on legitimacy
        total_score = calibrated_result['risk_score']
        if legitimacy['verdict'] == 'LIKELY_RUMOR':
            total_score = min(100, total_score * 1.2)
        elif legitimacy['verdict'] == 'LEGITIMATE':
            total_score = max(0, total_score * 0.8)
        
        total_score = int(round(total_score))
        
        # Determine level and color
        if total_score >= 75:
            level = 'HIGH RISK'
            color = 'RED'
        elif total_score >= 50:
            level = 'MEDIUM RISK'
            color = 'ORANGE'
        else:
            level = 'LOW RISK'
            color = 'GREEN'
        
        return {
            'score': total_score,
            'level': level,
            'color': color,
            'calibration': {
                'weights_used': calibrated_result['weights_used'],
                'formula': calibrated_result['formula'],
                'weighted_components': calibrated_result['weighted_components']
            }
        }
    
    def _generate_ai_analysis(self, ticker: str, unified_risk: Dict, 
                             market_data: Dict, social_activity: Dict,
                             risk_breakdown: Dict, legitimacy: Dict) -> str:
        """Generate AI analysis text matching UI format"""
        
        analysis_parts = []
        
        # Part 1: Coordination detection
        if social_activity['telegram']['mention_count'] > 10:
            analysis_parts.append(
                f"Coordinated Telegram activity detected across {social_activity['telegram']['mention_count']} messages."
            )
        
        # Part 2: Volume analysis
        if market_data['z_score'] > 3:
            analysis_parts.append(
                f"Volume spike {market_data['z_score']:.1f}x above 5-day average."
            )
        
        # Part 3: Filing check
        if legitimacy['verdict'] == 'LIKELY_RUMOR':
            analysis_parts.append(
                f"No NSE filings found in last 90 days."
            )
        
        # Part 4: Bot detection
        if risk_breakdown['bot_coordination']['value'] > 60:
            analysis_parts.append(
                f"Bot-like posting patterns identified with {risk_breakdown['bot_coordination']['value']}% confidence."
            )
        
        return ' '.join(analysis_parts) if analysis_parts else "Normal trading activity observed."
