"""
Market Data Integration - Reality Check Logic

🔴 RUMOR SOURCES (Untrusted):
   - Telegram pump groups
   - Reddit speculation

✅ VERIFICATION SOURCES (Trusted):
   - yfinance (Yahoo Finance)
   - Official market data (NSE/BSE)
   - Volume & price data
   - Market cap & liquidity metrics

Compares social hype with actual market fundamentals
If hype is HIGH but fundamentals are ZERO → RED FLAG
"""
import yfinance as yf
import logging
from typing import Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MarketDataChecker:
    """
    Reality Check: Social Hype vs Market Fundamentals
    If hype is HIGH but fundamentals are ZERO → RED FLAG
    """
    
    def __init__(self):
        # Cache to avoid repeated API calls
        self.cache = {}
        self.cache_ttl = timedelta(minutes=5)
    
    def get_stock_fundamentals(self, symbol: str) -> Dict:
        """✅ Get TRUSTED official market data from yfinance for reality check"""
        # Check cache first
        if symbol in self.cache:
            cached_data, cached_time = self.cache[symbol]
            if datetime.now() - cached_time < self.cache_ttl:
                return cached_data
        
        try:
            # Add .NS for NSE stocks
            ticker_symbol = f"{symbol}.NS" if not symbol.endswith('.NS') else symbol
            stock = yf.Ticker(ticker_symbol)
            
            # Get info (fast method)
            info = stock.info
            hist = stock.history(period="1d")
            
            result = {
                'has_official_news': bool(info.get('longName')),
                'market_cap': float(info.get('marketCap', 0) / 10000000),  # Convert to crores
                'volume': int(hist['Volume'].iloc[-1]) if not hist.empty else 0,
                'price_change': float(info.get('regularMarketChangePercent', 0)),
                'is_liquid': bool((hist['Volume'].iloc[-1] if not hist.empty else 0) > 100000)
            }
            
            # Cache the result
            self.cache[symbol] = (result, datetime.now())
            return result
            
        except Exception as e:
            logger.error(f"Error fetching market data for {symbol}: {e}")
        
        return {
            'has_official_news': False,
            'market_cap': 0,
            'volume': 0,
            'price_change': 0,
            'is_liquid': False
        }
    
    def reality_check(self, ticker: str, social_hype: float, fraud_score: int) -> Dict:
        """
        ⛖️ Core Reality Check Logic
        🔴 RUMOR: Social Hype from Telegram/Reddit (UNTRUSTED)
        ✅ VERIFICATION: Official data from yfinance (TRUSTED)
        
        If Social Hype HIGH + Official News ZERO = RED FLAG
        """
        fundamentals = self.get_stock_fundamentals(ticker)
        
        # Calculate risk level
        risk_factors = []
        risk_score = 0
        
        # Factor 1: High hype but no official news (RUMOR vs REALITY)
        if social_hype > 60 and not fundamentals['has_official_news']:
            risk_factors.append("🔴 High social hype (Telegram/Reddit) with NO official news (yfinance)")
            risk_score += 30
        
        # Factor 2: Low liquidity (easy to manipulate)
        if not fundamentals['is_liquid']:
            risk_factors.append("Low liquidity - easy to manipulate")
            risk_score += 20
        
        # Factor 3: Small market cap (penny stock)
        if fundamentals['market_cap'] < 500:  # < 500 crore
            risk_factors.append("Small market cap (penny stock)")
            risk_score += 20
        
        # Factor 4: High fraud signals
        if fraud_score >= 5:
            risk_factors.append(f"High fraud score ({fraud_score})")
            risk_score += 30
        
        # Determine safety indicator
        if risk_score >= 70:
            safety = "RED"
            risk_level = "CRITICAL"
        elif risk_score >= 50:
            safety = "AMBER"
            risk_level = "HIGH"
        elif risk_score >= 30:
            safety = "AMBER"
            risk_level = "MEDIUM"
        else:
            safety = "GREEN"
            risk_level = "LOW"
        
        # Generate "Why" explanation
        if risk_factors:
            why_explanation = f"⚠️ Risk detected: {', '.join(risk_factors)}"
        else:
            why_explanation = "✅ No significant risk factors detected"
        
        return {
            'ticker': ticker,
            'safety_indicator': safety,
            'risk_level': risk_level,
            'risk_score': int(risk_score),
            'why_explanation': why_explanation,
            'risk_factors': risk_factors,
            'social_hype': float(social_hype),
            'fraud_score': int(fraud_score),
            'fundamentals': fundamentals,
            'timestamp': datetime.now().isoformat()
        }


# Example usage
if __name__ == "__main__":
    checker = MarketDataChecker()
    
    # Test case: High hype penny stock
    result = checker.reality_check(
        ticker="YESBANK",
        social_hype=85,  # High hype
        fraud_score=7    # High fraud signals
    )
    
    print(f"Safety: {result['safety_indicator']}")
    print(f"Risk: {result['risk_level']}")
    print(f"Why: {result['why_explanation']}")
