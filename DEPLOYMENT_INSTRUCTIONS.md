# MERE ADHIKAAR - DEPLOYMENT INSTRUCTIONS

## COMPLETE CHATBOT WITH VOICE INPUT + HINDI/MARATHI TRANSLATIONS

---

## QUICK START (15 MINUTES)

### **Step 1: Get Your API Key (5 minutes)**

1. Go to: **console.anthropic.com**
2. Sign up / Log in
3. Click **"Billing"** → Add **$5 credit**
4. Click **"API Keys"** → **"Create Key"**
5. **COPY THE KEY** (starts with `sk-ant-`)
6. Save it somewhere safe!

---

### **Step 2: Upload to GitHub (5 minutes)**

1. Go to: **github.com**
2. Sign up / Log in
3. Click **"New Repository"**
4. Name it: **`mere-adhikaar`**
5. Make it **PUBLIC**
6. Click **"Create Repository"**

7. **IMPORTANT: Clean slate**
   - If you have old files, **DELETE THEM ALL**
   - Click on each file → trash icon → confirm

8. Click **"uploading an existing file"**
9. Upload these 2 files:
   - **`mere_adhikaar_app.py`**
   - **`requirements.txt`**
10. Click **"Commit changes"**

---

### **Step 3: Deploy on Streamlit Cloud (5 minutes)**

1. Go to: **share.streamlit.io**
2. **Sign in with GitHub**
3. Click **"New app"**
4. Select your repository: **`mere-adhikaar`**
5. Branch: **`main`**
6. Main file path: **`mere_adhikaar_app.py`** (EXACT spelling!)

7. Click **"Advanced settings"**
8. In the **Secrets** box, type EXACTLY:

```toml
ANTHROPIC_API_KEY = "sk-ant-paste-your-key-here"
```

Replace with your ACTUAL API key.

9. Click **"Deploy"**
10. Wait 2-3 minutes
11. **YOU'LL GET A LIVE URL!** 🎉

---

## FEATURES

✅ Voice Input (English, Hindi, Marathi)
✅ Full 3-language support
✅ Safety features (Quick Exit, privacy warnings)
✅ Emergency contacts & legal aid info
✅ All Indian DV laws integrated

---

## TESTING

### **CRITICAL: Test Voice Input BEFORE Demo**

**Voice Setup:**
1. **Use Chrome or Edge browser** (required - Firefox/Safari don't work well)
2. When you first click "Start Recording", browser will ask for microphone permission
3. Click **"Allow"** - this only happens once

**Test in Each Language:**

**English Test:**
1. Make sure language dropdown shows "English"
2. Click "🎤 Start Recording"  
3. Say clearly: "My husband beats me"
4. Check status shows: "✅ Recorded: My husband beats me"
5. Check text appears in chat box below
6. Press Enter to send

**Hindi Test:**
1. Switch language to "हिंदी (Hindi)"
2. Click "🎤 Start Recording"
3. Say clearly: "मेरा पति मुझे पीटता है"
4. Check it appears correctly
5. Press Enter

**Marathi Test:**
1. Switch to "मराठी (Marathi)"
2. Click "🎤 Start Recording"
3. Say clearly: "माझा नवरा मला मारतो"
4. Check it appears
5. Press Enter

**If Voice Doesn't Work:**
- Check you're using Chrome or Edge
- Check microphone permissions (browser settings)
- Check microphone is working (test in other apps)
- Refresh the page and try again
- **Backup plan:** Just type during demo, say "voice feature works but having technical issue"

### **Test Other Features:**
- ✅ Quick Exit button (redirects to Google)
- ✅ Language switching (entire interface changes)
- ✅ Emergency contacts visible
- ✅ Common topic buttons work
- ✅ Chat responds in correct language

---

## TROUBLESHOOTING

**Voice not working?**
- ✅ Use Chrome or Edge (required - Firefox/Safari limited support)
- ✅ Check microphone permissions: Browser settings → Privacy → Microphone → Allow
- ✅ Refresh page after allowing permissions
- ✅ Test microphone in another app first
- ✅ Select correct language BEFORE clicking record
- ✅ Speak clearly and not too fast
- ✅ Check you're not muted
- ✅ Try closing other apps using microphone (Zoom, Teams, etc.)

**API error?**
- ✅ Check secrets format: `ANTHROPIC_API_KEY = "sk-ant-..."`
- ✅ Verify you added $5 credits at console.anthropic.com
- ✅ Try creating new API key
- ✅ Reboot app after updating secrets

**Wrong language in voice?**
- ✅ Select language in dropdown BEFORE clicking record button
- ✅ Language is auto-detected from dropdown selection

**Text not appearing after voice?**
- ✅ Check status message - does it show "✅ Recorded: [text]"?
- ✅ If yes, look for text in chat input box below
- ✅ You may need to scroll down to see chat box
- ✅ Press Enter to send the message

---

**READY FOR DEMO!** 🚀
