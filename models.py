"""
AI Model loading and inference — JanRakshak Vision v3
Team: Anonymous Group | Leader: Kushal Soni | Tradition Hacks 2026

3-MODEL ENSEMBLE with model-specific label parsers:
  Model 1: umm-maybe/AI-image-detector      labels: "artificial" / "nature"
  Model 2: Organika/sdxl-detector            labels: "artificial" / "real"
  Model 3: dima806/deepfake_vs_real_image_detection  labels: "Fake" / "Real"

VOTING: Majority vote on verdict, weighted by individual confidence
"""

from transformers import pipeline
from PIL import Image
import logging

logger = logging.getLogger(__name__)

# ── Model registry ─────────────────────────────────────────────────────────────
MODELS = [
    {
        "id":   "umm-maybe/AI-image-detector",
        "name": "general",
        "fake_labels": ["artificial"],
        "real_labels": ["nature"],
    },
    {
        "id":   "Organika/sdxl-detector",
        "name": "sdxl",
        "fake_labels": ["artificial"],
        "real_labels": ["real"],
    },
    {
        "id":   "dima806/deepfake_vs_real_image_detection",
        "name": "face",
        "fake_labels": ["fake"],
        "real_labels": ["real"],
    },
]

_pipes = {}   # name -> pipeline or None


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
    """
    Extract fake probability using model-specific label lists.
    Labels are matched case-insensitively.
    Returns float in [0, 1].
    """
    fake_score = None
    real_score = None

    for item in raw:
        label_lower = item["label"].lower().strip()
        score = item["score"]

        if any(fl in label_lower for fl in fake_labels):
            fake_score = score if fake_score is None else max(fake_score, score)
        elif any(rl in label_lower for rl in real_labels):
            real_score = score if real_score is None else max(real_score, score)

    # Resolve
    if fake_score is not None and real_score is not None:
        # Normalize (in case model doesn't sum to 1)
        total = fake_score + real_score
        return fake_score / total if total > 0 else 0.5
    elif fake_score is not None:
        return fake_score
    elif real_score is not None:
        return 1.0 - real_score
    else:
        logger.warning(f"Could not parse labels: {[i['label'] for i in raw]}")
        return 0.5   # Unknown → treat as uncertain


def _verdict(fake_score: float) -> tuple:
    """Returns (verdict_str, confidence_int)"""
    if fake_score >= 0.65:
        return "FAKE", round(fake_score * 100)
    elif fake_score >= 0.38:
        return "SUSPICIOUS", round(fake_score * 100)
    else:
        return "REAL", round((1 - fake_score) * 100)


def run_inference(pil_image: Image.Image) -> dict:
    """
    Run all 3 models, collect fake scores, then:
    1. Majority vote on verdict
    2. Weighted confidence by number of agreeing models
    3. If tie → take the most suspicious (safer for a safety tool)
    """
    _ensure_loaded()
    img = _preprocess(pil_image)

    individual = []   # list of {name, fake_score, verdict, confidence}

    for m in MODELS:
        pipe = _pipes.get(m["name"])
        if pipe is None:
            continue
        try:
            raw = pipe(img)
            fs = _parse_fake_score(raw, m["fake_labels"], m["real_labels"])
            v, c = _verdict(fs)
            individual.append({
                "name": m["name"],
                "fake_score": round(fs, 4),
                "verdict": v,
                "confidence": c,
            })
            logger.info(f"[{m['name']}] fake={fs:.3f} → {v} ({c}%)")
        except Exception as e:
            logger.warning(f"[{m['name']}] inference error: {e}")

    if not individual:
        raise RuntimeError("All models failed. Please try again later.")

    # ── Voting ──────────────────────────────────────────────────────────────
    counts = {"FAKE": 0, "SUSPICIOUS": 0, "REAL": 0}
    score_sum = {"FAKE": 0.0, "SUSPICIOUS": 0.0, "REAL": 0.0}

    for r in individual:
        counts[r["verdict"]] += 1
        score_sum[r["verdict"]] += r["fake_score"]

    # Pick winner by majority; tie-break: most suspicious wins (safety tool)
    verdict_order = ["FAKE", "SUSPICIOUS", "REAL"]
    winner = max(verdict_order, key=lambda v: (counts[v], -verdict_order.index(v)))

    # Final fake_score = average of scores from WINNING models
    winners = [r for r in individual if r["verdict"] == winner]
    avg_fake = sum(r["fake_score"] for r in winners) / len(winners)

    # Blend in minority scores slightly (10% each) for smoother confidence
    others = [r for r in individual if r["verdict"] != winner]
    if others:
        minority_avg = sum(r["fake_score"] for r in others) / len(others)
        avg_fake = avg_fake * 0.85 + minority_avg * 0.15

    _, final_conf = _verdict(avg_fake)

    logger.info(f"ENSEMBLE: {counts} → {winner} ({final_conf}%) fake={avg_fake:.3f}")

    return {
        "verdict":    winner,
        "confidence": final_conf,
        "fake_score": round(avg_fake, 4),
        "real_score": round(1 - avg_fake, 4),
        "model_votes": individual,   # debug info in response
    }
