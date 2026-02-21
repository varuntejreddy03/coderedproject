"""
Alert Quality Controls - Reduce False Positives
Implements: Cooldowns, Confidence Scoring, Needs-Review State
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class AlertQualityControl:
    """Manages alert quality to reduce false positives"""
    
    def __init__(self, cooldown_minutes: int = 60):
        self.cooldown_period = timedelta(minutes=cooldown_minutes)
        self.alert_history = {}  # {ticker: last_alert_time}
        self.suppressed_count = defaultdict(int)
    
    def calculate_confidence(self, risk_breakdown: Dict) -> Dict:
        """
        Calculate confidence score based on signal agreement
        High confidence = all signals agree
        Low confidence = signals conflict
        """
        components = [
            risk_breakdown.get('social_hype_score', {}).get('value', 0),
            risk_breakdown.get('volume_anomaly', {}).get('value', 0),
            risk_breakdown.get('bot_coordination', {}).get('value', 0),
            risk_breakdown.get('sentiment_spike', {}).get('value', 0),
            risk_breakdown.get('lack_of_filings', {}).get('value', 0)
        ]
        
        # Classify each component
        high_signals = sum(1 for c in components if c >= 70)
        medium_signals = sum(1 for c in components if 40 <= c < 70)
        low_signals = sum(1 for c in components if c < 40)
        
        # Calculate confidence based on agreement
        if high_signals >= 4:
            confidence = 95  # Strong agreement on HIGH
        elif high_signals >= 3:
            confidence = 85  # Majority HIGH
        elif high_signals >= 2 and medium_signals >= 2:
            confidence = 70  # Mixed but leaning HIGH
        elif medium_signals >= 3:
            confidence = 55  # Moderate signals
        elif high_signals >= 1 and low_signals >= 3:
            confidence = 35  # Conflicting signals
        else:
            confidence = 50  # Default moderate
        
        return {
            'confidence_score': confidence,
            'signal_distribution': {
                'high': high_signals,
                'medium': medium_signals,
                'low': low_signals
            },
            'agreement_level': self._get_agreement_level(high_signals, medium_signals, low_signals)
        }
    
    def _get_agreement_level(self, high: int, medium: int, low: int) -> str:
        """Determine agreement level"""
        if high >= 4:
            return 'STRONG_AGREEMENT'
        elif high >= 3:
            return 'GOOD_AGREEMENT'
        elif high >= 1 and low >= 3:
            return 'CONFLICTING'
        else:
            return 'MODERATE'
    
    def should_alert(self, ticker: str, risk_score: float, confidence: int) -> Dict:
        """
        Determine if alert should be sent based on:
        1. Cooldown period
        2. Confidence threshold
        3. Risk score threshold
        
        Returns decision with state: ALERT / NEEDS_REVIEW / SUPPRESSED
        """
        now = datetime.now()
        
        # Check cooldown
        if ticker in self.alert_history:
            last_alert = self.alert_history[ticker]
            time_since_alert = now - last_alert
            
            if time_since_alert < self.cooldown_period:
                self.suppressed_count[ticker] += 1
                return {
                    'should_alert': False,
                    'state': 'SUPPRESSED',
                    'reason': f'Cooldown active ({int(time_since_alert.total_seconds() / 60)} min ago)',
                    'next_alert_in': int((self.cooldown_period - time_since_alert).total_seconds() / 60),
                    'suppressed_count': self.suppressed_count[ticker]
                }
        
        # Check confidence threshold
        if confidence < 50:
            return {
                'should_alert': False,
                'state': 'NEEDS_REVIEW',
                'reason': f'Low confidence ({confidence}%) - signals conflict',
                'recommendation': 'Manual review recommended'
            }
        
        # Check risk threshold
        if risk_score < 50:
            return {
                'should_alert': False,
                'state': 'LOW_RISK',
                'reason': f'Risk score below threshold ({risk_score}/100)'
            }
        
        # All checks passed - send alert
        self.alert_history[ticker] = now
        self.suppressed_count[ticker] = 0
        
        return {
            'should_alert': True,
            'state': 'ALERT',
            'reason': f'High risk ({risk_score}/100) with {confidence}% confidence',
            'confidence': confidence
        }
    
    def get_alert_status(self, ticker: str) -> Dict:
        """Get current alert status for ticker"""
        if ticker not in self.alert_history:
            return {
                'status': 'NEVER_ALERTED',
                'can_alert': True
            }
        
        now = datetime.now()
        last_alert = self.alert_history[ticker]
        time_since = now - last_alert
        
        if time_since < self.cooldown_period:
            return {
                'status': 'COOLDOWN',
                'can_alert': False,
                'last_alert': last_alert.isoformat(),
                'minutes_since': int(time_since.total_seconds() / 60),
                'next_alert_in': int((self.cooldown_period - time_since).total_seconds() / 60),
                'suppressed_count': self.suppressed_count[ticker]
            }
        else:
            return {
                'status': 'READY',
                'can_alert': True,
                'last_alert': last_alert.isoformat(),
                'minutes_since': int(time_since.total_seconds() / 60)
            }
    
    def reset_cooldown(self, ticker: str):
        """Manually reset cooldown for ticker"""
        if ticker in self.alert_history:
            del self.alert_history[ticker]
        self.suppressed_count[ticker] = 0
    
    def get_needs_review_list(self, all_analysis: List[Dict]) -> List[Dict]:
        """
        Get list of tickers that need manual review
        (conflicting signals, low confidence)
        """
        needs_review = []
        
        for analysis in all_analysis:
            ticker = analysis.get('ticker')
            risk_breakdown = analysis.get('risk_breakdown', {})
            
            confidence_data = self.calculate_confidence(risk_breakdown)
            
            if confidence_data['agreement_level'] == 'CONFLICTING':
                needs_review.append({
                    'ticker': ticker,
                    'risk_score': analysis.get('risk_score', 0),
                    'confidence': confidence_data['confidence_score'],
                    'reason': 'Conflicting signals detected',
                    'signal_distribution': confidence_data['signal_distribution']
                })
        
        return sorted(needs_review, key=lambda x: x['risk_score'], reverse=True)
    
    def get_statistics(self) -> Dict:
        """Get alert system statistics"""
        now = datetime.now()
        active_cooldowns = sum(
            1 for last_alert in self.alert_history.values()
            if now - last_alert < self.cooldown_period
        )
        
        total_suppressed = sum(self.suppressed_count.values())
        
        return {
            'total_tickers_alerted': len(self.alert_history),
            'active_cooldowns': active_cooldowns,
            'total_suppressed_alerts': total_suppressed,
            'cooldown_period_minutes': int(self.cooldown_period.total_seconds() / 60),
            'tickers_on_cooldown': [
                ticker for ticker, last_alert in self.alert_history.items()
                if now - last_alert < self.cooldown_period
            ]
        }

# Global instance
alert_controller = AlertQualityControl(cooldown_minutes=60)
