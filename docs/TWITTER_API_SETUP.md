# 🐦 Twitter API Setup Guide (Free Tier)

## ⚡ Quick Setup (5-10 minutes)

### Step 1: Create Twitter Developer Account

1. Go to: https://developer.twitter.com/en/portal/dashboard
2. Click **"Sign up for Free Account"**
3. Log in with your Twitter/X account

### Step 2: Apply for Access

**Choose:** Essential (Free)

**Fill out the form:**

**1. What's your name?**
```
Your Name
```

**2. What country are you based in?**
```
India
```

**3. What's your use case?**
Select: **"Making a bot"** or **"Exploring the API"**

**4. Will you make Twitter content or derived information available to a government entity?**
```
No
```

**5. Describe in your own words what you are building:**
```
Building an educational fraud detection system for my hackathon project called "PumpWatch". 
The system monitors social media for stock market pump & dump schemes to protect retail 
investors. It analyzes public tweets about stock tips, scams, and SEBI alerts to identify 
fraudulent activities. This is for educational and research purposes only.
```

### Step 3: Accept Terms

- ✅ Read and accept Developer Agreement
- ✅ Click **"Submit"**

### Step 4: Verify Email

- Check your email
- Click verification link
- Return to developer portal

### Step 5: Create App

1. Click **"Create Project"**
2. **Project Name:** `PumpWatch`
3. **Use Case:** Select **"Exploring the API"**
4. **Project Description:** 
   ```
   Fraud detection system for stock market scams
   ```

### Step 6: Create App

1. **App Name:** `PumpWatch-Bot`
2. Click **"Next"**

### Step 7: Get Bearer Token

**IMPORTANT:** Copy the Bearer Token immediately!

```
Bearer Token: AAAAAAAAAAAAAAAAAAAAABcdefgh1234567890...
```

**Save it!** You won't see it again.

### Step 8: Add to .env

```env
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAABcdefgh1234567890...
```

---

## ✅ Test Your Setup

```bash
# Install tweepy
pip install tweepy

# Restart app
python main.py

# Test Twitter endpoint
curl http://localhost:8000/twitter-alerts?limit=5
```

---

## 📊 Free Tier Limits

| Feature | Free Tier |
|---------|-----------|
| Tweets per month | 500,000 reads |
| Rate limit | 15 requests / 15 min |
| Search | Last 7 days |
| Cost | $0 (FREE) |

**More than enough for your hackathon!**

---

## 🔑 Where to Find Your Token Later

1. Go to: https://developer.twitter.com/en/portal/dashboard
2. Click your project name
3. Click your app name
4. Go to **"Keys and tokens"** tab
5. Under **"Bearer Token"** → Click **"Regenerate"**

---

## 🐛 Troubleshooting

### "Could not authenticate you"
**Fix:** Check bearer token is correct in .env

### "Rate limit exceeded"
**Fix:** Wait 15 minutes, or reduce query frequency

### "403 Forbidden"
**Fix:** Your app doesn't have read permissions. Check app settings.

### "App suspended"
**Fix:** Verify your email and accept terms

---

## 🎯 Quick Commands

```bash
# Install
pip install tweepy

# Add to .env
TWITTER_BEARER_TOKEN=your_token_here

# Test
python main.py
curl http://localhost:8000/twitter-alerts
```

---

## 💡 Pro Tips

1. **Save your bearer token** in a password manager
2. **Don't commit** .env to git (already in .gitignore)
3. **Regenerate token** if exposed
4. **Free tier is enough** for hackathons
5. **Approval is instant** for Essential tier

---

## 🚀 Alternative: Skip Twitter

If you don't want to wait for approval:

```env
# Leave empty
TWITTER_BEARER_TOKEN=
```

Your system will work with **Telegram + Reddit** only!

---

## ⏱️ Timeline

- **Account creation:** 2 minutes
- **Application:** 3 minutes
- **Approval:** Instant (for Essential/Free tier)
- **Total:** ~5 minutes

Much faster than before! 🎉
