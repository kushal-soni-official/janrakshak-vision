"""
AI Model loading and inference — JanRakshak Vision
Team: Anonymous Group | Leader: Kushal Soni
Tradition Hacks 2026

ENSEMBLE APPROACH (2 models):
  Model A: umm-maybe/AI-image-detector      → General AI-generated image detection
  Model B: dima806/deepfake_vs_real_image_detection → Face deepfake detection
  
  Logic: Run both → take MORE suspicious result → accurate for faces AND scenic/fantasy AI images
"""

from transformers import pipeline
from PIL import Image
import logging

logger = logging.getLogger(__name__)

_pipe_general = None   # General AI image detector (non-face: pandal, donation images etc.)
_pipe_face    = None   # Face deepfake detector

GENERAL_MODEL = "umm-maybe/AI-image-detector"
FACE_MODEL    = "dima806/deepfake_vs_real_image_detection"
FACE_FALLBACK = "prithivMLmods/Deepfake-vs-Real-Image-Classification"


def preload_model():
    global _pipe_general, _pipe_face
    _pipe_general = _load_general()
    _pipe_face    = _load_face()
    return _pipe_general is not None or _pipe_face is not None


def _load_general():
    try:
        logger.info(f"Loading general AI detector: {GENERAL_MODEL}")
        pipe = pipeline("image-classification", model=GENERAL_MODEL, device="cpu", top_k=None)
        logger.info(f"✅ General model loaded")
        return pipe
    except Exception as e:
        logger.warning(f"General model failed: {e}")
        return None


def _load_face():
    for model_id in [FACE_MODEL, FACE_FALLBACK]:
        try:
            logger.info(f"Loading face deepfake detector: {model_id}")
            pipe = pipeline("image-classification", model=model_id, device="cpu", top_k=None)
            logger.info(f"✅ Face model loaded: {model_id}")
            return pipe
        except Exception as e:
            logger.warning(f"Face model {model_id} failed: {e}")
    return None


def get_pipes():
    global _pipe_general, _pipe_face
    if _pipe_general is None:
        _pipe_general = _load_general()
    if _pipe_face is None:
        _pipe_face = _load_face()
    return _pipe_general, _pipe_face


def _preprocess(pil_image: Image.Image) -> Image.Image:
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    if max(pil_image.size) > 1024:
        pil_image.thumbnail((1024, 1024), Image.LANCZOS)
    return pil_image


def _parse_scores(raw: list) -> dict:
    """Normalize raw pipeline output to {FAKE: float, REAL: float}"""
    scores = {}
    for item in raw:
        label = item['label'].upper()
        score = item['score']
        if any(x in label for x in ['FAKE', 'AI', 'GENERATED', 'ARTIFICIAL', 'MANIPULATED', 'DEEPFAKE', 'MACHINE']):
            scores['FAKE'] = max(scores.get('FAKE', 0), score)
        elif any(x in label for x in ['REAL', 'AUTHENTIC', 'GENUINE', 'ORIGINAL', 'HUMAN', 'NATURAL']):
            scores['REAL'] = max(scores.get('REAL', 0), score)

    # Normalize if both missing
    if not scores:
        scores = {'FAKE': 0.5, 'REAL': 0.5}
    elif 'FAKE' not in scores:
        scores['FAKE'] = 1.0 - scores.get('REAL', 0.5)
    elif 'REAL' not in scores:
        scores['REAL'] = 1.0 - scores.get('FAKE', 0.5)
    return scores


def _verdict_from_fake_score(fake_score: float, confidence_override: int = None) -> dict:
    """
    Thresholds (tuned for ensemble):
      FAKE       : fake_score >= 0.65
      SUSPICIOUS : fake_score >= 0.35
      REAL       : fake_score < 0.35
    """
    if fake_score >= 0.65:
        verdict = "FAKE"
        confidence = confidence_override or round(fake_score * 100)
    elif fake_score >= 0.35:
        verdict = "SUSPICIOUS"
        confidence = confidence_override or round(fake_score * 100)
    else:
        verdict = "REAL"
        confidence = confidence_override or round((1 - fake_score) * 100)
    return {"verdict": verdict, "confidence": confidence,
            "fake_score": round(fake_score, 4), "real_score": round(1 - fake_score, 4)}


def run_inference(pil_image: Image.Image) -> dict:
    """
    ENSEMBLE: Run general + face models, take MORE suspicious result.
    This catches:
      - AI-generated scenic/fantasy images (Gemini, Midjourney, DALL-E)
      - Face deepfakes / face swaps
      - Celebrity manipulated photos
      - AI pandal / donation scam images
    """
    pipe_general, pipe_face = get_pipes()
    if pipe_general is None and pipe_face is None:
        raise RuntimeError("No models available. Please try again later.")

    img = _preprocess(pil_image)

    results = []

    # Model A: General AI detector
    if pipe_general is not None:
        try:
            raw_g = pipe_general(img)
            scores_g = _parse_scores(raw_g)
            fake_g = scores_g.get('FAKE', 0)
            results.append(('general', fake_g))
            logger.info(f"General model → fake={fake_g:.3f}")
        except Exception as e:
            logger.warning(f"General model inference failed: {e}")

    # Model B: Face deepfake detector
    if pipe_face is not None:
        try:
            raw_f = pipe_face(img)
            scores_f = _parse_scores(raw_f)
            fake_f = scores_f.get('FAKE', 0)
            results.append(('face', fake_f))
            logger.info(f"Face model   → fake={fake_f:.3f}")
        except Exception as e:
            logger.warning(f"Face model inference failed: {e}")

    if not results:
        raise RuntimeError("All models failed on this image.")

    if len(results) == 1:
        # Only one model succeeded — use it directly
        _, fake_score = results[0]
    else:
        # ENSEMBLE: weighted combination
        # General model gets higher weight for overall AI detection
        # Face model gets higher weight when general says uncertain (0.35-0.65)
        fake_general = dict(results).get('general', 0.5)
        fake_face    = dict(results).get('face', 0.5)

        # If general model strongly says AI (>0.7), trust it
        if fake_general >= 0.70:
            fake_score = fake_general * 0.7 + fake_face * 0.3
        # If face model strongly says fake face (>0.80), trust it
        elif fake_face >= 0.80:
            fake_score = fake_general * 0.3 + fake_face * 0.7
        else:
            # Balanced: take MAX (more suspicious wins)
            fake_score = max(fake_general, fake_face)

        logger.info(f"Ensemble → general={fake_general:.3f}, face={fake_face:.3f}, final={fake_score:.3f}")

    return _verdict_from_fake_score(fake_score)
