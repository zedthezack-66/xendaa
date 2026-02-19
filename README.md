# 🇿🇲 Xtenda Finance — WhatsApp AI Bot
**Stack: Python + Flask + Meta Cloud API + Gemini AI + Google Sheets**
**Total Cost: $0/month** *(only Meta's ~$0.02/conversation fee applies)*

---

## 📱 What the Bot Does

| Feature | Details |
|---|---|
| Welcome message | Auto-sent on first message with structured menu |
| Loan product info | Personal, Business, Salary-Backed, Asset Finance |
| Eligibility check | Instant structured response |
| Lead capture | Collects loan type → amount → employment → name → callback time |
| Callback booking | Name + preferred time saved to Google Sheets |
| AI Q&A | Gemini answers anything else about Xtenda Finance |
| Human handoff | Escalation message with reference number |

---

## 🗂️ File Structure

```
xtenda-bot/
├── app.py            ← Flask server & webhook handler
├── bot_flow.py       ← Hybrid logic (rules + AI routing)
├── whatsapp.py       ← All WhatsApp message senders
├── gemini_ai.py      ← Gemini AI integration
├── sheets.py         ← Google Sheets lead saving
├── requirements.txt
├── Procfile          ← For Render deployment
├── .env.example      ← Copy to .env and fill in values
└── credentials.json  ← Google service account (you add this)
```

---

## 🚀 Setup Guide (Step by Step)

### STEP 1 — Meta WhatsApp Cloud API (Free)

1. Go to **https://developers.facebook.com** → Create an account
2. Create a new App → choose **Business** type
3. Add **WhatsApp** product to your app
4. Go to **WhatsApp → API Setup**
5. Copy your:
   - `Access Token` → paste into `.env` as `WHATSAPP_ACCESS_TOKEN`
   - `Phone Number ID` → paste into `.env` as `PHONE_NUMBER_ID`
6. Add a real phone number (or use the test number Meta gives you)

---

### STEP 2 — Gemini AI API (Free)

1. Go to **https://aistudio.google.com/app/apikey**
2. Click **Create API Key**
3. Copy the key → paste into `.env` as `GEMINI_API_KEY`
4. Free tier = **1,500 requests/month** (Gemini 1.5 Flash)

---

### STEP 3 — Google Sheets (Free)

1. Go to **https://console.cloud.google.com**
2. Create a new project → Enable **Google Sheets API** and **Google Drive API**
3. Go to **Credentials → Create Service Account**
4. Download the JSON key → save as `credentials.json` in the project folder
5. Copy your Google account email to `.env` as `GOOGLE_SHARE_EMAIL`
   *(The bot will auto-share the created sheet with this email)*

---

### STEP 4 — Deploy to Render (Free Hosting)

1. Push this project to GitHub
2. Go to **https://render.com** → New Web Service
3. Connect your GitHub repo
4. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
5. Add all your `.env` variables in the **Environment** section
6. Deploy — Render gives you a free URL like:
   `https://xtenda-bot.onrender.com`

---

### STEP 5 — Connect Webhook to Meta

1. In Meta Developer Dashboard → **WhatsApp → Configuration**
2. Set Webhook URL to: `https://xtenda-bot.onrender.com/webhook`
3. Set Verify Token to: `xtenda_verify_token`
4. Click **Verify and Save**
5. Subscribe to `messages` webhook field

---

### STEP 6 — Test It!

Send "Hi" to your WhatsApp number → The bot should respond with the welcome menu!

---

## 💬 Conversation Flow

```
Customer: "Hi"
    ↓
Bot: Welcome menu (5 options as list)
    ├── 💰 Our Loan Products → Product submenu
    │       ├── Personal Loan → Info + Apply/Callback buttons
    │       ├── Business Loan → Info + Apply/Callback buttons
    │       ├── Salary-Backed Loan → Info + ...
    │       └── Asset Finance → Info + ...
    │
    ├── ✅ Check Eligibility → Requirements + Apply/Callback
    │
    ├── 📋 Apply / Get a Quote
    │       → Select loan type
    │       → Enter amount (free text)
    │       → Employment status (3 buttons)
    │       → Full name (free text)
    │       → Callback time (3 buttons)
    │       → ✅ SAVED TO GOOGLE SHEETS + Confirmation message
    │
    ├── 📞 Book a Callback
    │       → Full name (free text)
    │       → Callback time (3 buttons)
    │       → ✅ SAVED TO GOOGLE SHEETS + Confirmation message
    │
    └── ❓ Ask a Question → Gemini AI answers freely
```

---

## ⚙️ Customising the Bot

| What to change | Where |
|---|---|
| Loan products & rates | `bot_flow.py` → `PRODUCT_INFO` dict |
| AI personality & knowledge | `gemini_ai.py` → `system_instruction` |
| Menu options | `whatsapp.py` → `send_main_menu()` |
| Sheet column names | `sheets.py` → `HEADERS` list |
| Welcome message | `whatsapp.py` → `send_main_menu()` |

---

## 💰 Cost Breakdown

| Item | Cost |
|---|---|
| Meta Cloud API | Free |
| Gemini 1.5 Flash (1,500/month) | Free |
| Render hosting | Free |
| Google Sheets | Free |
| WhatsApp conversation fees | ~$0.02 per 24hr conversation |
| **500 conversations/month** | **~$10/month** |

---

## 🆘 Common Issues

**Bot not responding?**
- Check Render logs for errors
- Make sure webhook is verified in Meta dashboard
- Ensure `WHATSAPP_ACCESS_TOKEN` hasn't expired (refresh in Meta dashboard)

**Google Sheets not saving?**
- Confirm `credentials.json` is in the project root
- Make sure you enabled both Sheets API and Drive API in Google Cloud

**Gemini errors?**
- Check you haven't exceeded 1,500 free requests
- Verify `GEMINI_API_KEY` is correct in `.env`
