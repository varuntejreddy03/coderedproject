"""
Test Evidence-First Explainability
Demonstrates: Judge-friendly evidence cards with all supporting proof
"""
import sys
sys.path.append('..')

from core.evidence_builder import EvidenceBuilder
from datetime import datetime

def test_evidence_builder():
    builder = EvidenceBuilder()
    
    print("\n" + "="*80)
    print("EVIDENCE-FIRST EXPLAINABILITY - JUDGE-FRIENDLY OUTPUT")
    print("="*80)
    
    # SCENARIO 1: High-risk pump with all evidence
    print("\n" + "="*80)
    print("SCENARIO 1: High-Risk Pump Detection")
    print("="*80)
    
    high_risk_data = {
        'ticker': 'RELIANCE',
        'risk_score': 82,
        'social_activity': {
            'telegram': {
                'mention_count': 47,
                'keywords': ['Upper Circuit Pakka', 'Target 5x', 'Operator Game']
            },
            'reddit': {
                'mention_count': 12
            }
        },
        'mention_burst': {
            'burst_detected': True,
            'velocity_multiplier': 12.0,
            'baseline_rate': 2.0,
            'current_rate': 24
        },
        'market_data': {
            'z_score': 4.3,
            'volume': 4300000,
            'avg_volume': 1000000
        },
        'bot_activity': {
            'bot_activity_detected': True,
            'confidence': 68,
            'indicators': ['Copy-paste detected', 'Cross-channel coordination']
        },
        'vernacular_detection': {
            'transliteration_detected': True,
            'language': 'Hindi',
            'detected_phrases': ['upar circuit pakka', 'buy karo jaldi']
        },
        'legitimacy': {
            'verdict': 'LIKELY_RUMOR'
        },
        'risk_breakdown': {
            'bot_coordination': {'value': 68}
        }
    }
    
    evidence = builder.build_evidence_card('RELIANCE', high_risk_data)
    
    print(f"\nTicker: {evidence['ticker']}")
    print(f"Risk Score: {evidence['risk_score']}/100")
    print(f"Verdict: {evidence['verdict']}")
    print(f"\nProof Summary: {evidence['proof_summary']}")
    
    print(f"\nEVIDENCE ({len(evidence['evidence_items'])} items):")
    print("-" * 80)
    
    for item in evidence['evidence_items']:
        severity_color = {
            'critical': 'RED',
            'high': 'ORANGE',
            'medium': 'YELLOW',
            'low': 'GREEN'
        }.get(item['severity'], 'GRAY')
        
        print(f"\n{item['icon']} {item['label']} [{severity_color}]")
        print(f"   {item['value']}")
    
    # SCENARIO 2: Medium-risk with partial evidence
    print("\n\n" + "="*80)
    print("SCENARIO 2: Medium-Risk Detection")
    print("="*80)
    
    medium_risk_data = {
        'ticker': 'TATA',
        'risk_score': 55,
        'social_activity': {
            'telegram': {
                'mention_count': 15,
                'keywords': ['Target', 'Breakout']
            }
        },
        'market_data': {
            'z_score': 2.1,
            'volume': 2100000,
            'avg_volume': 1000000
        },
        'legitimacy': {
            'verdict': 'UNCERTAIN'
        }
    }
    
    evidence = builder.build_evidence_card('TATA', medium_risk_data)
    
    print(f"\nTicker: {evidence['ticker']}")
    print(f"Risk Score: {evidence['risk_score']}/100")
    print(f"Verdict: {evidence['verdict']}")
    print(f"\nProof Summary: {evidence['proof_summary']}")
    
    print(f"\nEVIDENCE ({len(evidence['evidence_items'])} items):")
    print("-" * 80)
    
    for item in evidence['evidence_items']:
        print(f"\n{item['icon']} {item['label']} [{item['severity'].upper()}]")
        print(f"   {item['value']}")
    
    # SCENARIO 3: Low-risk (legitimate)
    print("\n\n" + "="*80)
    print("SCENARIO 3: Low-Risk (Legitimate Activity)")
    print("="*80)
    
    low_risk_data = {
        'ticker': 'TCS',
        'risk_score': 25,
        'social_activity': {
            'telegram': {
                'mention_count': 5,
                'keywords': []
            }
        },
        'market_data': {
            'z_score': 0.8,
            'volume': 1080000,
            'avg_volume': 1000000
        },
        'legitimacy': {
            'verdict': 'LEGITIMATE'
        }
    }
    
    evidence = builder.build_evidence_card('TCS', low_risk_data)
    
    print(f"\nTicker: {evidence['ticker']}")
    print(f"Risk Score: {evidence['risk_score']}/100")
    print(f"Verdict: {evidence['verdict']}")
    print(f"\nProof Summary: {evidence['proof_summary']}")
    
    print(f"\nEVIDENCE ({len(evidence['evidence_items'])} items):")
    print("-" * 80)
    
    for item in evidence['evidence_items']:
        print(f"\n{item['icon']} {item['label']} [{item['severity'].upper()}]")
        print(f"   {item['value']}")
    
    # Summary
    print("\n\n" + "="*80)
    print("KEY BENEFITS FOR JUDGES")
    print("="*80)
    print("\n1. TRANSPARENT: Shows exactly WHY stock was flagged")
    print("2. EVIDENCE-BASED: Every claim backed by concrete data")
    print("3. STRUCTURED: Easy to understand severity levels")
    print("4. COMPREHENSIVE: Covers all detection dimensions")
    print("5. DEFENSIBLE: Can explain to regulators/users")
    print("\n" + "="*80)
    print("\nJudge Question: 'Why is RELIANCE risky?'")
    print("Your Answer: [Shows evidence card with 7 proof points]")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_evidence_builder()
