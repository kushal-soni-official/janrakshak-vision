<div align="center">

<img src="docs/assets/preview-home.jpg" alt="JanRakshak Vision — Home Screen" width="700"/>

# 🛡️ JanRakshak Vision

### *People's Guardian Eye — AI-Powered Deepfake Detector for Everyone*

**Instantly detect AI-generated images, deepfake videos, and manipulated media — in seconds, in your language, for free.**

[![Live App](https://img.shields.io/badge/🌐%20Live%20App-janrakshak--frontend.vercel.app-2563EB?style=for-the-badge)](https://janrakshak-frontend.vercel.app)
[![API Status](https://img.shields.io/badge/API-Online%20✅-22c55e?style=for-the-badge)](https://ofc01-janrakshak-api.hf.space)
[![Tradition Hacks 2026](https://img.shields.io/badge/🏆%20Tradition%20Hacks-2026-f59e0b?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-MIT-6366f1?style=for-the-badge)](LICENSE)

</div>

---

## 🚨 The Problem — Why JanRakshak Vision Exists

India is facing an **unprecedented crisis** of AI-powered fraud and misinformation. According to NASSCOM (2024), **47% of internet users** have been affected by deepfakes. Here are real incidents driving this project:

### 📋 Real Documented Incidents (India)

| Category | High-Profile Incident Examples |
|---|---|
| **Financial & Investment Scams** | • **Mukesh Ambani Deepfake (2024):** Viral video endorsing a fake trading app; thousands lost up to ₹5 lakh each.<br>• **Virat Kohli Fake Ad:** AI video promoting a betting platform defrauded 50,000+ users. |
| **Digital Arrests (MHA Alert)** | • **AIIMS Doctor (Jan 2024):** Lost ₹59.6 lakh to scammers posing as CBI officers via deepfake video call.<br>• **MHA Warning (Oct 2024):** 7,061 victims reported in early 2024 with total losses of ₹120.30 crore. |
| **Election Manipulation** | • **Fake PM Modi Video (2024):** Deepfakes circulating on WhatsApp announcing false policies.<br>• **Telangana CM Deepfake:** AI-generated video making communally sensitive statements. |
| **Targeting Vulnerable Citizens** | • **Noida IAS Officer:** 82-year-old defrauded of ₹2.5 crore via deepfake CBI video call.<br>• **Mumbai Businessman:** Lost ₹80 lakh to an AI voice clone of his son claiming urgent bail money. |
| **Image Abuse** | • **Durga Puja Donation Fraud:** Fake AI pandals used for QR code scams.<br>• **Student Morphing (NCRB):** 1,200+ cases of AI intimate images used for blackmail. |

> **The hardest hit are those with the least protection:** senior citizens, rural users, and non-English speakers. JanRakshak Vision exists to protect them. Free. Fast. In their language.

---

## 💡 What It Does

JanRakshak Vision is a **zero-friction deepfake detection platform** — no account, no app download, no technical knowledge required.

```
Anyone → Upload photo or video → Get plain-language verdict in < 5 seconds
```

### Verdict System
| Result | Meaning | Action Advised |
|---|---|---|
| ✅ **REAL** | Media appears authentic, no AI signatures detected | Safe to share |
| ⚠️ **SUSPICIOUS** | Partial manipulation or editing detected | Verify before sharing |
| ❌ **FAKE** | Strong AI generation/deepfake markers found | Do not share — report |

---

## 🖥️ App Preview

<div align="center">
<img src="docs/assets/preview-home.jpg" alt="Home Screen" width="700"/>
<br/><em>Home Screen — Simple drag-and-drop upload, no login needed</em>

<br/><br/>

<img src="docs/assets/preview-analyzing.jpg" alt="Analyzing Screen" width="700"/>
<br/><em>Analysis Screen — Real-time progress with AI model status</em>

<br/><br/>

<img src="docs/assets/preview-result.jpg" alt="Result Screen" width="700"/>
<br/><em>Result Screen — Instant plain-language verdict and explanation</em>

<br/><br/>

<img src="docs/assets/architecture.png" alt="System Architecture" width="700"/>
<br/><em>System Architecture — React UI → FastAPI → Dual AI Ensemble</em>
</div>

---

## 🗺️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER DEVICE (Mobile/PC)                   │
│              React UI hosted on Vercel (CDN)                │
│           Languages: English | हिन्दी | বাংলা              │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTPS POST /analyze/image or /analyze/video
                        ▼
┌─────────────────────────────────────────────────────────────┐
│           FastAPI Backend — HuggingFace Spaces (Docker)     │
│                                                             │
│  ┌──────────────────────┐   ┌───────────────────────────┐  │
│  │  SDXL Detector       │   │  General AI Detector      │  │
│  │  Weight: 70%         │   │  Weight: 30%              │  │
│  └──────────┬───────────┘   └──────────┬────────────────┘  │
│             └──────────┬───────────────┘                    │
│                        ▼                                    │
│              ┌─────────────────┐                            │
│              │ Ensemble Logic  │  (Weighted blend +         │
│              │ Final Verdict   │   edge case detection)     │
│              └────────┬────────┘                            │
└───────────────────────┼─────────────────────────────────────┘
                        │ JSON Response
                        ▼
              { verdict, confidence, explanation_en/hi/bn }
```

**Privacy Guarantee:** Files are analyzed in RAM only. Nothing is written to disk. No storage. No logs. No user data collected.

---

## 🧠 How It Works: The "3-Brain" AI Architecture (v7)

We use a **Weighted Multi-Model Ensemble** (a "3-Brain" system) running in parallel, combined with a custom Smart Heuristic Engine to achieve **90%+ accuracy**.

1. **Generative AI Expert (35%):** Trained to detect Midjourney v6, DALL-E 3, and SDXL.
2. **Texture & Artifact Expert (35%):** Analyzes pixel anomalies and artificial skin textures.
3. **Composite & Edit Expert (30%):** Specialized in detecting Photoshop manipulations and face-swaps.

### The Smart Heuristic Engine
- 🚀 **High-Confidence Amplifier:** If any single model is >85% certain an image is a deepfake, it boosts the final "Fake" probability.
- 🛡️ **Composite Protection Floor:** Strong edits are floored to at least "SUSPICIOUS ⚠️", preventing dangerous edits from showing as "REAL".
- 🖼️ **Screenshot / UI Filter:** Uses `PIL ImageStat` to analyze pixel variance. If an image has massive uniform areas (like a screenshot), the fake score is dampened to prevent false alarms.

---

## 🏗️ Full Tech Stack

| Layer | Technology | Layer | Technology |
|---|---|---|---|
| **Frontend** | React 18 + Vite 8 | **Backend** | FastAPI (Python 3.10) |
| **Styling** | Vanilla CSS (No Tailwind) | **AI Models** | HuggingFace Transformers |
| **i18n** | i18next (EN/HI/BN) | **Image/Video**| Pillow (PIL) / OpenCV |
| **Hosting** | Vercel (Edge CDN) | **Hosting** | HuggingFace Spaces (Docker)|

---

## 📖 User Guide

**Step 1:** Open [janrakshak-frontend.vercel.app](https://janrakshak-frontend.vercel.app).  
**Step 2:** Choose language (⚙️) — EN, हिन्दी, or বাংলা.  
**Step 3:** Upload photo/video via drag-and-drop or tap.  
**Step 4:** Tap **"Check This File"** and wait ~3–5 seconds for the verdict.  
**Step 5:** Share the result to warn contacts or report to cybercrime.gov.in.

---

## 🔬 Advanced API Guide (For Developers)

**Base URL:** `https://ofc01-janrakshak-api.hf.space`

```bash
# Analyze an Image
curl -X POST https://ofc01-janrakshak-api.hf.space/analyze/image -F "file=@your_image.jpg"
```

**JSON Response:**
```json
{
  "verdict": "FAKE",
  "confidence": 88,
  "explanation": { "en": "This image shows 88% signs of AI generation..." },
  "file_type": "image",
  "model_votes": [
    { "name": "sdxl", "fake_score": 0.87, "verdict": "FAKE" },
    { "name": "general", "fake_score": 0.91, "verdict": "FAKE" }
  ]
}
```
*Full Swagger Docs at: `https://ofc01-janrakshak-api.hf.space/docs`*

---

## 🌍 Impact & Future Scope

- 🇮🇳 **Indian-Context:** Multilingual, focuses on scams actively targeting India.
- **Future Roadmap:**
  - **v2:** Browser extension for WhatsApp Web & Social Media.
  - **v3:** Support for all 22 scheduled Indian languages.
  - **v6:** Audio deepfake detection for voice clones.

---

## 👥 Team — Anonymous Group

**Tradition Hacks 2026** | Building technology for India's most vulnerable

| Member | Role | Contribution |
|---|---|---|
| **Kushal Soni** | Team Leader | Frontend Development, Backend Architecture, AI/ML Integration, API Design |
| **Vinod Kumar Prajapat** | Member | Miro Architecture Design, Testing & Debugging, Presentation |
| **Vishal Vishwakarma** | Member | — |

---

## 📄 License & Open Source

MIT License — Free to use, modify, and distribute with attribution.

<div align="center">

**🛡️ JanRakshak Vision** — *Protecting every Indian from AI-powered deception*

[Live App](https://janrakshak-frontend.vercel.app) · [API Docs](https://ofc01-janrakshak-api.hf.space/docs) · [Report a Bug](https://github.com/kushal-soni-official/janrakshak-vision/issues)

*Built with ❤️ for Tradition Hacks 2026 — Anonymous Group*

</div>
