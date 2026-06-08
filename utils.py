"""
Utilities — JanRakshak Vision Backend
Image processing, video frame extraction, multilingual explanations
Team: Anonymous Group | Leader: Kushal Soni
"""

from PIL import Image
import cv2, numpy as np, io, os, tempfile, logging

logger = logging.getLogger(__name__)


def bytes_to_pil(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(data))


def extract_frames(video_bytes: bytes, num_frames: int = 8) -> list:
    """Extract evenly-spaced frames from video as PIL Images."""
    tmp_path, frames = None, []
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            tmp.write(video_bytes)
            tmp_path = tmp.name

        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            logger.error("OpenCV: cannot open video")
            return frames

        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        logger.info(f"Video: {total} frames @ {cap.get(cv2.CAP_PROP_FPS):.1f} FPS")
        if total <= 0:
            return frames

        start, end = int(total * 0.05), int(total * 0.95)
        step = max(1, (end - start) // num_frames)
        indices = list(range(start, end, step))[:num_frames]

        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        cap.release()
        logger.info(f"Extracted {len(frames)} frames")
    except Exception as e:
        logger.error(f"Frame extraction error: {e}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
    return frames


def generate_explanations(verdict: str, confidence: int, file_type: str = "image") -> dict:
    """Generate human-readable explanations in EN, HI, BN."""
    t = {
        "image": {"en": "image", "hi": "तस्वीर", "bn": "ছবি"},
        "video": {"en": "video", "hi": "वीडियो", "bn": "ভিডিও"},
    }.get(file_type, {"en": "image", "hi": "तस्वीर", "bn": "ছবি"})

    expl = {
        "FAKE": {
            "en": f"This {t['en']} shows {confidence}% signs of AI manipulation. It was likely created or edited by AI tools. Do not trust or share this content.",
            "hi": f"इस {t['hi']} में {confidence}% AI हेरफेर के संकेत हैं। यह AI टूल्स से बनाई या बदली गई हो सकती है। इस पर विश्वास न करें और शेयर न करें।",
            "bn": f"এই {t['bn']}তে {confidence}% AI কারসাজির লক্ষণ দেখা যাচ্ছে। এটি AI টুলস দিয়ে তৈরি বা পরিবর্তন করা হতে পারে। বিশ্বাস করবেন না বা শেয়ার করবেন না।",
        },
        "SUSPICIOUS": {
            "en": f"This {t['en']} shows unusual patterns ({confidence}% confidence). It may have been partially modified. Verify from a trusted source before sharing.",
            "hi": f"इस {t['hi']} में कुछ असामान्य पैटर्न हैं ({confidence}% विश्वास)। यह आंशिक रूप से बदली गई हो सकती है। शेयर करने से पहले पुष्टि करें।",
            "bn": f"এই {t['bn']}তে কিছু অস্বাভাবিক প্যাটার্ন রয়েছে ({confidence}% আত্মবিশ্বাস)। শেয়ার করার আগে বিশ্বস্ত সূত্র থেকে নিশ্চিত করুন।",
        },
        "REAL": {
            "en": f"This {t['en']} appears authentic ({confidence}% confidence). No clear signs of AI manipulation detected. Always stay cautious with viral content.",
            "hi": f"यह {t['hi']} असली लगती है ({confidence}% विश्वास)। AI हेरफेर के कोई स्पष्ट संकेत नहीं मिले। फिर भी वायरल सामग्री से सावधान रहें।",
            "bn": f"এই {t['bn']}টি আসল বলে মনে হচ্ছে ({confidence}% আত্মবিশ্বাস)। AI কারসাজির কোনো স্পষ্ট লক্ষণ পাওয়া যায়নি। তবুও সতর্ক থাকুন।",
        },
    }
    return expl.get(verdict, expl["SUSPICIOUS"])
