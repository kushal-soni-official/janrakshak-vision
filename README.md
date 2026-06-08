---
title: JanRakshak Vision API
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: mit
---

# 🛡️ JanRakshak Vision — Backend API

**AI deepfake detection for every Indian citizen**  
Team: **Anonymous Group** | Leader: Kushal Soni | Tradition Hacks 2026

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/analyze/image` | Analyze image (JPG/PNG/WEBP/GIF/BMP, max 50MB) |
| `POST` | `/analyze/video` | Analyze video — samples 8 frames (MP4/AVI/MOV, max 100MB) |

## Response Format

```json
{
  "verdict": "FAKE | SUSPICIOUS | REAL",
  "confidence": 87,
  "explanation": {
    "en": "This image shows 87% signs of AI manipulation...",
    "hi": "इस तस्वीर में 87% AI हेरफेर के संकेत हैं...",
    "bn": "এই ছবিতে 87% AI কারসাজির লক্ষণ দেখা যাচ্ছে..."
  },
  "file_type": "image",
  "file_name": "photo.jpg",
  "frames_analyzed": null,
  "frame_breakdown": null
}
```

## Model
- **Primary**: `dima806/deepfake_vs_real_image_detection` (EfficientNetB0)
- **Fallback**: `prithivMLmods/Deepfake-vs-Real-Image-Classification`
- **Device**: CPU (HuggingFace free tier)

> ⚠️ First request after cold start may take 30–60 seconds while model loads. This is normal.

## Frontend
Live at: https://janrakshak-vision.vercel.app
