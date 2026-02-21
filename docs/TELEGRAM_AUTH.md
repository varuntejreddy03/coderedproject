# 📱 Telegram Authentication Guide

## Phone Number Format

### ❌ Wrong:
```
8374967870
```

### ✅ Correct:
```
+918374967870
```

**Format:** `+[country code][phone number]`

---

## Country Codes

- 🇮🇳 India: `+91`
- 🇺🇸 USA: `+1`
- 🇬🇧 UK: `+44`
- 🇦🇪 UAE: `+971`

---

## Authentication Flow

### Step 1: Enter Phone
```
Please enter your phone (or bot token): +918374967870
```

### Step 2: Enter Code
```
Please enter the code you received: 12345
```

### Step 3: Enter Password (if 2FA enabled)
```
Please enter your password: your_password
```

---

## First Time Setup

When you run `python find_fraud_channels.py` or `python main.py`:

1. **Phone prompt appears**
   - Enter: `+918374967870` (with +91)

2. **Telegram sends code to your phone**
   - Check Telegram app
   - Enter the 5-digit code

3. **Session saved**
   - File: `channel_finder.session` or `pumpwatch_session.session`
   - Next time: No login needed!

---

## Common Issues

### "Phone number is invalid"
**Cause:** Missing country code  
**Fix:** Add `+91` before number

### "Code invalid"
**Cause:** Wrong code or expired  
**Fix:** Request new code, enter quickly

### "Two-step verification"
**Cause:** You have 2FA enabled  
**Fix:** Enter your Telegram password

### "Flood wait"
**Cause:** Too many login attempts  
**Fix:** Wait 5-10 minutes, try again

---

## Session Files

After first login, these files are created:
- `pumpwatch_session.session` (for main.py)
- `channel_finder.session` (for find_fraud_channels.py)

**Keep these files!** They store your login so you don't need to authenticate again.

---

## Quick Fix

```bash
# Delete old session if having issues
del pumpwatch_session.session
del channel_finder.session

# Run again with correct format
python find_fraud_channels.py
# Enter: +918374967870
```

---

## Security Note

- ✅ Session files are encrypted
- ✅ Safe to keep locally
- ❌ Don't share session files
- ❌ Don't commit to git (already in .gitignore)
