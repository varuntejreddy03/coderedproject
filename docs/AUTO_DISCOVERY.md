# 🤖 Automated Channel Discovery

## ✅ Zero Manual Work!

The system now **automatically discovers fraud channels** every 5 minutes and updates your `.env` file.

---

## 🚀 Two Ways to Use

### Option 1: Integrated (Recommended)

Auto-discovery runs **inside the main app**:

```bash
# 1. Enable in .env
AUTO_DISCOVERY=true

# 2. Start app (discovery runs automatically)
python main.py
```

**What happens:**
- App starts normally
- Every 5 minutes: Searches for new fraud channels
- Auto-updates `.env` with discovered channels
- No manual intervention needed!

### Option 2: Standalone Service

Run discovery as **separate background service**:

```bash
# Terminal 1: Run discovery service
python auto_discovery.py

# Terminal 2: Run main app
python main.py
```

---

## 🔍 How It Works

```
Every 5 minutes:
1. Search Telegram for fraud-related terms
2. Filter channels with suspicious keywords
3. Add new channels to .env automatically
4. Keep top 10 most recent channels
5. Log discoveries
```

### Search Terms:
- "stock tips"
- "intraday calls"
- "penny stocks"
- "multibagger stocks"
- "BTST calls"

### Suspicious Keywords:
- tip, call, advisory
- premium, vip, intraday
- btst, multibagger, jackpot

---

## 📊 What You'll See

```
2024-01-15 10:00:00 - INFO - Running channel discovery...
2024-01-15 10:00:05 - INFO - Discovered new channel: @stocktipsXYZ
2024-01-15 10:00:07 - INFO - Discovered new channel: @intradaycallsABC
2024-01-15 10:00:10 - INFO - Updated .env with 2 channels
2024-01-15 10:00:10 - INFO - Found 2 new channels
2024-01-15 10:05:00 - INFO - Running channel discovery...
```

---

## ⚙️ Configuration

### Change Discovery Interval

**In .env:**
```env
AUTO_DISCOVERY=true
DISCOVERY_INTERVAL=10  # minutes (default: 5)
```

**Or in code:**
```python
# auto_discovery.py or main.py
await discovery.run_discovery_loop(interval_minutes=10)
```

### Disable Auto-Discovery

```env
AUTO_DISCOVERY=false
```

---

## 🎯 Benefits

✅ **Zero manual work** - Finds channels automatically  
✅ **Always up-to-date** - Discovers new fraud channels  
✅ **Runs in background** - No interruption  
✅ **Auto-updates .env** - Channels persist  
✅ **Rate-limited** - Won't spam Telegram API  
✅ **Filtered** - Only suspicious channels  

---

## 📝 First Time Setup

### Step 1: Authenticate Once
```bash
python main.py
# Enter: +918374967870
# Enter code from Telegram
```

Session is saved! Never need to login again.

### Step 2: Enable Auto-Discovery
```env
AUTO_DISCOVERY=true
```

### Step 3: Start App
```bash
python main.py
```

**That's it!** Channels will be discovered automatically.

---

## 🔧 Troubleshooting

### "No new channels found"
**Normal!** Means all available channels already discovered.

### "Error in discovery loop"
**Check:** Telegram session is valid  
**Fix:** Delete `pumpwatch_session.session` and re-authenticate

### "Rate limit"
**Normal!** Discovery waits 2 seconds between searches.

### Channels not updating
**Check:** `AUTO_DISCOVERY=true` in .env  
**Check:** App is running (not stopped)

---

## 💡 Pro Tips

1. **Let it run overnight** - Discovers more channels
2. **Check logs** - See what's being found
3. **Manual override** - Can still add channels manually to .env
4. **Top 10 kept** - Automatically manages channel list size

---

## 🎓 How It's Better Than Manual

| Method | Time | Effort | Updates |
|--------|------|--------|---------|
| **Manual** | 10 min | High | Never |
| **Auto** | 0 min | Zero | Every 5 min |

---

## 🚀 Quick Start

```bash
# 1. Set in .env
AUTO_DISCOVERY=true

# 2. Run once (authenticate)
python main.py
# Enter phone: +918374967870

# 3. Let it run!
# Channels discovered automatically every 5 minutes
```

---

## 📊 Example Output

After 1 hour of running:

```env
CHANNELS=stocktipsXYZ,intradaycallsABC,premiumequity,multibagger2024,niftyoptions,btststocks,pennystockalerts,jackpotstocks,vipstocktips,equityadvisory
```

**All discovered automatically!** 🎉

---

## ⚡ Summary

**Before:** Manually search → Find channels → Copy to .env  
**Now:** Enable AUTO_DISCOVERY → Done! ✅

Your fraud detection system now **maintains itself**! 🤖
