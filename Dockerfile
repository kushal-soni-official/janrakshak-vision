FROM python:3.10-slim

WORKDIR /code

# System dependencies for OpenCV and video processing
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    libgomp1 ffmpeg libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# CPU-only PyTorch (smaller, faster install on HuggingFace free tier)
RUN pip install --no-cache-dir \
    torch==2.1.0 torchvision==0.16.0 \
    --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-download AI model during Docker build (speeds up first request)
RUN python -c "from models import preload_model; preload_model()"

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
