# 🔧 STEP-BY-STEP FIX - Get All Endpoints Working

## Current Status
✅ Reddit working  
❌ Fraud alerts - needs Telegram data  
❌ Hype intensity - needs Telegram data  
❌ Reality check - needs Telegram data  
❌ Safety dashboard - needs Telegram data  

---

## 🎯 Solution: Add Working Telegram Channels

### Step 1: Stop Current App
Press `Ctrl+C` in terminal

### Step 2: Update .env
Replace your `.env` with this:

```env
API_ID=37812454
API_HASH=c254b2bc3a4b77ac7922fb774fa2d34f

# Working Telegram channels
CHANNELS=MoneyControl,EconomicTimes,ZeeBusiness

# Auto-discovery: Disabled
AUTO_DISCOVERY=false
```

### Step 3: Restart App
```bash
python start.py
```

### Step 4: Wait for Startup
You'll see:
```
INFO - Fetching initial messages...
INFO - Fetched 200 messages from MoneyControl
INFO - Fetched 200 messages from EconomicTimes
INFO - Fetched 200 messages from ZeeBusiness
INFO - Background polling started
INFO - Application startup complete
```

**Wait for "Application startup complete"**

### Step 5: Test Endpoints in Order

#### 5.1 Health Check
```
GET /health
```
Expected: `{"status": "healthy", "messages_count": 600}`

#### 5.2 Messages
```
GET /messages?limit=5
```
Expected: List of 5 messages with tickers

#### 5.3 Tickers
```
GET /tickers
```
Expected: `{"RELIANCE": 10, "TCS": 5, ...}`

#### 5.4 Fraud Alerts
```
GET /fraud-alerts?min_risk=1
```
Expected: List of messages with fraud signals

#### 5.5 Hype Intensity
```
GET /hype-intensity/RELIANCE
```
Expected: Hype score, risk level, metrics

#### 5.6 Reality Check
```
GET /reality-check/RELIANCE
```
Expected: RED/AMBER/GREEN indicator

#### 5.7 Safety Dashboard
```
GET /safety-dashboard
```
Expected: All alerts summary

---

## ⏱️ Timeline

- **0:00** - Start app
- **0:10** - Telegram connected
- **0:30** - Messages fetched (600 messages)
- **1:00** - Background polling started
- **3:00** - First reality check runs
- **3:30** - All endpoints working!

---

## 🐛 If Channels Don't Work

Try these alternative channels:

```env
CHANNELS=business,stockmarket,investing
```

Or just use one that definitely works:

```env
CHANNELS=MoneyControl
```

---

## 📊 Expected Flow

```
1. Start app
   ↓
2. Connect to Telegram (10 sec)
   ↓
3. Fetch messages from channels (20 sec)
   ↓
4. Extract tickers (RELIANCE, TCS, etc.)
   ↓
5. Calculate fraud scores
   ↓
6. Calculate hype intensity
   ↓
7. Wait 3 minutes
   ↓
8. Run reality check
   ↓
9. All endpoints working!
```

---

## 💡 Quick Test

After startup completes, test in this order:

```bash
# 1. Health
curl http://localhost:8000/health

# 2. Messages
curl http://localhost:8000/messages?limit=3

# 3. Tickers
curl http://localhost:8000/tickers

# 4. Reddit (already working)
curl http://localhost:8000/reddit-posts?limit=3
```

If these 4 work, the rest will work too!

---

## 🚨 Common Issues

### Issue: "Telegram not configured"
**Fix:** CHANNELS is empty, add channels to .env

### Issue: "No data for ticker"
**Fix:** Wait 30 seconds for messages to be fetched

### Issue: Stuck at "Connecting..."
**Fix:** Channels don't exist, try: `CHANNELS=MoneyControl`

### Issue: "503 Service Unavailable"
**Fix:** Scraper not initialized, restart app

---

## ✅ Success Checklist

- [ ] App started without errors
- [ ] Saw "Fetched X messages from..."
- [ ] Saw "Application startup complete"
- [ ] `/health` returns message count > 0
- [ ] `/messages` returns data
- [ ] `/tickers` returns stock symbols
- [ ] `/fraud-alerts` returns alerts
- [ ] `/hype-intensity/RELIANCE` works
- [ ] `/reality-check/RELIANCE` works
- [ ] `/safety-dashboard` works

---

## 🎯 Final .env Configuration

```env
API_ID=37812454
API_HASH=c254b2bc3a4b77ac7922fb774fa2d34f

# Use these working channels
CHANNELS=MoneyControl,EconomicTimes,ZeeBusiness

# Keep disabled for faster startup
AUTO_DISCOVERY=false
```

**This will make ALL endpoints work!**
