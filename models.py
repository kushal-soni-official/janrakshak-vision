"""
AI Model loading and inference — JanRakshak Vision
Team: Anonymous Group | Leader: Kushal Soni
Tradition Hacks 2026

PRIMARY:  dima806/deepfake_vs_real_image_detection (EfficientNetB0)
FALLBACK: prithivMLmods/Deepfake-vs-Real-Image-Classification
"""

from transformers import pipeline
from PIL import Image
import logging

logger = logging.getLogger(__name__)

_pipe = None
PRIMARY_MODEL  = "dima806/deepfake_vs_real_image_detection"
FALLBACK_MODEL = "prithivMLmods/Deepfake-vs-Real-Image-Classification"


def preload_model():
    global _pipe
    _pipe = _load_model()
    return _pipe is not None


def _load_model():
    for model_id in [PRIMARY_MODEL, FALLBACK_MODEL]:
        try:
            logger.info(f"Loading model: {model_id}")
            pipe = pipeline("image-classification", model=model_id, device="cpu", top_k=None)
            logger.info(f"✅ Model loaded: {model_id}")
            return pipe
        except Exception as e:
            logger.warning(f"Failed {model_id}: {e}")
    logger.error("❌ All models failed")
    return None


def get_pipeline():
    global _pipe
    if _pipe is None:
        _pipe = _load_model()
    return _pipe


def run_inference(pil_image: Image.Image) -> dict:
    """
    Returns: { verdict, confidence, fake_score, real_score }
    Thresholds: FAKE >= 80%, SUSPICIOUS 45-79%, REAL < 45% fake score
    """
    pipe = get_pipeline()
    if pipe is None:
        raise RuntimeError("Model unavailable. Please try again later.")

    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    if max(pil_image.size) > 1024:
        pil_image.thumbnail((1024, 1024), Image.LANCZOS)

    raw = pipe(pil_image)
    scores = {}
    for item in raw:
        label = item['label'].upper()
        if any(x in label for x in ['FAKE', 'AI', 'GENERATED', 'MANIPULATED', 'DEEPFAKE']):
            scores['FAKE'] = max(scores.get('FAKE', 0), item['score'])
        elif any(x in label for x in ['REAL', 'AUTHENTIC', 'GENUINE', 'ORIGINAL']):
            scores['REAL'] = max(scores.get('REAL', 0), item['score'])

    fake_score = scores.get('FAKE', 0)
    real_score = scores.get('REAL', 0)
    if fake_score == 0 and real_score == 0:
        fake_score = real_score = 0.5

    if fake_score >= 0.80:
        verdict, confidence = "FAKE", round(fake_score * 100)
    elif fake_score >= 0.45:
        verdict, confidence = "SUSPICIOUS", round(fake_score * 100)
    else:
        verdict, confidence = "REAL", round(real_score * 100)

    return {"verdict": verdict, "confidence": confidence,
            "fake_score": round(fake_score, 4), "real_score": round(real_score, 4)}
