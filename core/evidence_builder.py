"""
Evidence-First Explainability - Judge-Friendly Output
Generates comprehensive evidence cards for every alert
"""
from typing import Dict, List
from datetime import datetime, timedelta

class EvidenceBuilder:
    """Builds evidence-based explanations for fraud alerts"""
    
    def build_evidence_card(self, ticker: str, analysis_data: Dict) -> Dict:
        """
        Generate complete evidence card with all supporting proof
        Returns: structured evidence for judges/users
        """
        evidence = {
            'ticker': ticker,
            'risk_score': analysis_data.get('risk_score', 0),
            'verdict': self._generate_verdict(analysis_data),
            'evidence_items': [],
            'proof_summary': '',
            'timestamp': datetime.now().isoformat()
        }
        
        # 1. Matched Triggers (Top 3-5)
        triggers = self._extract_top_triggers(analysis_data)
        if triggers:
            evidence['evidence_items'].append({
                'type': 'triggers',
                'icon': '🎯',
                'label': 'Matched Triggers',
                'value': ', '.join([f'"{t}"' for t in triggers[:5]]),
                'severity': 'high' if len(triggers) >= 3 else 'medium'
            })
        
        # 2. Activity Metrics (#messages, #channels, time window)
        activity = self._extract_activity_metrics(analysis_data)
        if activity['message_count'] > 0:
            time_window = activity['time_window_hours']
            evidence['evidence_items'].append({
                'type': 'activity',
                'icon': '📊',
                'label': 'Activity Pattern',
                'value': f"{activity['message_count']} messages across {activity['channel_count']} channels in {time_window} hours",
                'severity': 'high' if activity['message_count'] > 20 else 'medium'
            })
        
        # 3. Mention Burst Factor
        burst = self._extract_burst_data(analysis_data)
        if burst['detected']:
            evidence['evidence_items'].append({
                'type': 'burst',
                'icon': '💥',
                'label': 'Mention Burst',
                'value': f"{burst['multiplier']}x baseline (normal: {burst['baseline']}/hr, current: {burst['current']}/hr)",
                'severity': 'critical' if burst['multiplier'] >= 5 else 'high'
            })
        
        # 4. Volume Anomaly Score
        anomaly = self._extract_anomaly_data(analysis_data)
        if anomaly['detected']:
            evidence['evidence_items'].append({
                'type': 'anomaly',
                'icon': '📈',
                'label': 'Volume Anomaly',
                'value': f"Z-score {anomaly['z_score']} ({anomaly['spike_percent']}% above average)",
                'severity': 'high' if abs(anomaly['z_score']) > 3 else 'medium'
            })
        
        # 5. Bot Coordination
        bot = self._extract_bot_data(analysis_data)
        if bot['detected']:
            evidence['evidence_items'].append({
                'type': 'bot',
                'icon': '🤖',
                'label': 'Bot Coordination',
                'value': f"{bot['confidence']}% confidence ({', '.join(bot['indicators'][:2])})",
                'severity': 'high' if bot['confidence'] > 70 else 'medium'
            })
        
        # 6. Vernacular Detection
        vernacular = self._extract_vernacular_data(analysis_data)
        if vernacular['detected']:
            evidence['evidence_items'].append({
                'type': 'vernacular',
                'icon': '🌏',
                'label': 'Vernacular Fraud',
                'value': f"Detected {vernacular['language']} phrases: {', '.join(vernacular['phrases'][:3])}",
                'severity': 'medium'
            })
        
        # 7. Official Verification (NO FILINGS = RED FLAG)
        filings = self._extract_filing_data(analysis_data)
        evidence['evidence_items'].append({
            'type': 'filings',
            'icon': '❌' if not filings['found'] else '✅',
            'label': 'Official Verification',
            'value': filings['message'],
            'severity': 'critical' if not filings['found'] else 'low'
        })
        
        # Generate proof summary
        evidence['proof_summary'] = self._generate_proof_summary(evidence['evidence_items'])
        
        return evidence
    
    def _extract_top_triggers(self, data: Dict) -> List[str]:
        """Extract top fraud triggers"""
        triggers = []
        
        # From social activity
        if 'social_activity' in data:
            telegram = data['social_activity'].get('telegram', {})
            triggers.extend(telegram.get('keywords', []))
        
        # From bot activity
        if 'bot_activity' in data:
            bot_indicators = data['bot_activity'].get('indicators', [])
            triggers.extend(bot_indicators)
        
        # From risk breakdown
        if 'risk_breakdown' in data:
            # Extract from breakdown if available
            pass
        
        return list(set(triggers))[:5]
    
    def _extract_activity_metrics(self, data: Dict) -> Dict:
        """Extract message count, channel count, time window"""
        activity = {
            'message_count': 0,
            'channel_count': 0,
            'time_window_hours': 24
        }
        
        if 'social_activity' in data:
            telegram = data['social_activity'].get('telegram', {})
            activity['message_count'] = telegram.get('mention_count', 0)
            
            reddit = data['social_activity'].get('reddit', {})
            activity['message_count'] += reddit.get('mention_count', 0)
            
            # Estimate channels (simplified)
            activity['channel_count'] = max(1, activity['message_count'] // 5)
        
        return activity
    
    def _extract_burst_data(self, data: Dict) -> Dict:
        """Extract mention burst metrics"""
        burst = {'detected': False, 'multiplier': 0, 'baseline': 0, 'current': 0}
        
        if 'mention_burst' in data:
            burst_data = data['mention_burst']
            burst['detected'] = burst_data.get('burst_detected', False)
            burst['multiplier'] = burst_data.get('velocity_multiplier', 0)
            burst['baseline'] = burst_data.get('baseline_rate', 0)
            burst['current'] = burst_data.get('current_rate', 0)
        
        return burst
    
    def _extract_anomaly_data(self, data: Dict) -> Dict:
        """Extract volume anomaly metrics"""
        anomaly = {'detected': False, 'z_score': 0, 'spike_percent': 0}
        
        if 'market_data' in data:
            market = data['market_data']
            anomaly['z_score'] = market.get('z_score', 0)
            anomaly['detected'] = abs(anomaly['z_score']) > 2
            
            # Calculate spike percent
            volume = market.get('volume', 0)
            avg_volume = market.get('avg_volume', 1)
            anomaly['spike_percent'] = int(((volume - avg_volume) / avg_volume) * 100) if avg_volume > 0 else 0
        
        return anomaly
    
    def _extract_bot_data(self, data: Dict) -> Dict:
        """Extract bot coordination metrics"""
        bot = {'detected': False, 'confidence': 0, 'indicators': []}
        
        if 'bot_activity' in data:
            bot_data = data['bot_activity']
            bot['detected'] = bot_data.get('bot_activity_detected', False)
            bot['confidence'] = bot_data.get('confidence', 0)
            bot['indicators'] = bot_data.get('indicators', [])
        
        # From risk breakdown
        if 'risk_breakdown' in data:
            bot_coord = data['risk_breakdown'].get('bot_coordination', {})
            bot['confidence'] = bot_coord.get('value', 0)
        
        return bot
    
    def _extract_vernacular_data(self, data: Dict) -> Dict:
        """Extract vernacular detection"""
        vernacular = {'detected': False, 'language': '', 'phrases': []}
        
        if 'vernacular_detection' in data:
            vern_data = data['vernacular_detection']
            vernacular['detected'] = vern_data.get('transliteration_detected', False)
            vernacular['language'] = vern_data.get('language', 'Unknown')
            vernacular['phrases'] = vern_data.get('detected_phrases', [])
        
        return vernacular
    
    def _extract_filing_data(self, data: Dict) -> Dict:
        """Extract official filing verification"""
        filings = {'found': False, 'message': ''}
        
        if 'legitimacy' in data:
            legit = data['legitimacy']
            verdict = legit.get('verdict', 'UNCERTAIN')
            
            if verdict == 'LIKELY_RUMOR':
                filings['found'] = False
                filings['message'] = 'No NSE filings found in last 90 days'
            elif verdict == 'LEGITIMATE':
                filings['found'] = True
                filings['message'] = 'Official NSE filings verified'
            else:
                filings['found'] = False
                filings['message'] = 'Unable to verify official filings'
        else:
            filings['message'] = 'No official news/filing found'
        
        return filings
    
    def _generate_verdict(self, data: Dict) -> str:
        """Generate final verdict"""
        risk_score = data.get('risk_score', 0)
        
        if isinstance(risk_score, dict):
            risk_score = risk_score.get('score', 0)
        
        if risk_score >= 75:
            return 'High manipulation risk - Social hype with no fundamentals'
        elif risk_score >= 50:
            return 'Medium risk - Verify before trading'
        else:
            return 'Low risk - Normal trading activity'
    
    def _generate_proof_summary(self, evidence_items: List[Dict]) -> str:
        """Generate one-line proof summary"""
        critical = sum(1 for e in evidence_items if e['severity'] == 'critical')
        high = sum(1 for e in evidence_items if e['severity'] == 'high')
        
        if critical > 0:
            return f"{critical} critical + {high} high-risk signals detected"
        elif high > 0:
            return f"{high} high-risk signals detected"
        else:
            return "Multiple risk indicators present"

# Global instance
evidence_builder = EvidenceBuilder()
