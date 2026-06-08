# 🛡️ JanRakshak Vision

> **AI-powered deepfake & media manipulation detection for every Indian citizen**  
> Built in Hindi, Bengali & English — No technical knowledge required

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-black?logo=vercel)](https://janrakshak-frontend.vercel.app)
[![Backend](https://img.shields.io/badge/Backend-HuggingFace%20Spaces-yellow?logo=huggingface)](https://huggingface.co/spaces/tglprince/janrakshak-api)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

---

## 🎯 The Problem

India faces a **deepfake crisis**:
- **47%** of Indians have been affected by deepfake content
- **900%** increase in AI-manipulated media in 2024–25
- Kolkata's Durga Puja 2024 saw viral deepfake videos of politicians used for fraud
- Most detection tools are English-only and require technical expertise

**Common people — especially in rural India — have no way to verify suspicious media.**

---

## 💡 The Solution: JanRakshak Vision

A free, privacy-first deepfake detector that works for **everyone**:

| Feature | Details |
|---|---|
| 🌐 3 Languages | English, हिंदी, বাংলা — switch anytime |
| 📱 Mobile-first | Works on any smartphone browser |
| 🔒 Privacy | Files analyzed & immediately deleted — nothing stored |
| ⚡ Fast | Results in ~3 seconds for images |
| 🎨 Accessible | 7 color themes + dark/light mode |
| 🎥 Video Support | Analyzes 8 frames via majority vote |

---

## 🏗️ Architecture

```
User (Mobile/Desktop)
        ↓
React Frontend (Vercel CDN)
        ↓ HTTPS POST /analyze/image
FastAPI Backend (HuggingFace Spaces — Free CPU)
        ↓
EfficientNetB0 AI Model (dima806/deepfake_vs_real_image_detection)
        ↓
Verdict: REAL / SUSPICIOUS / FAKE
+ Multilingual explanation (EN / HI / BN)
        ↓
Back to User
```

> 🗺️ [View full architecture diagram on Miro →](YOUR_MIRO_LINK)

---

## 🧠 AI Model

- **Primary**: `dima806/deepfake_vs_real_image_detection`
  - EfficientNetB0 fine-tuned on FaceForensics++ & DFDC datasets
  - Binary: Fake vs Real — Input: PIL Image
- **Fallback**: `prithivMLmods/Deepfake-vs-Real-Image-Classification`
- **Thresholds**: FAKE ≥ 80% · SUSPICIOUS 45–79% · REAL < 45% fake score

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite, Tailwind CSS, i18next, react-dropzone |
| Backend | FastAPI, Python 3.10 |
| AI | HuggingFace Transformers, EfficientNet, PyTorch (CPU) |
| Video | OpenCV, NumPy |
| Hosting | Vercel (frontend) + HuggingFace Spaces Docker (backend) |
| Cost | **₹0 — 100% Free** |

---

## 🚀 Run Locally

### Frontend
```bash
git clone https://github.com/kushal-soni-official/janrakshak-vision
cd janrakshak-vision
npm install
# Create .env file:
echo "VITE_BACKEND_URL=https://tglprince-janrakshak-api.hf.space" > .env
npm run dev
```

### Backend
```bash
git clone https://huggingface.co/spaces/tglprince/janrakshak-api
cd janrakshak-api
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
uvicorn app:app --reload --port 7860
```

---

## 📊 Judging Criteria

| Criteria | Our Approach |
|---|---|
| **Creativity** | First deepfake detector for non-technical users in regional Indian languages |
| **Real World Impact** | Directly addresses ₹70,000 crore deepfake fraud problem in India |
| **Cultural Relevance** | Built specifically for Kolkata / Bengali communities |
| **Technical Implementation** | Full-stack AI app — FastAPI + Transformers + React |
| **Scalability** | Phase 1→4 roadmap: 22 Indian languages, browser extension, election deepfake detection |
| **Innovation** | Multilingual AI explanations generated per-language in real-time |

---

## 🗺️ Roadmap

- **Phase 1** *(current)*: Web app — Image & Video detection, EN/HI/BN
- **Phase 2**: Browser extension for WhatsApp Web & Telegram
- **Phase 3**: 22 Indian language support
- **Phase 4**: Election deepfake monitoring, government API

---

## 👥 Team — Anonymous Group

| Name | Role |
|---|---|
| **Kushal Soni** *(Leader)* | Full-stack development, AI integration, architecture |
| Member 2 | TBD |
| Member 3 | TBD |

**Competition**: Tradition Hacks 2026 · Miro Meetups Kolkata · Platform: Unstop  
**Submission deadline**: June 12, 2026, 5:00 PM IST

---

## 🔗 Links

- **Live Demo**: https://janrakshak-frontend.vercel.app ✅ LIVE
- **Backend API**: https://tglprince-janrakshak-api.hf.space ✅ LIVE
- **Architecture (Miro)**: *(link coming soon)*
- **GitHub**: https://github.com/kushal-soni-official/janrakshak-vision

---

*Built with ❤️ for India · Files are never stored · Privacy first*
