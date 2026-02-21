# 🔍 Finding Real Telegram Channels

## ⚠️ For Fraud Detection: You Need SUSPICIOUS Channels!

Not official channels like NSE/BSE - you need **pump & dump groups**!

---

## 🚀 Automated Method (BEST)

### Run the Channel Finder Script:

```bash
python find_fraud_channels.py
```

This will:
1. Search Telegram for suspicious channels
2. Filter for fraud-related keywords
3. Output ready-to-use channel list
4. Show member counts and titles

**Copy the output directly to your `.env` file!**

---

## 🔍 Manual Method

### Step 1: Search in Telegram App

Search for these terms:
- "stock tips india"
- "intraday calls"
- "BTST calls"
- "penny stock tips"
- "multibagger stocks"
- "share market advisory"
- "equity tips"
- "stock recommendations"

### Step 2: Identify Suspicious Channels

Look for channels with:
- ✅ 1K-50K members (sweet spot)
- ✅ Keywords: "tips", "calls", "premium", "VIP", "advisory"
- ✅ Frequent posts with stock names
- ✅ Language like "guaranteed", "sure shot", "100%"

### Step 3: Get Username

1. Open channel
2. Click channel name
3. Look for @username
4. Copy without @ symbol

### Step 4: Add to .env

```env
CHANNELS=channel1,channel2,channel3
```

---

## 🎯 What to Look For

### ✅ Good Fraud Detection Channels:
- "Premium Stock Tips"
- "Intraday Calls VIP"
- "Multibagger Advisory"
- "BTST Jackpot Calls"
- "Penny Stock Alerts"

### ❌ NOT Good for Fraud Detection:
- NSEIndia (official)
- BSEIndia (official)
- MoneycontrolNews (news)
- EconomicTimes (news)

---

## 💡 Pro Tips

1. **Start with 3-5 channels** to test
2. **Mix of sizes**: 2K, 10K, 30K members
3. **Active channels**: Posted in last 24 hours
4. **Hindi/Hinglish**: Better for Indian market fraud
5. **Free channels**: Paid groups are harder to access

---

## 🚨 Example Real Patterns

Channels often have names like:
- `@stocktipsXYZ`
- `@intradaycallsABC`
- `@premiumequitytips`
- `@multibagger2024`
- `@niftybankoptionscalls`

**Note:** Exact usernames change frequently as channels get banned!

---

## ⚡ Quick Start

```bash
# Method 1: Automated
python find_fraud_channels.py
# Copy output to .env

# Method 2: Manual
# 1. Open Telegram
# 2. Search "stock tips india"
# 3. Join 3-5 suspicious channels
# 4. Copy usernames to .env

# Method 3: Use discovery API
python main.py
curl "http://localhost:8000/discover-channels?query=stock+tips"
# Copy usernames from response
```

---

## 🔒 Legal Note

You're monitoring **public channels** for:
- ✅ Educational research
- ✅ Fraud detection
- ✅ Investor protection
- ✅ Pattern analysis

This is legal and ethical!
