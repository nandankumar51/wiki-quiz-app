# Easy Deployment Guide - Wiki Quiz App

## 🚀 सबसे आसान तरीका (Recommended)

### Backend: Railway (Free)
### Frontend: Vercel (Free)
### Database: Railway PostgreSQL (Free)

---

## Step-by-Step Guide

### 1️⃣ GitHub पर Code Upload करें

```bash
# Terminal में ये commands run करें:
cd "C:\Users\kunda\OneDrive\Desktop\Deepklarity"

git init
git add .
git commit -m "Wiki Quiz App - Ready for deployment"

# GitHub पर जाएं और new repository बनाएं
# फिर ये commands run करें:
git remote add origin https://github.com/YOUR_USERNAME/wiki-quiz-app.git
git push -u origin main
```

---

### 2️⃣ Backend Deploy करें (Railway)

1. **Railway Account बनाएं:**
   - https://railway.app पर जाएं
   - "Login with GitHub" click करें

2. **New Project बनाएं:**
   - "New Project" → "Deploy from GitHub repo"
   - अपनी repository select करें
   - Root directory: `backend`

3. **Environment Variables Add करें:**
   - Settings → Variables में जाएं
   - Add करें:
     ```
     GOOGLE_API_KEY = your_gemini_api_key_here
     ```
   - Database URL automatic मिलेगा

4. **PostgreSQL Add करें:**
   - "New" → "Database" → "Add PostgreSQL"
   - Automatically connect हो जाएगा

5. **Deploy होने का wait करें**
   - URL मिलेगा जैसे: `https://wiki-quiz-backend.railway.app`
   - इसे copy करें!

---

### 3️⃣ Frontend Deploy करें (Vercel)

1. **Vercel Account बनाएं:**
   - https://vercel.com पर जाएं
   - "Sign Up" → "Continue with GitHub"

2. **New Project:**
   - "Add New" → "Project"
   - GitHub repository import करें

3. **Configure करें:**
   - Framework Preset: **Vite**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Environment Variable Add करें:**
   ```
   Name: VITE_API_URL
   Value: https://wiki-quiz-backend.railway.app
   ```
   (आपका Railway backend URL यहां paste करें)

5. **Deploy करें!**
   - "Deploy" button click करें
   - 2-3 minutes में ready हो जाएगा

6. **CORS Fix करें:**
   - Backend के `main.py` में Vercel URL add करें
   - Railway पर redeploy हो जाएगा automatically

---

## ✅ Deployment Checklist

### Before Deployment:
- [ ] Google Gemini API key ready है
- [ ] GitHub account बना है
- [ ] Code GitHub पर push किया

### Backend (Railway):
- [ ] Railway account बनाया
- [ ] Repository connect किया
- [ ] PostgreSQL database add किया
- [ ] Environment variables set किए
- [ ] Backend URL copy किया

### Frontend (Vercel):
- [ ] Vercel account बनाया
- [ ] Repository import किया
- [ ] VITE_API_URL set किया
- [ ] Deploy successful हुआ
- [ ] Website test किया

---

## 🎯 Final Result

आपको मिलेंगे:

1. **Live Frontend:** `https://wiki-quiz-app.vercel.app`
2. **Live Backend:** `https://wiki-quiz-backend.railway.app`
3. **API Docs:** `https://wiki-quiz-backend.railway.app/docs`

---

## 💰 Cost

✅ **सब कुछ FREE!**

- Vercel: Unlimited deployments (free forever)
- Railway: $5/month credit (enough for this app)
- No credit card required initially

---

## 🐛 अगर Error आए तो:

### CORS Error:
Railway dashboard → Backend → Redeploy करें

### Environment Variable नहीं मिल रहा:
Vercel/Railway dashboard check करें और redeploy करें

### Database Error:
Railway में PostgreSQL service running है check करें

---

## 📱 Share करें!

Deployment होने के बाद अपना app link share कर सकते हैं:
```
https://your-app-name.vercel.app
```

---

**Need Help?** DEPLOYMENT.md file में detailed guide है!
