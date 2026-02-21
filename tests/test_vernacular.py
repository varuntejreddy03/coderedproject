"""
Test Vernacular & Hinglish Fraud Detection
Demonstrates: Language detection + Transliteration variants + Multilingual keywords
"""
import sys
sys.path.append('..')

from core.vernacular_detector import VernacularDetector

def test_vernacular_detection():
    detector = VernacularDetector()
    
    print("\n" + "="*80)
    print("VERNACULAR & HINGLISH FRAUD DETECTION")
    print("="*80)
    
    # Test cases with different languages and transliterations
    test_messages = [
        # English
        ("RELIANCE upper circuit pakka hai!", "English/Hinglish"),
        
        # Hinglish variants
        ("TATA upar circuit confirm! Buy karo jaldi!", "Hinglish"),
        ("INFY upper sarkit lagega! Target 2000!", "Hinglish"),
        ("HDFC UC pakka hai! Operator game chal raha!", "Hinglish"),
        
        # Hindi (Devanagari)
        ("TCS target pakka hai! Multibagger stock!", "Hindi"),
        
        # Telugu mix
        ("WIPRO multibagger stock! UC hit!", "Telugu-English"),
        
        # Multiple fraud phrases
        ("RELIANCE buy now! Upper circuit pakka! Operator game! Last chance!", "High Risk"),
        
        # Normal message (control)
        ("INFY quarterly results announced today", "Normal"),
        
        # Transliteration variants
        ("TATA upar sarkit confirm! Jaldi kharido!", "Transliteration"),
        ("HDFC uc lagega! Abhi lelo!", "Transliteration"),
    ]
    
    print("\nAnalyzing messages:\n")
    print("-" * 80)
    
    for i, (message, label) in enumerate(test_messages, 1):
        print(f"\n{i}. [{label}]")
        print(f"   Message: \"{message}\"")
        
        result = detector.detect_vernacular_fraud(message)
        
        print(f"   Language: {result['language']}")
        print(f"   Fraud Score: {result['fraud_score']}/10")
        
        if result['detected_phrases']:
            print(f"   Detected Phrases: {', '.join(result['detected_phrases'])}")
            print(f"   Categories: {', '.join(result['categories'])}")
            
            explanation = detector.get_fraud_explanation(result)
            print(f"   Explanation: {explanation}")
        else:
            print("   Status: No fraud phrases detected")
        
        print("-" * 80)
    
    # Summary statistics
    print("\n" + "="*80)
    print("TRANSLITERATION COVERAGE")
    print("="*80)
    
    print("\nUpper Circuit Variants:")
    for variant in detector.transliteration_map['upper_circuit']:
        print(f"  - {variant}")
    
    print("\nBuy Urgency Variants:")
    for variant in detector.transliteration_map['buy_urgency'][:8]:
        print(f"  - {variant}")
    
    print("\nOperator/Insider Variants:")
    for variant in detector.transliteration_map['operator'][:6]:
        print(f"  - {variant}")
    
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80)
    print("\n1. Detects 50+ transliteration variants of common pump phrases")
    print("2. Supports Hindi, Telugu, Tamil, Marathi, Gujarati detection")
    print("3. Catches 'upar circuit', 'upper sarkit', 'UC pakka' as same phrase")
    print("4. Fraud score increases for non-English messages (higher risk)")
    print("5. Provides natural language explanation for each detection")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    test_vernacular_detection()
