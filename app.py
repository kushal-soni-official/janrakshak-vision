"""
JanRakshak Vision — FastAPI Backend
AI Deepfake & AI-Generated Content Detection for Everyone
Team: Anonymous Group | Leader: Kushal Soni
Competition: Tradition Hacks 2026

Endpoints:
  GET  /              → Health check
  POST /analyze/image → Analyze image file (JPG, PNG, WEBP, GIF, BMP)
  POST /analyze/video → Analyze video via frame-by-frame majority vote (MP4, AVI, MOV, MKV)

Rate limiting: 10 requests/minute per IP (free tier protection)
Privacy: Zero-storage — all processing is RAM-only, no files written to disk.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import gc

from models import preload_model, run_inference
from utils import bytes_to_pil, extract_frames, generate_explanations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File size limits
MAX_IMAGE = 50 * 1024 * 1024   # 50MB
MAX_VIDEO = 100 * 1024 * 1024  # 100MB

# Supported MIME types
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/bmp"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/avi", "video/quicktime", "video/x-matroska", "video/x-msvideo"}

# Rate limiter (protects free-tier HuggingFace Spaces from abuse)
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🛡️ JanRakshak Vision API starting — Team: Anonymous Group | Leader: Kushal Soni")
    preload_model()
    logger.info("✅ All models loaded. API ready.")
    yield
    logger.info("🔄 Shutting down JanRakshak Vision API.")
    gc.collect()


app = FastAPI(
    title="JanRakshak Vision API",
    description=(
        "AI-powered deepfake and AI-generated content detection for everyone. "
        "Supports images (JPG, PNG, WEBP) and videos (MP4, AVI, MOV, MKV). "
        "Zero-storage policy — no files are saved. "
        "Built for Tradition Hacks 2026 by Team Anonymous Group (Leader: Kushal Soni)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Rate limit error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
        "endpoints": {
            "image": "POST /analyze/image",
            "video": "POST /analyze/video",
            "docs":  "GET  /docs",
        },
        "limits": {
            "image_max": "50MB",
            "video_max": "100MB",
            "rate_image": "10 requests/minute per IP",
            "rate_video": "5 requests/minute per IP",
        },
    }


@app.post("/analyze/image")
@limiter.limit("10/minute")
async def analyze_image(request: Request, file: UploadFile = File(...)):
    # Validate MIME type
    if not file.content_type or file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: '{file.content_type}'. Accepted: JPG, PNG, WEBP, GIF, BMP."
        )

    content = await file.read()

    # Validate file size
    if len(content) > MAX_IMAGE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(content) // (1024*1024)}MB). Maximum allowed: 50MB."
        )

    # Parse image
    try:
        pil_image = bytes_to_pil(content)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read the image. File may be corrupted or in an unsupported format."
        )
    finally:
        del content
        gc.collect()

    # Run AI inference
    try:
        result = run_inference(pil_image)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Image inference error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Analysis failed due to an internal error. Please try again."
        )

    return {
        "verdict":         result["verdict"],
        "confidence":      result["confidence"],
        "fake_score":      result["fake_score"],
        "real_score":      result["real_score"],
        "explanation":     generate_explanations(result["verdict"], result["confidence"], "image"),
        "file_type":       "image",
        "file_name":       file.filename,
        "frames_analyzed": None,
        "frame_breakdown": None,
        "model_votes":     result.get("model_votes", []),
    }


@app.post("/analyze/video")
@limiter.limit("5/minute")
async def analyze_video(request: Request, file: UploadFile = File(...)):
    # Validate MIME type
    if not file.content_type or file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: '{file.content_type}'. Accepted: MP4, AVI, MOV, MKV."
        )

    content = await file.read()

    # Validate file size
    if len(content) > MAX_VIDEO:
        raise HTTPException(
            status_code=413,
            detail=f"Video too large ({len(content) // (1024*1024)}MB). Maximum allowed: 100MB."
        )

    # Extract video frames
    try:
        frames = extract_frames(content, num_frames=8)
    except Exception as e:
        logger.error(f"Frame extraction error: {e}")
        raise HTTPException(
            status_code=400,
            detail="Could not process the video. File may be corrupted or codec unsupported."
        )
    finally:
        del content
        gc.collect()

    if not frames:
        raise HTTPException(
            status_code=400,
            detail="Could not extract frames from the video. Try a shorter clip or different format."
        )

    # Run inference on each frame
    frame_results = []
    for i, frame in enumerate(frames):
        try:
            frame_results.append(run_inference(frame))
        except Exception as e:
            logger.warning(f"Frame {i+1} inference failed: {e}")

    if not frame_results:
        raise HTTPException(
            status_code=500,
            detail="All frame analyses failed. Please try again with a different video."
        )

    # Majority-vote verdict across frames
    total   = len(frame_results)
    fake_n  = sum(1 for r in frame_results if r["verdict"] == "FAKE")
    susp_n  = sum(1 for r in frame_results if r["verdict"] == "SUSPICIOUS")

    if fake_n / total >= 0.5:
        final_verdict = "FAKE"
    elif (fake_n + susp_n) / total >= 0.5:
        final_verdict = "SUSPICIOUS"
    else:
        final_verdict = "REAL"

    avg_fake_score = round(sum(r["fake_score"] for r in frame_results) / total, 4)
    avg_conf = round(sum(r["confidence"] for r in frame_results) / total)
    logger.info(f"Video verdict: {final_verdict} ({avg_conf}%) — {total} frames, {fake_n} FAKE, {susp_n} SUSPICIOUS")

    return {
        "verdict":         final_verdict,
        "confidence":      avg_conf,
        "fake_score":      avg_fake_score,
        "real_score":      round(1 - avg_fake_score, 4),
        "explanation":     generate_explanations(final_verdict, avg_conf, "video"),
        "file_type":       "video",
        "file_name":       file.filename,
        "frames_analyzed": total,
        "frame_breakdown": [
            {
                "frame":       i + 1,
                "verdict":     r["verdict"],
                "confidence":  r["confidence"],
                "fake_score":  r.get("fake_score"),
                "model_votes": r.get("model_votes", []),
            }
            for i, r in enumerate(frame_results)
        ],
        "model_votes": [],  # Aggregate not meaningful for video; see frame_breakdown
    }
