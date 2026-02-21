"""
Risk Score Calibration & Consistency
Defines clear weights and validates against known pump-and-dump cases
"""
from typing import Dict, List
import json

# Clear, tunable weights (must sum to 1.0)
RISK_WEIGHTS = {
    'social_hype': 0.30,        # Mentions, velocity, keyword intensity
    'coordination': 0.25,        # Bot patterns, cross-channel coordination
    'market_anomaly': 0.25,      # Volume spike, price manipulation
    'fundamentals_mismatch': 0.20  # No filings, news mismatch
}

# Known calibration cases (historical pump-and-dump + legitimate stocks)
CALIBRATION_CASES = [
    # Known pump-and-dump cases (should score HIGH)
    {
        'ticker': 'KNOWN_PUMP_1',
        'description': 'Telegram pump group coordinated attack',
        'expected_score_range': (80, 95),
        'components': {
            'social_hype': 90,
            'coordination': 85,
            'market_anomaly': 75,
            'fundamentals_mismatch': 90
        }
    },
    {
        'ticker': 'KNOWN_PUMP_2',
        'description': 'Penny stock manipulation with fake news',
        'expected_score_range': (75, 90),
        'components': {
            'social_hype': 80,
            'coordination': 70,
            'market_anomaly': 85,
            'fundamentals_mismatch': 80
        }
    },
    
    # Legitimate stocks (should score LOW)
    {
        'ticker': 'RELIANCE',
        'description': 'Blue chip with genuine news',
        'expected_score_range': (10, 30),
        'components': {
            'social_hype': 25,
            'coordination': 10,
            'market_anomaly': 20,
            'fundamentals_mismatch': 5
        }
    },
    {
        'ticker': 'TCS',
        'description': 'IT major with quarterly results',
        'expected_score_range': (5, 25),
        'components': {
            'social_hype': 20,
            'coordination': 5,
            'market_anomaly': 15,
            'fundamentals_mismatch': 10
        }
    },
    
    # Borderline cases (should score MEDIUM)
    {
        'ticker': 'BORDERLINE_1',
        'description': 'High social buzz but legitimate news',
        'expected_score_range': (40, 60),
        'components': {
            'social_hype': 60,
            'coordination': 30,
            'market_anomaly': 50,
            'fundamentals_mismatch': 20
        }
    }
]


class RiskCalibrator:
    """Calibrates and validates risk scoring consistency"""
    
    def __init__(self, weights: Dict = None):
        self.weights = weights or RISK_WEIGHTS
        self._validate_weights()
    
    def _validate_weights(self):
        """Ensure weights sum to 1.0"""
        total = sum(self.weights.values())
        if not (0.99 <= total <= 1.01):  # Allow small floating point error
            raise ValueError(f"Weights must sum to 1.0, got {total}")
    
    def calculate_calibrated_risk(self, components: Dict) -> Dict:
        """
        Calculate risk score using calibrated weights
        
        Args:
            components: {
                'social_hype': 0-100,
                'coordination': 0-100,
                'market_anomaly': 0-100,
                'fundamentals_mismatch': 0-100
            }
        
        Returns:
            {
                'risk_score': 0-100,
                'level': 'LOW'|'MEDIUM'|'HIGH'|'CRITICAL',
                'weighted_components': {...},
                'formula': 'explanation'
            }
        """
        # Calculate weighted score
        weighted_components = {}
        total_score = 0.0
        
        for component, weight in self.weights.items():
            component_score = components.get(component, 0)
            weighted_score = component_score * weight
            weighted_components[component] = {
                'raw_score': component_score,
                'weight': weight,
                'weighted_score': round(weighted_score, 2)
            }
            total_score += weighted_score
        
        # Determine risk level
        if total_score >= 75:
            level = 'CRITICAL'
            color = 'RED'
        elif total_score >= 50:
            level = 'HIGH'
            color = 'RED'
        elif total_score >= 30:
            level = 'MEDIUM'
            color = 'AMBER'
        else:
            level = 'LOW'
            color = 'GREEN'
        
        # Generate formula explanation
        formula = self._generate_formula(weighted_components)
        
        return {
            'risk_score': round(total_score, 1),
            'level': level,
            'color': color,
            'weighted_components': weighted_components,
            'formula': formula,
            'weights_used': self.weights
        }
    
    def _generate_formula(self, weighted_components: Dict) -> str:
        """Generate human-readable formula"""
        parts = []
        for component, data in weighted_components.items():
            parts.append(f"({data['weight']} × {data['raw_score']})")
        return " + ".join(parts) + f" = {sum(d['weighted_score'] for d in weighted_components.values()):.1f}"
    
    def validate_calibration(self) -> Dict:
        """
        Validate scoring against known cases
        Returns accuracy metrics
        """
        results = []
        correct = 0
        total = len(CALIBRATION_CASES)
        
        for case in CALIBRATION_CASES:
            calculated = self.calculate_calibrated_risk(case['components'])
            expected_min, expected_max = case['expected_score_range']
            actual_score = calculated['risk_score']
            
            is_correct = expected_min <= actual_score <= expected_max
            if is_correct:
                correct += 1
            
            results.append({
                'ticker': case['ticker'],
                'description': case['description'],
                'expected_range': case['expected_score_range'],
                'actual_score': actual_score,
                'is_correct': is_correct,
                'deviation': min(abs(actual_score - expected_min), abs(actual_score - expected_max))
            })
        
        accuracy = (correct / total) * 100 if total > 0 else 0
        
        return {
            'accuracy': round(accuracy, 1),
            'correct': correct,
            'total': total,
            'results': results,
            'weights_used': self.weights
        }
    
    def tune_weights(self, target_accuracy: float = 90.0, max_iterations: int = 100) -> Dict:
        """
        Auto-tune weights to achieve target accuracy
        Simple grid search approach
        """
        best_weights = self.weights.copy()
        best_accuracy = 0.0
        
        # Try small adjustments
        for _ in range(max_iterations):
            # Random small adjustment
            import random
            component = random.choice(list(self.weights.keys()))
            adjustment = random.uniform(-0.05, 0.05)
            
            # Create new weights
            new_weights = self.weights.copy()
            new_weights[component] += adjustment
            
            # Normalize to sum to 1.0
            total = sum(new_weights.values())
            new_weights = {k: v/total for k, v in new_weights.items()}
            
            # Test accuracy
            temp_calibrator = RiskCalibrator(new_weights)
            validation = temp_calibrator.validate_calibration()
            
            if validation['accuracy'] > best_accuracy:
                best_accuracy = validation['accuracy']
                best_weights = new_weights
                
                if best_accuracy >= target_accuracy:
                    break
        
        return {
            'best_weights': best_weights,
            'accuracy': best_accuracy,
            'iterations': _ + 1
        }
    
    def export_weights(self, filepath: str = 'risk_weights.json'):
        """Export current weights to file"""
        with open(filepath, 'w') as f:
            json.dump(self.weights, f, indent=2)
    
    def import_weights(self, filepath: str = 'risk_weights.json'):
        """Import weights from file"""
        with open(filepath, 'r') as f:
            self.weights = json.load(f)
        self._validate_weights()


# Global instance with default weights
risk_calibrator = RiskCalibrator()
