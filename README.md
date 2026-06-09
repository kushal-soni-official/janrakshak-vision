---
title: Janrakshak API
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 7860
---

# 🛡️ JanRakshak Vision — Backend API (v7)

> **AI Deepfake Detection Backend** | JanRakshak Vision | Tradition Hacks 2026  
> Team: **Anonymous Group** | Leader: **Kushal Soni**

[![HuggingFace Space](https://img.shields.io/badge/HuggingFace-Space-yellow?logo=huggingface)](https://ofc01-janrakshak-api.hf.space)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://python.org)

---

## 🌐 Live Deployment

| Service | URL |
|---|---|
| **API Base** | https://ofc01-janrakshak-api.hf.space |
| **Swagger UI** | https://ofc01-janrakshak-api.hf.space/docs |
| **Frontend** | https://janrakshak-frontend.vercel.app |

---

## 📡 API Endpoints

### `GET /`
Health check and basic info.
```json
{
  "status": "JanRakshak Vision API ✅",
  "version": "1.0.0",
  "team": "Anonymous Group",
  "leader": "Kushal Soni",
  "competition": "Tradition Hacks 2026",
  "limits": {
    "image_max": "50MB",
    "video_max": "100MB",
    "rate_image": "10 requests/minute per IP",
    "rate_video": "5 requests/minute per IP"
  }
}
```

### `POST /analyze/image`
Upload any image (JPG, PNG, WEBP, GIF, BMP — max 50MB)

**Response:**
```json
{
  "verdict": "FAKE",
  "confidence": 88,
  "fake_score": 0.8842,
  "real_score": 0.1158,
  "explanation": {
    "en": "This image shows 88% signs of AI generation...",
    "hi": "इस तस्वीर में 88% AI निर्माण के संकेत हैं...",
    "bn": "এই ছবিতে 88% AI তৈরির লক্ষণ রয়েছে..."
  },
  "file_type": "image",
  "file_name": "photo.jpg",
  "frames_analyzed": null,
  "model_votes": [
    { "name": "detector_v2", "fake_score": 0.95, "verdict": "FAKE", "confidence": 95 },
    { "name": "sdxl",        "fake_score": 0.82, "verdict": "FAKE", "confidence": 82 },
    { "name": "general",     "fake_score": 0.85, "verdict": "FAKE", "confidence": 85 }
  ]
}
```

### `POST /analyze/video`
Upload any video (MP4, AVI, MOV, MKV — max 100MB)

Same response format + `frames_analyzed` count + `frame_breakdown` array (per-frame verdicts), plus `avg_fake_score` and `real_score` averaged across frames.

---

## 🤖 The "3-Brain" AI Ensemble (v7)

Three models run in parallel, combined with a custom Smart Heuristic Engine:

| Model | HuggingFace ID | Weight | Specialty |
|---|---|---|---|
| **detector_v2** (Gen-AI) | `haywoodsloan/ai-image-detector-deploy` | 35% | Generative AI (Midjourney, DALL-E, SDXL) |
| **sdxl** (Texture) | `Organika/sdxl-detector` | 35% | Pixel noise, texture artifacts |
| **general** (Composites) | `umm-maybe/AI-image-detector` | 30% | Composite edits, face-swaps, Photoshop |

### Smart Heuristic Logic:
- **High-Confidence Boost:** If any single model >85% FAKE, final score is boosted.
- **Composite Floor:** If Brain 3 (Composites) ≥70%, final verdict floored to `SUSPICIOUS`.
- **Screenshot Filter:** Detects UI screenshots (low color count + low variance) and dampens the fake score by 60% to prevent false positives.
- **Thresholds:** `FAKE ≥ 50%`, `SUSPICIOUS ≥ 30%`, `REAL < 30%`

---

## 🏗️ Architecture

```
React Frontend (Vercel)
        │
        │ HTTPS POST /analyze/image
        ▼
FastAPI Backend (HuggingFace Space — Docker)
        │
        ├── Brain 1: haywoodsloan (35%)
        ├── Brain 2: Organika (35%)
        └── Brain 3: umm-maybe (30%)
                │
                └── Smart Heuristic Engine (Python)
                        │
                        └── FAKE / SUSPICIOUS / REAL
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
├── app.py              # FastAPI routes, Rate Limiting (slowapi), CORS, lifespan
├── models.py           # 3-model ensemble inference & heuristic engine
├── utils.py            # PIL helpers, video frame extraction, memory mgmt
├── requirements.txt    # Python dependencies
└── Dockerfile          # HuggingFace Space Docker config
```

---

## 🔒 Privacy & Zero-Storage

- **Zero storage** — files analyzed in RAM, never written to disk (except temp video files, instantly deleted via `os.unlink`).
- **Memory Management** — explicitly calls `del` and `gc.collect()` after every inference to free memory instantly.
- **No logging** — image contents, user IPs, and hashes are never stored.

---

<div align="center">
Built for Tradition Hacks 2026 | Leader: Kushal Soni | Anonymous Group
</div>
