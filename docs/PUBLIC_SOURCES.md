# 📡 Public Data Sources

## ✅ Telegram Channels (Already Configured)

### News & Market Updates (Legitimate)
- `MoneyControlNews` - Moneycontrol official
- `EconomicTimes` - Economic Times news
- `ZeeBusiness` - Zee Business updates
- `CNBCTVAwaaz` - CNBC Awaaz Hindi
- `StockMarketToday` - Market updates

**These work immediately!** No fraud, but good for testing the system.

---

## ✅ Reddit Subreddits (Already Configured)

### Automatically Monitored:
- `r/IndianStockMarket` - Main Indian stock discussions
- `r/IndianStreetBets` - Retail investor community
- `r/DalalStreetTalks` - Stock market conversations

**No setup needed!** System scrapes these automatically.

---

## 🔍 Finding Fraud Channels

### Auto-Discovery Searches For:
- "stock tips" - Tip providers
- "intraday calls" - Day trading groups
- "multibagger stocks" - Pump groups
- "BTST calls" - Short-term trades
- "penny stocks" - Small cap pumps
- "premium tips" - Paid groups
- "share bazaar tips" - Hindi groups

**Runs every 5 minutes automatically!**

---

## 🎯 How It Works

```
┌─────────────────────────────────────┐
│  DATA SOURCES                       │
├─────────────────────────────────────┤
│                                     │
│  📱 TELEGRAM (5 channels now)       │
│  ├─ MoneyControlNews               │
│  ├─ EconomicTimes                  │
│  ├─ ZeeBusiness                    │
│  ├─ CNBCTVAwaaz                    │
│  └─ StockMarketToday               │
│                                     │
│  🔴 REDDIT (3 subreddits)           │
│  ├─ r/IndianStockMarket            │
│  ├─ r/IndianStreetBets             │
│  └─ r/DalalStreetTalks             │
│                                     │
│  🤖 AUTO-DISCOVERY                  │
│  └─ Finds fraud channels every 5min│
│                                     │
└─────────────────────────────────────┘
```

---

## 🚀 Test Now

```bash
# Start app
python start.py

# Open browser
http://localhost:8000/docs

# Test endpoints:
# - /health
# - /messages (Telegram)
# - /reddit-posts (Reddit)
# - /tickers (All mentioned stocks)
```

---

## 📊 What You'll See

### Telegram Messages:
```json
{
  "channel": "MoneyControlNews",
  "text": "Sensex up 200 points, Nifty at 21,500",
  "tickers": ["SENSEX", "NIFTY"],
  "sentiment_score": 0.65,
  "fraud_score": 0
}
```

### Reddit Posts:
```json
{
  "channel": "r/IndianStockMarket",
  "text": "Discussion: Best stocks for 2024",
  "url": "https://reddit.com/r/IndianStockMarket/..."
}
```

---

## 🎯 Next Steps

1. **Test with current channels** (legitimate news)
2. **Wait 5 minutes** for auto-discovery
3. **Check `.env`** - fraud channels added automatically
4. **Monitor fraud alerts** - `/fraud-alerts` endpoint

---

## 💡 Pro Tip

Current channels are **legitimate news sources** - good for testing but won't show fraud.

**Auto-discovery will find fraud channels automatically!**

After 10-15 minutes, you'll have:
- 5 news channels (current)
- 10-15 fraud channels (auto-discovered)
- 3 Reddit communities
- Full fraud detection operational

**Just let it run!** 🚀
