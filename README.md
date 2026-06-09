# 🛡️ JanRakshak Vision — Frontend

> **People's Guardian Eye — AI Deepfake Detector for Everyone**  
> Competition: **Tradition Hacks 2026** | Team: **Anonymous Group** | Leader: **Kushal Soni**

[![Vercel](https://img.shields.io/badge/Deployed-Vercel-black?logo=vercel)](https://janrakshak-frontend.vercel.app)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite)](https://vitejs.dev)

---

## 🌐 Live App

**👉 [janrakshak-frontend.vercel.app](https://janrakshak-frontend.vercel.app)**

| Service | URL |
|---|---|
| **Frontend (Vercel)** | https://janrakshak-frontend.vercel.app |
| **Backend API** | https://ofc01-janrakshak-api.hf.space |
| **API Docs** | https://ofc01-janrakshak-api.hf.space/docs |

---

## 📱 What It Does

JanRakshak Vision is a **zero-friction deepfake detection platform** where anyone — including senior citizens with no technical background — can:

1. **Upload** any suspicious image or video (drag-drop or tap)
2. **Get instant verdict** in < 5 seconds: ✅ REAL / ⚠️ SUSPICIOUS / ❌ FAKE
3. **Read plain-language explanation** in Bengali, Hindi, or English
4. **Share the result** or **Report to Cyber Police** directly

---

## ✨ Features

| Feature | Detail |
|---|---|
| **3 Languages** | English, हिन्दी, বাংলা — full UI translation |
| **Dark/Light Mode** | System default + manual toggle |
| **7 Color Themes** | Blue, Saffron, Forest, Night, Ocean, Rose + Custom |
| **Video Support** | Frame-by-frame analysis (MP4, AVI, MOV) |
| **Privacy First** | Files never stored — analyzed & deleted instantly |
| **Senior Friendly** | Large buttons, simple layout, one-screen design |
| **Share Result** | Copy verdict to clipboard with one click |
| **Report Crime** | Direct link to cybercrime.gov.in |
| **Advanced Panel** | Sensitivity slider + session history for power users |
| **Team Credits** | Anonymous Group popup with member details |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | React 18 + Vite 8 |
| Styling | Vanilla CSS + CSS Variables (theme system) |
| i18n | i18next + react-i18next |
| Upload | react-dropzone |
| Toasts | react-hot-toast |
| Icons | lucide-react |
| HTTP | fetch API |
| Hosting | Vercel (free tier) |

---

## 🚀 Local Development

```bash
# Install dependencies
npm install

# Set backend URL
echo "VITE_BACKEND_URL=https://ofc01-janrakshak-api.hf.space" > .env

# Start dev server
npm run dev

# Build for production
npm run build
```

---

## 📁 Project Structure

```
janrakshak-frontend/
├── public/
│   └── favicon.svg
├── src/
│   ├── components/
│   │   ├── Navbar.jsx          # Header + Settings panel
│   │   ├── UploadZone.jsx      # Drag-drop file upload
│   │   ├── ResultCard.jsx      # Verdict display + actions
│   │   ├── LoadingState.jsx    # Analysis progress UI
│   │   ├── ThemePicker.jsx     # Color theme selector
│   │   ├── AdvancedPanel.jsx   # Power user settings
│   │   └── TeamModal.jsx       # Anonymous Group credits
│   ├── contexts/
│   │   └── ThemeContext.jsx    # Theme state + CSS vars
│   ├── i18n/
│   │   ├── index.js
│   │   └── locales/
│   │       ├── en.json         # English translations
│   │       ├── hi.json         # Hindi translations
│   │       └── bn.json         # Bengali translations
│   ├── utils/
│   │   ├── api.js              # Backend API calls
│   │   └── fileValidator.js    # File type/size checks
│   ├── App.jsx                 # Main app + state machine
│   └── index.css               # Global styles + CSS vars
├── vercel.json                  # SPA routing config
├── .env.example
└── package.json
```

---

## 🌍 Languages

| Language | UI | Verdict | Explanation |
|---|---|---|---|
| English | ✅ | ✅ | ✅ |
| हिन्दी (Hindi) | ✅ | ✅ | ✅ |
| বাংলা (Bengali) | ✅ | ✅ | ✅ |

---

## 🎨 Themes

- **Default** (Blue)
- **Saffron** (Orange — Indian flag)
- **Forest** (Green)
- **Night** (Dark mode)
- **Ocean** (Cyan)
- **Rose** (Pink)
- **Custom** (Any color via picker)

---

## 🔒 Privacy Promise

> ✅ Files are analyzed in memory and **never stored on any server**  
> ✅ No user accounts required  
> ✅ No tracking or analytics  
> ✅ HTTPS encrypted in transit  

---

## 👥 Team

**Anonymous Group** | Tradition Hacks 2026

| Role | Name |
|---|---|
| Team Leader | Kushal Soni |
| Member | Vinod Kumar Prajapat |
| Member | Vishal Vishwakarma |

---

## 🗺️ Roadmap

- **v1 (Now):** EN/HI/BN · Images + Videos · Vercel + HuggingFace
- **v2:** Browser extension for WhatsApp Web
- **v3:** All 22 Indian languages
- **v4:** Election deepfake detection mode
- **v5:** Enterprise API for media organizations

---

## 📄 License

MIT License — Free to use, modify, and distribute.
