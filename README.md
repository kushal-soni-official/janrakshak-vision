# 🛡️ JanRakshak Vision — Backend API

> **AI Deepfake Detection Backend** | JanRakshak Vision | Tradition Hacks 2026  
> Team: **Anonymous Group** | Leader: **Kushal Soni**

[![HuggingFace Space](https://img.shields.io/badge/HuggingFace-Space-yellow?logo=huggingface)](https://tglprince-janrakshak-api.hf.space)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://python.org)

---

## 🌐 Live Deployment

| Service | URL |
|---|---|
| **API Base** | https://tglprince-janrakshak-api.hf.space |
| **Swagger UI** | https://tglprince-janrakshak-api.hf.space/docs |
| **Frontend** | https://janrakshak-frontend.vercel.app |

---

## 📡 API Endpoints

### `GET /`
Health check
```json
{
  "status": "JanRakshak Vision API ✅",
  "version": "1.0.0",
  "team": "Anonymous Group",
  "leader": "Kushal Soni",
  "competition": "Tradition Hacks 2026"
}
```

### `POST /analyze/image`
Upload any image (JPG, PNG, WEBP, GIF, BMP — max 50MB)

**Response:**
```json
{
  "verdict": "FAKE",
  "confidence": 88,
  "explanation": {
    "en": "This image shows 88% signs of AI generation or manipulation...",
    "hi": "इस तस्वीर में 88% AI निर्माण के संकेत हैं...",
    "bn": "এই ছবিতে 88% AI তৈরির লক্ষণ দেখা যাচ্ছে..."
  },
  "file_type": "image",
  "file_name": "photo.jpg",
  "frames_analyzed": null,
  "model_votes": [
    {"name": "sdxl", "fake_score": 0.87, "verdict": "FAKE", "confidence": 87},
    {"name": "general", "fake_score": 0.91, "verdict": "FAKE", "confidence": 91}
  ]
}
```

### `POST /analyze/video`
Upload any video (MP4, AVI, MOV — max 100MB)

Same response format + `frames_analyzed` count.

---

## 🤖 AI Model Ensemble (v4 — Data-Driven)

Two models run in parallel, combined with weighted ensemble:

| Model | HuggingFace ID | Weight | Specialty |
|---|---|---|---|
| **sdxl** (primary) | `Organika/sdxl-detector` | 70% | Realistic AI scenes, landscapes |
| **general** (secondary) | `umm-maybe/AI-image-detector` | 30% | Composite edits, manipulated photos |

**Ensemble Logic:**
- Standard: `final = 0.70 × sdxl_score + 0.30 × general_score`
- Edge case (sdxl < 0.10 AND general > 0.55): `final = MAX(sdxl, general)` — catches composite edits
- Thresholds: `FAKE ≥ 58%`, `SUSPICIOUS ≥ 28%`, `REAL < 28%`

---

## 🏗️ Architecture

```
React Frontend (Vercel)
        │
        │ HTTPS POST /analyze/image
        ▼
FastAPI Backend (HuggingFace Space — Docker)
        │
        ├── Model A: Organika/sdxl-detector (70%)
        └── Model B: umm-maybe/AI-image-detector (30%)
                │
                └── Weighted Ensemble → Verdict
```

---

## 🚀 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app:app --reload --port 8000

# Test API
curl -X POST "http://localhost:8000/analyze/image" \
  -F "file=@test_image.jpg"
```

---

## 📁 Project Structure

```
janrakshak-backend/
├── app.py              # FastAPI routes + CORS + lifespan
├── models.py           # Dual-model ensemble inference
├── utils.py            # PIL helpers, frame extraction, explanations
├── requirements.txt    # Python dependencies
└── Dockerfile          # HuggingFace Space Docker config
```

---

## 🌍 Languages Supported

| Language | Code | Full UI |
|---|---|---|
| English | `en` | ✅ |
| हिन्दी (Hindi) | `hi` | ✅ |
| বাংলা (Bengali) | `bn` | ✅ |

---

## 🔒 Privacy

- **Zero storage** — files analyzed in RAM, never written to disk
- **No logs** — no file content logged
- **No accounts** — completely anonymous

---

## 👥 Team

**Anonymous Group** | Tradition Hacks 2026

| Role | Name |
|---|---|
| Team Leader | Kushal Soni |
| Members | _To be updated_ |

---

## 📄 License

MIT License — Free to use, modify, and distribute.
