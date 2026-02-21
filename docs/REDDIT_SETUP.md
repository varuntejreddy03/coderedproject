# Reddit API Setup - Quick Reference

## Creating Reddit App

Go to: https://www.reddit.com/prefs/apps

Click: "Create App" or "Create Another App"

---

## Form Fields - What to Enter

### 1. name
```
PumpWatch
```

### 2. App type (radio buttons)
Select: **script**
- ✅ script (for personal use)
- ❌ NOT web app
- ❌ NOT installed app

### 3. description
```
Stock market fraud detection and pump & dump monitoring system for educational purposes
```

### 4. about url (optional)
```
https://github.com/yourusername/pumpwatch
```
Or leave blank - it's optional

### 5. redirect uri (REQUIRED)
```
http://localhost:8000
```

**Important:** Even though it's a script app, Reddit requires this field. Use `http://localhost:8000`

---

## After Creating App

You'll see:

```
PumpWatch
personal use script by yourusername
[14 character string]  ← This is your CLIENT_ID
secret: [27 character string]  ← This is your CLIENT_SECRET
```

---

## Copy to .env

```env
REDDIT_CLIENT_ID=your_14_char_id_here
REDDIT_CLIENT_SECRET=your_27_char_secret_here
REDDIT_USER_AGENT=PumpWatch/1.0
```

---

## Why "script" type?

- ✅ No OAuth flow needed
- ✅ Simpler authentication
- ✅ Perfect for backend services
- ✅ Read-only access (what we need)

---

## Common Issues

**Issue:** "redirect uri is required"
**Solution:** Enter `http://localhost:8000` even for script apps

**Issue:** Can't find CLIENT_ID
**Solution:** It's the 14-character string directly under your app name

**Issue:** Can't find CLIENT_SECRET
**Solution:** Look for "secret:" label, copy the string after it

---

## Test Your Setup

After adding credentials to `.env`:

```bash
python main.py
curl http://localhost:8000/reddit-posts?limit=5
```

Should return posts from r/IndianStockMarket!
