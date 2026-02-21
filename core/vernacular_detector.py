"""
Vernacular & Hinglish Fraud Detection
Detects pump-and-dump phrases in Hindi, Telugu, Tamil, and transliteration variants
"""
from typing import Dict, List, Tuple
import re

try:
    from langdetect import detect, LangDetectException
except ImportError:
    detect = None
    LangDetectException = Exception

class VernacularDetector:
    def __init__(self):
        # Transliteration variants (same phrase, different spellings)
        self.transliteration_map = {
            # Upper Circuit variants
            'upper_circuit': [
                'upper circuit', 'upar circuit', 'upper sarkit', 'upar sarkit',
                'uc pakka', 'uc confirm', 'uc hit', 'uc lagega', 'uc jayega'
            ],
            # Target variants
            'target': [
                'target', 'टारगेट', 'లక్ష్యం', 'இலக்கு',
                'target pakka', 'target confirm', 'target hit hoga'
            ],
            # Operator/Insider variants
            'operator': [
                'operator', 'ऑपरेटर', 'operator game', 'operator stock',
                'operator chal raha', 'insider', 'insider news', 'insider info'
            ],
            # Buy/Sell urgency
            'buy_urgency': [
                'buy now', 'buy karo', 'kharid lo', 'खरीद लो', 'కొనండి',
                'abhi kharido', 'jaldi karo', 'last chance', 'dont miss'
            ],
            # Multibagger variants
            'multibagger': [
                'multibagger', 'multi bagger', 'मल्टीबैगर', 'multibagger stock',
                '10x', '100x', 'moon shot', 'rocket'
            ],
            # Profit/Loss
            'profit': [
                'profit pakka', 'profit confirm', 'लाभ पक्का', 'లాభం ఖచ్చితం',
                'book profit', 'exit karo', 'sell karo'
            ],
            # Scam/Fraud indicators
            'scam': [
                'scam', 'fraud', 'धोखा', 'మోసం', 'கள்ளம்',
                'fake news', 'rumor', 'झूठी खबर'
            ]
        }
        
        # Flatten for quick lookup
        self.all_variants = {}
        for category, variants in self.transliteration_map.items():
            for variant in variants:
                self.all_variants[variant.lower()] = category
    
    def detect_language(self, text: str) -> str:
        """Detect language using langdetect"""
        if not detect:
            return 'unknown'
        try:
            lang = detect(text)
            lang_map = {
                'hi': 'Hindi',
                'te': 'Telugu', 
                'ta': 'Tamil',
                'en': 'English',
                'mr': 'Marathi',
                'gu': 'Gujarati'
            }
            return lang_map.get(lang, lang)
        except (LangDetectException, Exception):
            return 'unknown'
    
    def detect_vernacular_fraud(self, text: str) -> Dict:
        """
        Detect fraud phrases in Hinglish/vernacular
        Returns: detected phrases, language, fraud score
        """
        text_lower = text.lower()
        detected_phrases = []
        categories_found = set()
        
        # Check all transliteration variants
        for variant, category in self.all_variants.items():
            if variant in text_lower:
                detected_phrases.append(variant)
                categories_found.add(category)
        
        # Detect language
        language = self.detect_language(text)
        
        # Calculate fraud score (0-10)
        fraud_score = min(10, len(detected_phrases) * 2)
        
        # Boost score for non-English (more likely manipulation)
        if language not in ['English', 'unknown']:
            fraud_score = min(10, fraud_score + 2)
        
        return {
            'detected_phrases': detected_phrases,
            'categories': list(categories_found),
            'language': language,
            'fraud_score': fraud_score,
            'is_vernacular': language not in ['English', 'unknown'],
            'transliteration_detected': len(detected_phrases) > 0
        }
    
    def get_fraud_explanation(self, detection: Dict) -> str:
        """Generate explanation for detected fraud"""
        if not detection['detected_phrases']:
            return ""
        
        phrases_str = ', '.join([f"'{p}'" for p in detection['detected_phrases'][:3]])
        lang_str = f" ({detection['language']})" if detection['is_vernacular'] else ""
        
        return f"Detected Hinglish/vernacular pump phrases{lang_str}: {phrases_str}"

# Global instance
vernacular_detector = VernacularDetector()
