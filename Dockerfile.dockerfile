# 🧱 الأساس: Python مع دعم CUDA (إذا كنت تستخدم GPU)
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 🛠️ تثبيت الأدوات الأساسية
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-venv \
    git \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 🔧 إعداد البيئة
WORKDIR /app
COPY . /app

# 🧪 تثبيت المتطلبات
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# 📁 إنشاء مجلدات الإخراج
RUN mkdir -p outputs assets/qr

# 🌍 تعيين المنفذ
EXPOSE 7860

# 🚀 تشغيل التطبيق
CMD ["python3", "app.py"]
