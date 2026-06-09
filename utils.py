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


def extract_frames(video_bytes: bytes, num_frames: int = 8, suffix: str = '.mp4') -> list:
    """Extract evenly-spaced frames from video as PIL Images."""
    tmp_path, frames = None, []
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
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
            "en": f"This {t['en']} shows {confidence}% signs of AI generation or manipulation. It was likely created by AI tools like Midjourney, DALL-E, or Gemini, or is a face deepfake. Do NOT trust, share, or use this as evidence.",
            "hi": f"इस {t['hi']} में {confidence}% AI निर्माण या हेरफेर के संकेत हैं। यह Midjourney, DALL-E या Gemini जैसे AI टूल्स से बनाई गई हो सकती है या फेस डीपफेक हो सकती है। इसे साक्ष्य के रूप में उपयोग, शेयर या विश्वास न करें।",
            "bn": f"এই {t['bn']}তে {confidence}% AI তৈরি বা কারসাজির লক্ষণ দেখা যাচ্ছে। এটি Midjourney, DALL-E বা Gemini-এর মতো AI টুলস দিয়ে তৈরি হতে পারে বা ফেস ডিপফেক হতে পারে। এটি বিশ্বাস, শেয়ার বা প্রমাণ হিসেবে ব্যবহার করবেন না।",
        },
        "SUSPICIOUS": {
            "en": f"This {t['en']} has unusual patterns ({confidence}% AI probability). It may be partially AI-generated or edited. Verify from a trusted source before sharing or using as evidence.",
            "hi": f"इस {t['hi']} में कुछ असामान्य पैटर्न हैं ({confidence}% AI संभावना)। यह आंशिक रूप से AI से बनाई या संपादित हो सकती है। शेयर करने या साक्ष्य के रूप में उपयोग करने से पहले किसी विश्वसनीय स्रोत से पुष्टि करें।",
            "bn": f"এই {t['bn']}তে কিছু অস্বাভাবিক প্যাটার্ন রয়েছে ({confidence}% AI সম্ভাবনা)। এটি আংশিকভাবে AI-তৈরি বা সম্পাদিত হতে পারে। শেয়ার করার বা প্রমাণ হিসেবে ব্যবহারের আগে বিশ্বস্ত সূত্র থেকে নিশ্চিত করুন।",
        },
        "REAL": {
            "en": f"This {t['en']} appears authentic ({confidence}% confidence). No strong signs of AI generation or manipulation detected. Still — always verify viral content before sharing.",
            "hi": f"यह {t['hi']} असली लगती है ({confidence}% विश्वास)। AI निर्माण या हेरफेर के कोई मजबूत संकेत नहीं मिले। फिर भी — वायरल सामग्री शेयर करने से पहले हमेशा जाँच करें।",
            "bn": f"এই {t['bn']}টি আসল বলে মনে হচ্ছে ({confidence}% আত্মবিশ্বাস)। AI তৈরি বা কারসাজির কোনো শক্তিশালী লক্ষণ পাওয়া যায়নি। তবুও — শেয়ার করার আগে সর্বদা যাচাই করুন।",
        },
    }
    return expl.get(verdict, expl["SUSPICIOUS"])
