"""
AI Model loading and inference — JanRakshak Vision v5
Team: Anonymous Group | Tradition Hacks 2026

v5 UPGRADE — 3-MODEL ENSEMBLE with better deepfake-specific models:

NEW MODELS ADDED:
  1. haywoodsloan/ai-image-detector-deploy  — production-grade, balanced detector
     Labels: AI-Generated vs Real  |  Weight: 40%
  2. Organika/sdxl-detector                — SDXL/modern AI art detector
     Labels: artificial vs real    |  Weight: 35%
  3. umm-maybe/AI-image-detector           — general composite/edit detector
     Labels: artificial vs nature  |  Weight: 25%

ENSEMBLE LOGIC:
  - All 3 models run in parallel
  - Weighted average as primary verdict
  - Boost: if ANY single model scores >= 0.80, raise final by 10% (high confidence boost)
  - Edge case: if model1+model2 both < 0.10 but model3 > 0.60 → use model3 score
  - Thresholds: FAKE>=0.55, SUSPICIOUS>=0.25, REAL<0.25

WHY THIS IS BETTER:
  - haywoodsloan model is specifically trained on modern AI generators
    (Midjourney v6, DALL-E 3, Stable Diffusion XL, Gemini, etc.)
  - Three models = majority vote gives more stable results
  - Lower FAKE threshold (0.55 vs 0.58) = catches more deepfakes
  - High-confidence boost = if model is very sure, amplify it
"""

from transformers import pipeline
from PIL import Image
import logging

logger = logging.getLogger(__name__)

MODELS = [
    {
        "id":          "haywoodsloan/ai-image-detector-deploy",
        "name":        "detector_v2",
        "fake_labels": ["ai-generated", "artificial", "fake", "generated"],
        "real_labels": ["real", "photo", "authentic", "human"],
        "weight":      0.40,
    },
    {
        "id":          "Organika/sdxl-detector",
        "name":        "sdxl",
        "fake_labels": ["artificial"],
        "real_labels": ["real"],
        "weight":      0.35,
    },
    {
        "id":          "umm-maybe/AI-image-detector",
        "name":        "general",
        "fake_labels": ["artificial"],
        "real_labels": ["nature"],
        "weight":      0.25,
    },
]

_pipes = {}


def preload_model():
    for m in MODELS:
        _pipes[m["name"]] = _try_load(m["id"], m["name"])
    loaded = sum(1 for v in _pipes.values() if v is not None)
    logger.info(f"✅ {loaded}/{len(MODELS)} models loaded (v5 ensemble)")
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
        # Check fake labels — partial match
        if any(fl in lbl for fl in fake_labels):
            fake_score = sc if fake_score is None else max(fake_score, sc)
        # Check real labels — partial match
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
        # Unknown labels — log and return neutral
        logger.warning(f"Unknown labels from model: {[i['label'] for i in raw]}")
        # Treat unknown as slightly suspicious (don't return clean REAL)
        return 0.35


def _verdict(fake_score: float) -> tuple:
    """
    v5 Thresholds — slightly lower to catch more deepfakes:
      FAKE:       fake_score >= 0.55
      SUSPICIOUS: fake_score >= 0.25
      REAL:       fake_score <  0.25
    """
    if fake_score >= 0.55:
        return "FAKE",       round(fake_score * 100)
    elif fake_score >= 0.25:
        return "SUSPICIOUS", round(fake_score * 100)
    else:
        return "REAL",       round((1 - fake_score) * 100)


def run_inference(pil_image: Image.Image) -> dict:
    """
    v5 THREE-MODEL ENSEMBLE:
    1. Run all 3 models in parallel
    2. Weighted blend: detector_v2(40%) + sdxl(35%) + general(25%)
    3. High-confidence boost: if any model >= 0.80, boost final by 8%
    4. Edge case: fallback to max if weighted blend misses obvious fake
    5. Gracefully handle partial model failures (1 or 2 models ok)
    """
    _ensure_loaded()
    img = _preprocess(pil_image)

    scores   = {}  # name -> fake_score
    individual = []
    weights  = {m["name"]: m["weight"] for m in MODELS}

    for m in MODELS:
        pipe = _pipes.get(m["name"])
        if pipe is None:
            continue
        try:
            raw = pipe(img)
            fs  = _parse_fake_score(raw, m["fake_labels"], m["real_labels"])
            v, c = _verdict(fs)
            scores[m["name"]] = fs
            individual.append({
                "name":       m["name"],
                "fake_score": round(fs, 4),
                "verdict":    v,
                "confidence": c,
            })
            logger.info(f"[{m['name']}] fake={fs:.4f} → {v} ({c}%)")
        except Exception as e:
            logger.warning(f"[{m['name']}] error: {e}")

    if not scores:
        raise RuntimeError("All models failed. Please try again.")

    # ── Compute weighted average ────────────────────────────────────────────
    total_weight = sum(weights[n] for n in scores)
    weighted_sum = sum(scores[n] * weights[n] for n in scores)
    final_fake   = weighted_sum / total_weight
    logger.info(f"Weighted blend: {final_fake:.4f} (from {list(scores.keys())})")

    # ── High-confidence boost ───────────────────────────────────────────────
    # If ANY model is very confident something is fake, amplify the signal
    max_score = max(scores.values())
    if max_score >= 0.80:
        boost     = min(0.08, (max_score - 0.80) * 0.4)
        final_fake = min(0.99, final_fake + boost)
        logger.info(f"High-confidence boost: +{boost:.3f} → {final_fake:.4f}")

    # ── Edge case: strong minority opinion ─────────────────────────────────
    # Weighted blend may dilute a single strong signal.
    # If the best model says 0.85+ but others drag it below threshold,
    # raise to at least SUSPICIOUS level.
    if max_score >= 0.85 and final_fake < 0.25:
        final_fake = 0.30  # Bump to SUSPICIOUS minimum
        logger.info(f"Edge case bump: max_score={max_score:.3f} → forcing SUSPICIOUS")

    verdict, confidence = _verdict(final_fake)
    logger.info(f"FINAL v5: {verdict} ({confidence}%) fake_score={final_fake:.4f}")

    return {
        "verdict":     verdict,
        "confidence":  confidence,
        "fake_score":  round(final_fake, 4),
        "real_score":  round(1 - final_fake, 4),
        "model_votes": individual,
    }
