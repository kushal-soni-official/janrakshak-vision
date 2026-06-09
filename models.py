"""
JanRakshak Vision v7 — models.py
Weighted Multi-Model Ensemble for AI-generated image & deepfake detection.

ENSEMBLE:
  1. Multi-Model Weighted Ensemble (3 specialized brains)
     - detector_v2 (35%): Generative AI expert (Midjourney v6, DALL-E 3, Gemini)
     - sdxl (35%): AI texture / artifact expert (noise patterns, lighting anomalies)
     - general (30%): Composite / Edit expert (face-swaps, Photoshop manipulation)

  2. Smart Heuristic Engine v7:
     - High-Confidence Amplifier: If any model is >85% fake, boost final score.
     - Composite Protection Floor: If 'general' detects edit >70%, floor to SUSPICIOUS.
     - Screenshot & Digital Art Filter: Dual-check using unique color count + pixel
       variance analysis. Dampens fake score for UI screenshots to eliminate false
       positives while keeping sensitivity on real photos with low-light palettes.

Built by: Kushal Soni (Team Leader) | Team: Anonymous Group
Competition: Tradition Hacks 2026 | Hosted: Hugging Face Spaces (CPU)
"""

from transformers import pipeline
from PIL import Image, ImageStat
import logging
import gc

logger = logging.getLogger(__name__)

MODELS = [
    {
        "id":          "haywoodsloan/ai-image-detector-deploy",
        "name":        "detector_v2",
        "fake_labels": ["ai-generated", "artificial", "fake", "generated"],
        "real_labels": ["real", "photo", "authentic", "human"],
        "weight":      0.35,
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
        "weight":      0.30,
    },
]

_pipes = {}


def preload_model():
    for m in MODELS:
        _pipes[m["name"]] = _try_load(m["id"], m["name"])
    loaded = sum(1 for v in _pipes.values() if v is not None)
    logger.info(f"✅ {loaded}/{len(MODELS)} models loaded (v7)")
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


def _is_digital_ui_or_screenshot(img: Image.Image) -> bool:
    """
    Dual-signal screenshot detection:
    1. Unique color count on 256x256 thumbnail (<2000 = very uniform = likely UI/clipart)
    2. Pixel variance check — real photographs have high std-dev; flat UI has near-zero variance

    Why dual-check:
    - Color count alone misfires on dark/low-light photos and heavy JPEG compression.
    - Variance alone can misfire on solid-background product shots.
    - Both signals agreeing = high confidence it's a non-photographic image.
    """
    try:
        small = img.copy()
        small.thumbnail((256, 256))

        # Signal 1: Unique color count
        colors = small.getcolors(maxcolors=65536)
        num_colors = len(colors) if colors is not None else 65536
        logger.info(f"Color count: {num_colors}")

        # Signal 2: Pixel variance (real photos: stddev > 30; flat UI: < 10)
        stat = ImageStat.Stat(small)
        # Average std deviation across R, G, B channels
        avg_stddev = sum(stat.stddev[:3]) / 3
        logger.info(f"Pixel stddev: {avg_stddev:.2f}")

        # Both signals must agree to be called a screenshot
        # Low color count alone is not enough (dark photos can be low)
        if num_colors < 2000 and avg_stddev < 15:
            logger.info("Screenshot/UI detected via dual-signal check.")
            return True

        return False
    except Exception as e:
        logger.warning(f"UI detection failed: {e}")
        return False


def _parse_fake_score(raw: list, fake_labels: list, real_labels: list) -> float:
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
        return 0.35


def _verdict(fake_score: float) -> tuple:
    """
    v7 thresholds:
      FAKE:       >= 0.50
      SUSPICIOUS: >= 0.30
      REAL:       <  0.30
    """
    if fake_score >= 0.50:
        return "FAKE",       round(fake_score * 100)
    elif fake_score >= 0.30:
        return "SUSPICIOUS", round(fake_score * 100)
    else:
        return "REAL",       round((1 - fake_score) * 100)


def run_inference(pil_image: Image.Image) -> dict:
    _ensure_loaded()
    img = _preprocess(pil_image)
    is_ui = _is_digital_ui_or_screenshot(img)

    scores   = {}
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
            logger.info(f"[{m['name']}] fake={fs:.4f} → {v}")
        except Exception as e:
            logger.warning(f"[{m['name']}] error: {e}")

    if not scores:
        raise RuntimeError("All models failed. Please try again.")

    # 1. Weighted Average
    total_weight = sum(weights[n] for n in scores)
    weighted_sum = sum(scores[n] * weights[n] for n in scores)
    final_fake   = weighted_sum / total_weight

    # 2. High-Confidence Amplifier
    max_score = max(scores.values())
    if max_score >= 0.85:
        boost = min(0.15, (max_score - 0.80) * 0.8)
        final_fake = min(0.99, final_fake + boost)

    # 3. Composite Edit Protection Floor
    # If Brain 3 (composite/edit expert) strongly flags manipulation but
    # the weighted average is low, force a SUSPICIOUS floor.
    # Threshold: >0.70 on general (previously was 0.60 — tightened to reduce false positives)
    general_score = scores.get("general", 0)
    if general_score >= 0.70 and final_fake < 0.35:
        final_fake = 0.35
        logger.info(f"Composite floor applied. general={general_score:.4f}")

    # 4. Screenshot / UI Filter (Dampener)
    if is_ui:
        logger.info("UI/Screenshot detected! Dampening fake score.")
        # Reduce fake score significantly for screenshots
        final_fake = final_fake * 0.40

    verdict, confidence = _verdict(final_fake)
    logger.info(f"FINAL v7: {verdict} ({confidence}%) fake_score={final_fake:.4f}")

    result = {
        "verdict":     verdict,
        "confidence":  confidence,
        "fake_score":  round(final_fake, 4),
        "real_score":  round(1 - final_fake, 4),
        "model_votes": individual,
    }

    # Explicit memory cleanup (GC is non-deterministic; force it)
    del img
    gc.collect()

    return result

