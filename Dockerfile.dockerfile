# استخدام صورة Python الرسمية
FROM python:3.11-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ الملفات المطلوبة إلى الحاوية
COPY . .

# تثبيت المتطلبات
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# إعداد متغير البيئة (يمكن تجاوزه من إعدادات منصة النشر لاحقًا)
ENV curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explain how AI works in a few words"
          }
        ]
      }
    ]
  }'

# تعيين المنفذ الافتراضي في بيئة النشر
ENV PORT=8080

# أمر التشغيل
CMD ["python", "app.py"]
