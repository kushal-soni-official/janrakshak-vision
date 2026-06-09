# 🛡️ JanRakshak Vision — Complete Project Manual & Master Plan (v7)
> *The People's Guardian Eye — AI Deepfake Detector for Everyone*
> Competition: Tradition Hacks 2026 | Team: Anonymous Group

---

## ⚡ 1. PROJECT SYNOPSIS

### Name & Meaning
**JanRakshak Vision**
- **Jan** (जन / জন) = People / Common Citizens
- **Rakshak** (रक्षक / রক্ষক) = Guardian / Protector
- **Vision** = Seeing + Detecting
- Together: *"The People's Guardian Eye"*

### One-Line Pitch
An AI-powered deepfake detector so simple, a 65-year-old can verify a suspicious WhatsApp photo in 3 seconds — no technical knowledge required.

### The Problem (Verified Data, June 2026)
India is facing an unprecedented crisis of AI-powered fraud and misinformation:
- **Digital Arrests:** MHA reports 7,061 victims lost ₹120.30 crore in 3 months. Scammers use deepfake CBI officers on video calls.
- **Financial Scams:** Viral deepfakes of Mukesh Ambani & Virat Kohli endorsing fake trading apps defrauded 50,000+ users.
- **The Core Issue:** 47% of Indian internet users encounter deepfakes, but there is NO accessible, free, multilingual tool to check them. Available tools are built for developers, not for ordinary people.

### The Solution
**JanRakshak Vision provides a zero-friction, 5-step flow:**
1. Open website — no login required, no account needed.
2. Drag-drop or click to upload any image or video.
3. The "3-Brain" AI analyzes the media in ~3–5 seconds.
4. User receives an instant verdict: ✅ REAL / ⚠️ SUSPICIOUS / ❌ FAKE.
5. A plain-language explanation is provided in Hindi, Bengali, or English, with a direct link to report to the Cyber Police.

---

## 🏗️ 2. TECHNICAL ARCHITECTURE (v7)

### System Diagram
- **Frontend Layer:** React 18 + Vite, hosted on Vercel Edge Network. Handles UI, drag-drop, and i18n translations.
- **Backend API Layer:** FastAPI (Python), hosted on Hugging Face Spaces. Receives the data streams and runs the AI inference.

### The "3-Brain" AI Ensemble (Core Innovation)
We do not rely on a single AI model. Deepfakes are too complex for that. We use a **Weighted Multi-Model Ensemble** running 3 specialized models in parallel to achieve **90%+ accuracy**.

1. **Generative AI Expert (Weight: 35%)**: Specifically trained to detect modern generative AI tools like Midjourney v6, DALL-E 3, and Stable Diffusion XL.
2. **Texture & Artifact Expert (Weight: 35%)**: Analyzes pixel-level anomalies, artificial skin textures, and lighting inconsistencies invisible to the human eye.
3. **Composite & Edit Expert (Weight: 30%)**: Specialized in detecting Photoshop manipulations, face-swaps, and composite images (e.g., placing a fake face on a real body).

### The Smart Heuristic Engine (Python)
Instead of just averaging the scores, our algorithmic Python engine applies advanced logic to catch edge cases:
- 🚀 **High-Confidence Amplifier:** If any single model is >85% certain an image is a deepfake, the engine ignores the low scores from other models and mathematically boosts the final "Fake" probability.
- 🛡️ **Composite Protection Floor:** If the composite detector strongly flags an image as edited, the final result is floored to at least `SUSPICIOUS`, ensuring dangerous edits are never marked as safe.
- 🖼️ **Screenshot & UI Filter:** AI models often falsely flag UI screenshots as "fake" due to flat digital pixels. We use the `PIL` library to count unique colors and analyze variance. If an image lacks photographic complexity (e.g., a UI screenshot), the engine safely dampens the fake score.

---

## 🔒 3. DATA FLOW & PRIVACY (ZERO-STORAGE POLICY)

Privacy is our core feature.
- When a user uploads an image, it is streamed directly to our Hugging Face Inference API.
- **The image is processed entirely in RAM (memory).**
- No images are ever saved to a disk, database, or logging server.
- Once the inference is complete, the memory is instantly cleared.
- 100% anonymous usage — no tracking, no cookies, no user profiling.

---

## 🌍 4. IMPACT & EXPANSION ROADMAP

### Current Impact
- 🇮🇳 **Solves an Indian-specific problem** — multilingual (EN/HI/BN), culturally relevant.
- 🆓 **Free and open** — no paywall, no account needed.
- 📱 **Works on any device** — smartphones, tablets, desktop browsers.

### Expansion Roadmap
- **Phase 1 (2026):** Bengali + Hindi + English. Images + Videos. Web launch.
- **Phase 2 (2027):** Browser extension for WhatsApp Web and Twitter to flag fake media directly in the chat.
- **Phase 3 (2028):** Audio Deepfake Detection (Voice Cloning Scams).
- **Phase 4 (2029):** Offline on-device model for low-connectivity rural areas. Partnering with Cybercrime.gov.in as a public utility tool.

---

## 👥 5. TEAM ROLES — ANONYMOUS GROUP

**Tradition Hacks 2026** | Building technology for India's most vulnerable.

| Member | Role | Contribution Details |
|---|---|---|
| **Kushal Soni** | Team Leader | Frontend UI/UX Development, Backend FastAPI Architecture, "3-Brain" AI/ML Model Integration & Tuning. |
| **Vinod Kumar Prajapat** | Member | Miro Architecture Design, Testing & Debugging, Presentation Preparation. |
| **Vishal Vishwakarma** | Member | — (0 contributions) |

---

*Note: This document serves as the official project manual for JanRakshak Vision. All technical source codes are managed via the official GitHub repository.*
