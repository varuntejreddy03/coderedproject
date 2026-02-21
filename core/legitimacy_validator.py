"""
Legitimacy Validator - Validates Social Media Rumors Against Official Data

🔴 RUMOR SOURCES (Untrusted):
   - Telegram channels (pump & dump groups)
   - Reddit (IndianStockMarket, IndianStreetBets)

✅ VERIFICATION SOURCES (Trusted):
   - yfinance (Yahoo Finance official data)
   - NSE/BSE official filings
   - Corporate action announcements
   - Official news sources

Logic: If social hype is HIGH but official data is ZERO → LIKELY RUMOR
"""
import yfinance as yf
import requests
from datetime import datetime, timedelta
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class LegitimacyValidator:
    """
    Validates social media claims against official market data
    """
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = timedelta(minutes=10)
    
    def get_nse_filings(self, ticker: str) -> Dict:
        """✅ Check TRUSTED official NSE filings/announcements via yfinance"""
        try:
            stock = yf.Ticker(f"{ticker}.NS")
            info = stock.info
            news = stock.news[:5] if hasattr(stock, 'news') else []
            
            return {
                'has_recent_filings': len(news) > 0,
                'filing_count': len(news),
                'recent_news': [{'title': n.get('title', ''), 'publisher': n.get('publisher', '')} for n in news],
                'has_corporate_action': bool(info.get('dividendRate') or info.get('exDividendDate')),
                'official_news_sources': [n.get('publisher', '') for n in news if 'BSE' in n.get('publisher', '') or 'NSE' in n.get('publisher', '')]
            }
        except Exception as e:
            logger.error(f"Error fetching NSE filings for {ticker}: {e}")
            return {
                'has_recent_filings': False,
                'filing_count': 0,
                'recent_news': [],
                'has_corporate_action': False,
                'official_news_sources': []
            }
    
    def validate_price_claim(self, ticker: str, social_claim: str) -> Dict:
        """Validate if social media price claims match actual market movement"""
        try:
            stock = yf.Ticker(f"{ticker}.NS")
            hist = stock.history(period="5d")
            
            if hist.empty:
                return {'validated': False, 'reason': 'No market data'}
            
            price_change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
            
            # Check if social claim matches reality
            claim_lower = social_claim.lower()
            is_bullish_claim = any(word in claim_lower for word in ['moon', 'rocket', 'upper circuit', 'multibagger', 'target'])
            is_bearish_claim = any(word in claim_lower for word in ['crash', 'dump', 'fall', 'down'])
            
            validated = False
            if is_bullish_claim and price_change > 5:
                validated = True
            elif is_bearish_claim and price_change < -5:
                validated = True
            elif abs(price_change) < 2:
                validated = False  # No significant movement despite claims
            
            return {
                'validated': validated,
                'actual_change': float(round(price_change, 2)),
                'claim_type': 'bullish' if is_bullish_claim else 'bearish' if is_bearish_claim else 'neutral',
                'mismatch': not validated
            }
        except Exception as e:
            logger.error(f"Error validating price claim for {ticker}: {e}")
            return {'validated': False, 'reason': str(e)}
    
    def check_volume_legitimacy(self, ticker: str) -> Dict:
        """Check if volume spike is backed by official news"""
        try:
            stock = yf.Ticker(f"{ticker}.NS")
            hist = stock.history(period="3mo")
            
            if hist.empty or len(hist) < 20:
                return {'legitimate': False, 'reason': 'Insufficient data'}
            
            recent_volume = hist['Volume'].iloc[-1]
            avg_volume = hist['Volume'].iloc[:-1].mean()
            volume_spike = ((recent_volume - avg_volume) / avg_volume) * 100
            
            # Get filings
            filings = self.get_nse_filings(ticker)
            
            # Volume spike is legitimate if backed by official news
            legitimate = volume_spike > 100 and filings['has_recent_filings']
            
            return {
                'legitimate': legitimate,
                'volume_spike_percent': float(round(volume_spike, 2)),
                'backed_by_filings': filings['has_recent_filings'],
                'filing_count': filings['filing_count'],
                'suspicion_level': 'HIGH' if volume_spike > 200 and not filings['has_recent_filings'] else 'MEDIUM' if volume_spike > 100 else 'LOW'
            }
        except Exception as e:
            logger.error(f"Error checking volume legitimacy for {ticker}: {e}")
            return {'legitimate': False, 'reason': str(e)}
    
    def validate_social_vs_official(self, ticker: str, social_hype: float, social_sentiment: str) -> Dict:
        """
        ⛖️ Core Validation: RUMOR vs REALITY
        🔴 RUMOR: Social media hype from Telegram/Reddit (UNTRUSTED)
        ✅ VERIFICATION: Official market data from yfinance/NSE (TRUSTED)
        
        Returns legitimacy score (0-100)
        """
        filings = self.get_nse_filings(ticker)
        volume_check = self.check_volume_legitimacy(ticker)
        
        # Calculate legitimacy score
        legitimacy_score = 50  # Start neutral
        red_flags = []
        green_flags = []
        
        # Red Flag 1: High social hype (RUMOR) but NO official filings (REALITY)
        if social_hype > 70 and not filings['has_recent_filings']:
            legitimacy_score -= 30
            red_flags.append("🔴 High Telegram/Reddit hype with ZERO yfinance/NSE filings")
        
        # Red Flag 2: Volume spike without corporate action
        if volume_check.get('volume_spike_percent', 0) > 150 and not filings['has_corporate_action']:
            legitimacy_score -= 25
            red_flags.append("Unusual volume spike without corporate action")
        
        # Red Flag 3: No official news sources
        if not filings['official_news_sources']:
            legitimacy_score -= 15
            red_flags.append("No coverage from official news sources (BSE/NSE)")
        
        # Green Flag 1: Official filings present (TRUSTED SOURCE)
        if filings['has_recent_filings']:
            legitimacy_score += 20
            green_flags.append(f"✅ Official yfinance/NSE filings found ({filings['filing_count']} recent)")
        
        # Green Flag 2: Corporate action announced
        if filings['has_corporate_action']:
            legitimacy_score += 15
            green_flags.append("Corporate action announced (dividend/split)")
        
        # Green Flag 3: Covered by official sources
        if filings['official_news_sources']:
            legitimacy_score += 15
            green_flags.append("Covered by official sources")
        
        legitimacy_score = max(0, min(100, legitimacy_score))
        
        # Determine verdict
        if legitimacy_score >= 70:
            verdict = "LEGITIMATE"
            color = "GREEN"
        elif legitimacy_score >= 40:
            verdict = "UNCERTAIN"
            color = "AMBER"
        else:
            verdict = "LIKELY_RUMOR"
            color = "RED"
        
        return {
            'ticker': ticker,
            'legitimacy_score': int(legitimacy_score),
            'verdict': verdict,
            'color_indicator': color,
            'red_flags': red_flags,
            'green_flags': green_flags,
            'official_filings': filings,
            'volume_analysis': volume_check,
            'recommendation': self._generate_recommendation(verdict, red_flags)
        }
    
    def _generate_recommendation(self, verdict: str, red_flags: List[str]) -> str:
        """Generate actionable recommendation"""
        if verdict == "LEGITIMATE":
            return "✅ Social media activity backed by official data. Safe to investigate further."
        elif verdict == "UNCERTAIN":
            return "⚠️ Mixed signals. Verify with official NSE/BSE announcements before acting."
        else:
            return f"🚨 LIKELY RUMOR: {len(red_flags)} red flags detected. Avoid acting on social media claims alone."
