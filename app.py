import os
import torch
import json
import uuid
from PIL import Image
from datetime import datetime
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
import gradio as gr
from dotenv import load_dotenv
import qrcode

# تحميل متغيرات البيئة
load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH", "./models/stable-diffusion-v1")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./outputs")
QR_DIR = os.path.join("assets", "qr")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(QR_DIR, exist_ok=True)

# تحميل النموذج
text2img_pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16
).to("cuda")

img2img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16
).to("cuda")

# حفظ metadata و QR
def save_metadata(prompt, settings, image_paths):
    timestamp = datetime.now().isoformat()
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": timestamp,
        "prompt": prompt,
        "settings": settings,
        "images": image_paths
    }
    metadata_path = os.path.join(OUTPUT_DIR, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(metadata_path, "w") as f:
        json.dump(data, f, indent=2)

    # توليد QR لكل صورة
    for path in image_paths:
        qr = qrcode.make(f"file://{os.path.abspath(path)}")
        qr_filename = os.path.join(QR_DIR, os.path.basename(path).replace(".png", "_qr.png"))
        qr.save(qr_filename)

# توليد الصور
def generate(prompt, num_images, guidance, steps, width, height, input_image=None, strength=0.75):
    images = []
    image_paths = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for i in range(num_images):
        if input_image:
            input_image = input_image.convert("RGB").resize((width, height))
            result = img2img_pipe(prompt=prompt, image=input_image, strength=strength,
                                  guidance_scale=guidance, num_inference_steps=steps).images[0]
        else:
            result = text2img_pipe(prompt=prompt, guidance_scale=guidance,
                                   num_inference_steps=steps, height=height, width=width).images[0]

        filename = f"{OUTPUT_DIR}/{timestamp}_{i+1}.png"
        result.save(filename)
        images.append(result)
        image_paths.append(filename)

    save_metadata(prompt, {
        "guidance_scale": guidance,
        "steps": steps,
        "width": width,
        "height": height,
        "mode": "img2img" if input_image else "text2img"
    }, image_paths)

    return images

# واجهة إدارية
def view_metadata():
    metadata_path = os.path.join(OUTPUT_DIR, "metadata.json")
    if not os.path.exists(metadata_path):
        return "لا توجد بيانات محفوظة بعد."
    with open(metadata_path, "r") as f:
        data = json.load(f)
    return json.dumps(data, indent=2, ensure_ascii=False)

# واجهة Gradio
with gr.Blocks(title="Stable Diffusion App") as demo:
    gr.Markdown("## 🎨 تطبيق توليد الصور بالذكاء الاصطناعي")
    with gr.Row():
        prompt = gr.Textbox(label="📝 الوصف النصي")
        input_image = gr.Image(label="📤 صورة للتعديل (اختياري)", type="pil", optional=True)

    with gr.Row():
        num_images = gr.Slider(1, 5, value=1, step=1, label="📸 عدد الصور")
        guidance = gr.Slider(5, 20, value=7.5, step=0.5, label="🎯 قوة التوجيه")
        steps = gr.Slider(10, 100, value=30, step=5, label="⚙️ عدد الخطوات")
        strength = gr.Slider(0.3, 1.0, value=0.75, step=0.05, label="🧪 قوة التعديل (img2img)")
    with gr.Row():
        width = gr.Slider(256, 1024, value=512, step=64, label="📐 العرض")
        height = gr.Slider(256, 1024, value=512, step=64, label="📏 الارتفاع")

    generate_btn = gr.Button("🚀 توليد الصور")
    gallery = gr.Gallery(label="📂 الصور الناتجة").style(grid=2)

    generate_btn.click(fn=generate, inputs=[prompt, num_images, guidance, steps, width, height, input_image, strength], outputs=gallery)

    gr.Markdown("---")
    gr.Markdown("## 🗂️ واجهة إدارية")
    admin_btn = gr.Button("📋 عرض البيانات المحفوظة")
    admin_output = gr.Textbox(label="📄 Metadata", lines=20)
    admin_btn.click(fn=view_metadata, outputs=admin_output)

demo.launch()
