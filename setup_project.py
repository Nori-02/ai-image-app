import os
import platform

project_name = "ai-image-generator"
os.makedirs(project_name, exist_ok=True)
static_folder = os.path.join(project_name, "static")
os.makedirs(static_folder, exist_ok=True)

# ملفات المشروع الرئيسية
files = {
    "app.py": '''from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
app = Flask(__name__, static_folder="static")
CORS(app)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/generate-image", methods=["POST"])
def generate_image():
    prompt = request.json.get("prompt", "")
    try:
        model = genai.GenerativeModel("models/imagegeneration")
        response = model.generate_content(prompt)
        if response and response.candidates:
            base64_image = response.candidates[0].content.parts[0].inline_data.data
            return jsonify({"image_base64": base64_image})
        else:
            return jsonify({"error": "لم يتم توليد صورة"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

''',

    ".env": "GEMINI_API_KEY=your_gemini_api_key_here",
    "requirements.txt": "flask\nflask-cors\npython-dotenv\ngoogle-genai",
    "static/index.html": '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <title>مولد الصور بالذكاء الاصطناعي</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-900">
  <div class="max-w-xl mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">توليد صورة</h1>
    <textarea id="prompt" placeholder="صف الصورة هنا..." class="w-full p-3 border rounded mb-4"></textarea>
    <button id="generateButton" class="w-full bg-blue-600 text-white py-2 rounded">توليد الصورة</button>
    <div id="imageContainer" class="mt-6 hidden">
      <img id="generatedImage" class="w-full rounded shadow" />
    </div>
  </div>
  <script>
    document.getElementById("generateButton").addEventListener("click", async () => {
      const prompt = document.getElementById("prompt").value;
      const res = await fetch("/generate-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      if (data.image_base64) {
        document.getElementById("generatedImage").src = `data:image/png;base64,${data.image_base64}`;
        document.getElementById("imageContainer").classList.remove("hidden");
      } else {
        alert("حدث خطأ: " + (data.error || "تعذر توليد الصورة"));
      }
    });
  </script>
</body>
</html>'''
}

# إنشاء الملفات
for path, content in files.items():
    full_path = os.path.join(project_name, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

# إنشاء ملف تشغيل تلقائي حسب النظام
os.chdir(project_name)
if platform.system() == "Windows":
    with open("run.bat", "w", encoding="utf-8") as f:
        f.write('''@echo off
python -m venv venv
call venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
pause
''')
else:
    with open("run.sh", "w", encoding="utf-8") as f:
        f.write('''#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
''')

print(f"✅ تم إنشاء المشروع '{project_name}' وكل الملفات بنجاح.")

