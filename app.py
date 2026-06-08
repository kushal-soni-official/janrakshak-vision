"""
JanRakshak Vision — FastAPI Backend
AI Deepfake Detection for Everyone
Team: Anonymous Group | Leader: Kushal Soni
Competition: Tradition Hacks 2026

Endpoints:
  GET  /              → Health check
  POST /analyze/image → Analyze image file
  POST /analyze/video → Analyze video (frame-by-frame majority vote)
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from models import preload_model, run_inference
from utils import bytes_to_pil, extract_frames, generate_explanations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_IMAGE = 50 * 1024 * 1024   # 50MB
MAX_VIDEO = 100 * 1024 * 1024  # 100MB


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🛡️ JanRakshak Vision API starting — Team: Anonymous Group")
    preload_model()
    logger.info("✅ Ready")
    yield


app = FastAPI(
    title="JanRakshak Vision API",
    description="AI deepfake detection for everyone. Team: Anonymous Group. Leader: Kushal Soni. Tradition Hacks 2026.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def health():
    return {
        "status": "JanRakshak Vision API ✅",
        "version": "1.0.0",
        "team": "Anonymous Group",
        "leader": "Kushal Soni",
        "competition": "Tradition Hacks 2026",
    }


@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image.")

    content = await file.read()
    if len(content) > MAX_IMAGE:
        raise HTTPException(400, "File too large. Maximum 50MB.")

    try:
        pil_image = bytes_to_pil(content)
    except Exception:
        raise HTTPException(400, "Could not read image. File may be corrupted.")

    try:
        result = run_inference(pil_image)
    except RuntimeError as e:
        raise HTTPException(503, str(e))
    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(500, "Analysis failed. Please try again.")

    return {
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "explanation": generate_explanations(result["verdict"], result["confidence"], "image"),
        "file_type": "image",
        "file_name": file.filename,
        "frames_analyzed": None,
        "frame_breakdown": None,
    }


@app.post("/analyze/video")
async def analyze_video(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(400, "File must be a video.")

    content = await file.read()
    if len(content) > MAX_VIDEO:
        raise HTTPException(400, "Video too large. Maximum 100MB.")

    try:
        frames = extract_frames(content, num_frames=8)
    except Exception as e:
        logger.error(f"Frame extraction: {e}")
        raise HTTPException(400, "Could not process video.")

    if not frames:
        raise HTTPException(400, "Could not extract frames from video.")

    frame_results = []
    for i, frame in enumerate(frames):
        try:
            frame_results.append(run_inference(frame))
        except Exception as e:
            logger.warning(f"Frame {i} failed: {e}")

    if not frame_results:
        raise HTTPException(500, "Frame analysis failed.")

    total = len(frame_results)
    fake_n = sum(1 for r in frame_results if r["verdict"] == "FAKE")
    susp_n = sum(1 for r in frame_results if r["verdict"] == "SUSPICIOUS")

    if fake_n / total >= 0.5:
        final_verdict = "FAKE"
    elif (fake_n + susp_n) / total >= 0.5:
        final_verdict = "SUSPICIOUS"
    else:
        final_verdict = "REAL"

    avg_conf = round(sum(r["confidence"] for r in frame_results) / total)

    return {
        "verdict": final_verdict,
        "confidence": avg_conf,
        "explanation": generate_explanations(final_verdict, avg_conf, "video"),
        "file_type": "video",
        "file_name": file.filename,
        "frames_analyzed": total,
        "frame_breakdown": [
            {"frame": i + 1, "verdict": r["verdict"], "confidence": r["confidence"]}
            for i, r in enumerate(frame_results)
        ],
    }
