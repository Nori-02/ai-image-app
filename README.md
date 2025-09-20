# Nori stable-diffusion-app 🎨

تطبيق بسيط لتوليد الصور باستخدام Stable Diffusion محليًا.

## المتطلبات

- Python 3.8+
- بطاقة رسومية تدعم CUDA
- ملفات النموذج داخل `models/stable-diffusion-v1`

## التشغيل

### Linux/macOS

```bash
./run.sh

Windows
run.bat

## الميزات الجديدة
- توليد صور متعددة دفعة واحدة (حتى 5 صور)
- حفظ الصور تلقائيًا في مجلد `outputs/`
- تسمية الصور حسب الوقت والوصف
- واجهة Gradio محسّنة وسهلة الاستخدام
