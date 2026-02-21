# 🧪 Complete Testing Guide

## 🚀 Quick Test (Without Finding Channels)

### Option 1: Test with Empty Channels (Reddit + Twitter Only)

```bash
# 1. Leave CHANNELS empty in .env
CHANNELS=

# 2. Start backend
python main.py

# 3. Test Reddit
curl http://localhost:8000/reddit-posts?limit=5

# 4. Test Twitter
curl http://localhost:8000/twitter-alerts?limit=5

# 5. Test health
curl http://localhost:8000/health
```

This tests Reddit and Twitter scrapers without Telegram!

---

## 🔍 Option 2: Find Real Channels First

### Step 1: Run Channel Finder
```bash
python find_fraud_channels.py
```

**What happens:**
- Searches Telegram for suspicious channels
- Shows real channel usernames
- Outputs ready-to-paste list

### Step 2: Copy Output to .env
```env
CHANNELS=channel1,channel2,channel3
```

### Step 3: Test Full System
```bash
python main.py
```

---

## 🎯 Option 3: Manual Channel Search

### In Telegram App:

1. **Open Telegram**
2. **Search:** "stock market india"
3. **Find any public channel** with @username
4. **Examples that might exist:**
   - Search "MoneyControl"
   - Search "Economic Times"
   - Search "Stock Market"
5. **Copy username** (without @)
6. **Add to .env:**
   ```env
   CHANNELS=MoneyControl,EconomicTimes
   ```

---

## 📊 Testing Each Feature

### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "messages_count": 0,
  "active_channels": 0
}
```

### 2. Reddit Posts
```bash
curl http://localhost:8000/reddit-posts?limit=3
```

**Expected:**
```json
{
  "posts": [
    {
      "id": "abc123",
      "channel": "r/IndianStockMarket",
      "text": "...",
      "date": "2024-01-15T10:30:00",
      "url": "https://reddit.com/..."
    }
  ],
  "count": 3
}
```

### 3. Twitter Alerts
```bash
curl http://localhost:8000/twitter-alerts?limit=3
```

**Expected:**
```json
{
  "tweets": [
    {
      "id": 123456,
      "channel": "twitter",
      "text": "...",
      "username": "...",
      "url": "https://twitter.com/..."
    }
  ],
  "count": 3
}
```

### 4. Telegram Messages (if channels configured)
```bash
curl http://localhost:8000/messages?limit=5
```

### 5. Fraud Alerts
```bash
curl http://localhost:8000/fraud-alerts?min_risk=2
```

### 6. Hype Intensity (if data available)
```bash
curl http://localhost:8000/hype-intensity/RELIANCE
```

### 7. Channel Discovery
```bash
curl "http://localhost:8000/discover-channels?query=stock+market"
```

---

## 🌐 Interactive Testing (Best!)

### Open Swagger UI:
```
http://localhost:8000/docs
```

**Features:**
- ✅ Visual interface
- ✅ Try all endpoints
- ✅ See responses instantly
- ✅ No curl needed

**Steps:**
1. Open browser → http://localhost:8000/docs
2. Click any endpoint (e.g., `/health`)
3. Click "Try it out"
4. Click "Execute"
5. See response below

---

## 🧪 Run Test Script

```bash
python test_api.py
```

**What it does:**
- Tests all endpoints
- Shows formatted output
- Displays sample data
- Checks if everything works

---

## ✅ What Should Work Right Now

Even without Telegram channels:

| Feature | Status | Test Command |
|---------|--------|--------------|
| Health Check | ✅ Works | `curl http://localhost:8000/health` |
| Reddit Posts | ✅ Works | `curl http://localhost:8000/reddit-posts` |
| Twitter Alerts | ✅ Works | `curl http://localhost:8000/twitter-alerts` |
| Swagger UI | ✅ Works | Open http://localhost:8000/docs |
| Telegram | ⚠️ Needs channels | Find channels first |

---

## 🎯 Recommended Testing Flow

### Phase 1: Test Without Telegram
```bash
# 1. Set empty channels
CHANNELS=

# 2. Start app
python main.py

# 3. Test Reddit
curl http://localhost:8000/reddit-posts?limit=3

# 4. Test Twitter
curl http://localhost:8000/twitter-alerts?limit=3

# 5. Open Swagger UI
# Browser: http://localhost:8000/docs
```

### Phase 2: Find Channels
```bash
# Run channel finder
python find_fraud_channels.py

# Copy output to .env
# Restart app
```

### Phase 3: Test Full System
```bash
# Test all endpoints
python test_api.py

# Or use Swagger UI
# http://localhost:8000/docs
```

---

## 🐛 Troubleshooting

### "Nobody is using this username"
**Solution:** Those channels don't exist. Run `python find_fraud_channels.py` to find real ones.

### "can't compare offset-naive and offset-aware datetimes"
**Solution:** Already fixed in code. Restart app.

### "Connection refused"
**Solution:** App not running. Start with `python main.py`

### "No data returned"
**Solution:** Normal if no channels configured. Test Reddit/Twitter instead.

---

## 💡 Pro Tip

**Start simple:**
1. Test with empty CHANNELS (Reddit + Twitter work)
2. Verify those work
3. Then find Telegram channels
4. Test full system

This way you can demo the project even without finding fraud channels!
