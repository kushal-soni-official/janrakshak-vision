"""
AI Model loading and inference — JanRakshak Vision v4
Team: Anonymous Group | Leader: Kushal Soni | Tradition Hacks 2026

DATA-DRIVEN ENSEMBLE (from real test results):

Test results on 6 images:
  Model         AI-art  Scenic  Anime  Edited  Screenshot
  general       0.21    0.51    0.51   0.92    0.80 (false+)
  sdxl          0.0002  0.785   0.056  0.87    0.33 (good!)
  face          0.08    0.29    0.009  0.002   0.17 (useless)

Strategy:
  - REMOVE face model (noise, always near-zero for non-face)
  - PRIMARY = sdxl (reliable, low false positives)
  - SECONDARY = general (catches edited photos but erratic)
  - BLEND: 70% sdxl + 30% general
  - If sdxl < 0.1 AND general > 0.5 → use MAX (catch missed edits)
  - THRESHOLDS: FAKE>=0.58, SUSPICIOUS>=0.28, else REAL
"""

from transformers import pipeline
from PIL import Image
import logging

logger = logging.getLogger(__name__)

# Only 2 models now — face model removed (proven useless from testing)
MODELS = [
    {
        "id":   "Organika/sdxl-detector",
        "name": "sdxl",
        "fake_labels": ["artificial"],
        "real_labels": ["real"],
        "weight": 0.70,
    },
    {
        "id":   "umm-maybe/AI-image-detector",
        "name": "general",
        "fake_labels": ["artificial"],
        "real_labels": ["nature"],
        "weight": 0.30,
    },
]

_pipes = {}


def preload_model():
    for m in MODELS:
        _pipes[m["name"]] = _try_load(m["id"], m["name"])
    loaded = sum(1 for v in _pipes.values() if v is not None)
    logger.info(f"✅ {loaded}/{len(MODELS)} models loaded")
    return loaded > 0


def _try_load(model_id: str, name: str):
    try:
        logger.info(f"Loading [{name}]: {model_id}")
        pipe = pipeline("image-classification", model=model_id,
                        device="cpu", top_k=None)
        logger.info(f"✅ [{name}] ready")
        return pipe
    except Exception as e:
        logger.warning(f"❌ [{name}] failed: {e}")
        return None


def _ensure_loaded():
    for m in MODELS:
        if m["name"] not in _pipes:
            _pipes[m["name"]] = _try_load(m["id"], m["name"])


def _preprocess(img: Image.Image) -> Image.Image:
    if img.mode != "RGB":
        img = img.convert("RGB")
    if max(img.size) > 1024:
        img.thumbnail((1024, 1024), Image.LANCZOS)
    return img


def _parse_fake_score(raw: list, fake_labels: list, real_labels: list) -> float:
    """Extract fake probability using model-specific label lists (case-insensitive)."""
    fake_score = None
    real_score = None
    for item in raw:
        lbl = item["label"].lower().strip()
        sc  = item["score"]
        if any(fl in lbl for fl in fake_labels):
            fake_score = sc if fake_score is None else max(fake_score, sc)
        elif any(rl in lbl for rl in real_labels):
            real_score = sc if real_score is None else max(real_score, sc)

    if fake_score is not None and real_score is not None:
        total = fake_score + real_score
        return fake_score / total if total > 0 else 0.5
    elif fake_score is not None:
        return fake_score
    elif real_score is not None:
        return 1.0 - real_score
    else:
        logger.warning(f"Unknown labels: {[i['label'] for i in raw]}")
        return 0.5


def _verdict(fake_score: float) -> tuple:
    """
    Tuned thresholds based on real test data:
      FAKE:       fake_score >= 0.58
      SUSPICIOUS: fake_score >= 0.28
      REAL:       fake_score <  0.28
    """
    if fake_score >= 0.58:
        return "FAKE",       round(fake_score * 100)
    elif fake_score >= 0.28:
        return "SUSPICIOUS", round(fake_score * 100)
    else:
        return "REAL",       round((1 - fake_score) * 100)


def run_inference(pil_image: Image.Image) -> dict:
    """
    DATA-DRIVEN ENSEMBLE:
    1. Run sdxl (primary, weight=0.70) + general (secondary, weight=0.30)
    2. Blend: 70% sdxl + 30% general
    3. Edge case: if sdxl very confident REAL (<0.10) but general strongly says FAKE (>0.55)
       → use MAX to avoid missing edited real photos (Joker/composite case)
    4. Fallback: if only one model runs, use it directly
    """
    _ensure_loaded()
    img = _preprocess(pil_image)

    scores = {}   # name -> fake_score
    individual = []

    for m in MODELS:
        pipe = _pipes.get(m["name"])
        if pipe is None:
            continue
        try:
            raw = pipe(img)
            fs  = _parse_fake_score(raw, m["fake_labels"], m["real_labels"])
            v, c = _verdict(fs)
            scores[m["name"]] = fs
            individual.append({"name": m["name"], "fake_score": round(fs, 4), "verdict": v, "confidence": c})
            logger.info(f"[{m['name']}] fake={fs:.4f} → {v} ({c}%)")
        except Exception as e:
            logger.warning(f"[{m['name']}] error: {e}")

    if not scores:
        raise RuntimeError("All models failed. Please try again.")

    if len(scores) == 1:
        # Only one model available — use it
        name, fs = next(iter(scores.items()))
        final_fake = fs
    else:
        sdxl_score    = scores.get("sdxl", 0.5)
        general_score = scores.get("general", 0.5)

        # Edge case: sdxl very confident REAL but general strongly says FAKE
        # (catches composite edits like Joker + Thanos gauntlet)
        if sdxl_score < 0.10 and general_score > 0.55:
            # Trust general more — use MAX
            final_fake = max(sdxl_score, general_score)
            logger.info(f"Edge case: sdxl={sdxl_score:.3f} vs general={general_score:.3f} → MAX={final_fake:.3f}")
        else:
            # Standard blend: 70% sdxl + 30% general
            final_fake = 0.70 * sdxl_score + 0.30 * general_score
            logger.info(f"Blend: 0.7*{sdxl_score:.3f} + 0.3*{general_score:.3f} = {final_fake:.3f}")

    verdict, confidence = _verdict(final_fake)

    logger.info(f"FINAL: {verdict} ({confidence}%) fake_score={final_fake:.4f}")

    return {
        "verdict":     verdict,
        "confidence":  confidence,
        "fake_score":  round(final_fake, 4),
        "real_score":  round(1 - final_fake, 4),
        "model_votes": individual,
    }
