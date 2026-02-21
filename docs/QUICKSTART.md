# 🚀 QUICK START GUIDE

## ⚡ One Command Setup

```bash
python start.py
```

**That's it!** This will:
1. Check if you're authenticated
2. If not, ask for phone number once
3. Start PumpWatch with auto-discovery enabled

---

## 📱 First Time Authentication

When you run `python start.py`, you'll see:

```
📱 First time setup - Need to authenticate with Telegram

Your phone number (with country code):
Example: +918374967870

Enter your phone number: +918374967870
```

**Enter:** `+918374967870` (your number with +91)

**Then:**
```
Please enter the code you received: 12345
```

**Check Telegram app** for the 5-digit code, enter it.

**Done!** Session saved, never need to login again.

---

## 🎯 What Happens Next

```
✅ Authentication successful!
✅ Session saved
🚀 Starting PumpWatch with auto-discovery...

INFO - Starting PumpWatch backend...
INFO - Reddit scraper initialized
INFO - Auto-discovery enabled (runs every 5 minutes)
INFO - Application startup complete
INFO - Uvicorn running on http://0.0.0.0:8000
```

---

## 🌐 Test Your System

Open browser: **http://localhost:8000/docs**

Try these endpoints:

### 1. Health Check
```
GET /health
```

### 2. Reddit Posts (Works Now!)
```
GET /reddit-posts?limit=5
```

### 3. Discover Channels (After 5 min)
```
GET /discover-channels?query=stock+tips
```

---

## 🤖 Auto-Discovery Status

After app runs for 5 minutes:

```
INFO - Running channel discovery...
INFO - Discovered new channel: @stocktipsXYZ
INFO - Updated .env with 1 channels
```

Check your `.env` - channels added automatically!

---

## 📊 Full System Test

```bash
# Start app
python start.py

# Wait 5 minutes for auto-discovery

# Test all endpoints
curl http://localhost:8000/health
curl http://localhost:8000/reddit-posts?limit=3
curl http://localhost:8000/messages?limit=5
curl http://localhost:8000/fraud-alerts
```

---

## 🔧 Manual Control

### Start Without Auto-Discovery
```env
# In .env
AUTO_DISCOVERY=false
```

### Find Channels Manually
```bash
python find_fraud_channels.py
```

### Start Main App Only
```bash
python main.py
```

---

## ✅ What Works Right Now

| Feature | Status | Test |
|---------|--------|------|
| Reddit | ✅ Working | `/reddit-posts` |
| Health | ✅ Working | `/health` |
| Swagger UI | ✅ Working | `/docs` |
| Auto-discovery | ⏳ After 5 min | Automatic |
| Telegram | ⏳ After channels found | Automatic |

---

## 💡 Pro Tips

1. **Let it run** - Auto-discovery needs 5-10 minutes
2. **Check logs** - See channels being discovered
3. **Use Swagger UI** - Best way to test endpoints
4. **Reddit works now** - Test while waiting for Telegram

---

## 🐛 Troubleshooting

### "Phone number invalid"
**Fix:** Add country code: `+918374967870`

### "No channels found"
**Normal!** Wait 5 minutes for auto-discovery

### "Session error"
**Fix:** Delete `pumpwatch_session.session` and run `python start.py` again

---

## 🎯 Complete Workflow

```bash
# Day 1: Setup (5 minutes)
python start.py
# Enter phone: +918374967870
# Enter code from Telegram
# Let it run for 10 minutes

# Day 2+: Just start
python start.py
# Already authenticated, starts immediately!
```

---

## 📈 Expected Timeline

- **0 min:** Start app, authenticate
- **0-5 min:** Reddit working, test endpoints
- **5 min:** First auto-discovery runs
- **10 min:** 2-3 channels discovered
- **30 min:** 5-10 channels discovered
- **1 hour:** Full fraud detection operational

---

## 🚀 You're Ready!

```bash
python start.py
```

Then open: **http://localhost:8000/docs**

Your fraud detection system is live! 🎉
