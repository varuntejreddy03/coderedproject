# 🧠 Intelligence Engine Documentation

## Overview

Advanced fraud detection system with 4 core components:

1. **Sentiment Layer** - VADER-style sentiment scoring
2. **Fraud Trigger Engine** - Weighted phrase detection
3. **Hinglish Handler** - Text normalization for Indian context
4. **Hype Intensity Score** - Multi-factor pump detection

---

## 1️⃣ Sentiment Layer

### How It Works
- Analyzes text for bullish/bearish keywords
- Returns score from **-1 (bearish) to +1 (bullish)**
- Weighted scoring based on keyword strength

### Example
```python
Text: "🚀 YESBANK rocket to moon! Strong breakout!"
Sentiment Score: +0.75 (highly bullish)

Text: "YESBANK crash incoming, dump now"
Sentiment Score: -0.70 (highly bearish)
```

### API Response
```json
{
  "sentiment_score": 0.75,
  "sentiment_label": "bullish"
}
```

---

## 2️⃣ Fraud Trigger Engine

### Weighted Phrases

**High Risk (Weight: 3)**
- "upper circuit pakka"
- "operator game"
- "sure shot"
- "guaranteed profit"
- "100% confirmed"
- "insider info"

**Medium Risk (Weight: 2)**
- "multibagger confirmed"
- "rocket stock"
- "jackpot"
- "don't miss"
- "last chance"
- "premium tip"

**Low Risk (Weight: 1)**
- "target"
- "book profit"
- "btst"
- "intraday"

### Example
```python
Text: "Upper circuit pakka! Sure shot multibagger confirmed!"
Fraud Score: 3 + 3 + 2 = 8 (CRITICAL)

Text: "RELIANCE target 2500, book profit"
Fraud Score: 1 + 1 = 2 (LOW)
```

---

## 3️⃣ Hinglish Handler

### Normalization Map

**Pakka Variants:**
- pakkaaa → pakka
- pukka → pakka
- pakaaa → pakka
- pakkaa → pakka

**Common Hinglish:**
- zaroor/zarur/jarur → sure
- bilkul/bilkull → absolutely
- ekdum/ekdam → totally
- bahut/bohot/bhot → very
- jaldi/jaldee → quick
- abhi/abi → now

### Example
```python
Input:  "Pakkaaa zaroor upper circuit! Bilkull sure shot!"
Output: "pakka sure upper circuit absolutely sure shot"
```

---

## 4️⃣ Hype Intensity Score

### Formula
```
Hype Score (0-100) = 
  Mention Score (0-25) +
  Acceleration Score (0-25) +
  Trigger Density Score (0-25) +
  Sentiment Spike Score (0-25)
```

### Components

**1. Mention Count**
- Raw number of mentions
- Normalized to 0-25 scale

**2. Message Acceleration**
- Mentions in last hour vs previous hour
- Detects sudden spikes

**3. Trigger Density**
- Total fraud trigger weight / message count
- Higher = more suspicious

**4. Sentiment Spike**
- Extreme sentiment (very bullish/bearish)
- Indicates coordinated hype

### Risk Levels
- **0-29**: Low risk
- **30-49**: Medium risk
- **50-69**: High risk
- **70-100**: CRITICAL risk

---

## 🎯 API Endpoint: Hype Intensity

### Request
```bash
GET /hype-intensity/YESBANK
```

### Response
```json
{
  "ticker": "YESBANK",
  "hype_score": 78.5,
  "risk_level": "critical",
  "breakdown": {
    "mention_score": 23.0,
    "acceleration_score": 20.0,
    "trigger_score": 18.5,
    "sentiment_score": 17.0
  },
  "metrics": {
    "mention_count": 23,
    "velocity": 12,
    "acceleration": 8,
    "avg_sentiment": 0.68,
    "trigger_density": 2.4
  },
  "recent_messages": [
    {
      "id": 12345,
      "channel": "stocktipsindia",
      "text": "🚀 YESBANK pakkaaa upper circuit! Sure shot multibagger!",
      "sentiment_score": 0.75,
      "sentiment_label": "bullish",
      "fraud_score": 8,
      "fraud_signals": ["upper circuit pakka", "sure shot", "multibagger confirmed"]
    }
  ]
}
```

---

## 📊 Enhanced Message Response

Every message now includes:

```json
{
  "id": 12345,
  "channel": "stocktipsindia",
  "text": "Pakkaaa YESBANK rocket! Upper circuit sure shot!",
  "normalized_text": "pakka yesbank rocket upper circuit sure shot",
  "tickers": ["YESBANK"],
  "fraud_signals": ["upper circuit pakka", "sure shot"],
  "risk_score": 6,
  "sentiment_score": 0.75,
  "sentiment_label": "bullish",
  "fraud_score": 6
}
```

---

## 🚀 Usage Examples

### Detect Coordinated Pump
```python
# Get hype intensity
response = requests.get('http://localhost:8000/hype-intensity/YESBANK')
data = response.json()

if data['hype_score'] > 70:
    print(f"🚨 CRITICAL: {data['ticker']} is being pumped!")
    print(f"Velocity: {data['metrics']['velocity']} mentions/hour")
    print(f"Acceleration: {data['metrics']['acceleration']}")
    print(f"Sentiment: {data['metrics']['avg_sentiment']}")
```

### Track Sentiment Shift
```python
# Get ticker messages
response = requests.get('http://localhost:8000/ticker/YESBANK')
messages = response.json()['recent_messages']

# Analyze sentiment trend
sentiments = [msg['sentiment_score'] for msg in messages]
avg_sentiment = sum(sentiments) / len(sentiments)

if avg_sentiment > 0.5:
    print("📈 Strong bullish sentiment - possible pump")
```

### Filter by Fraud Score
```python
# Get high fraud score messages
response = requests.get('http://localhost:8000/messages?limit=100')
messages = response.json()

critical = [m for m in messages if m['fraud_score'] >= 6]
print(f"Found {len(critical)} critical fraud messages")
```

---

## 🎯 Real-World Scenario

### YESBANK Pump Detection

**Step 1: Check Hype Intensity**
```bash
GET /hype-intensity/YESBANK
```
Result: Hype Score = 78.5 (CRITICAL)

**Step 2: Analyze Breakdown**
- Mention Score: 23 (high volume)
- Acceleration: 20 (sudden spike)
- Trigger Density: 18.5 (many fraud keywords)
- Sentiment: 17 (extreme bullish)

**Step 3: Review Messages**
- "upper circuit pakka" (3x)
- "sure shot" (5x)
- "guaranteed profit" (2x)
- Average sentiment: +0.68 (very bullish)

**Conclusion:** Coordinated pump & dump in progress! 🚨

---

## 💡 Pro Tips

1. **Hype Score > 70** = Immediate alert
2. **Acceleration > 5** = Sudden coordinated activity
3. **Trigger Density > 2** = Heavy fraud language
4. **Sentiment > 0.6** = Artificial hype
5. **Combine all 4** = High confidence pump detection

---

## 🔧 Configuration

All weights and thresholds are in `intelligence_engine.py`:
- Adjust `SENTIMENT_KEYWORDS` for custom sentiment
- Modify `FRAUD_TRIGGERS` weights for your use case
- Add more `HINGLISH_VARIANTS` as needed
- Tune hype score formula in `calculate_hype_intensity()`

---

## 📈 Performance

- **Sentiment Analysis**: O(n) - linear with text length
- **Fraud Detection**: O(m) - linear with trigger count
- **Hinglish Normalization**: O(n) - linear with word count
- **Hype Intensity**: O(k) - linear with message count

All operations are fast enough for real-time processing!
