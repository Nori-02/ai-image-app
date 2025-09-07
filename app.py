from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google import genai

# تحميل متغيرات البيئة
load_dotenv()

# التحقق من مفتاح API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set in environment variables.")

# إنشاء عميل Google GenAI
client = genai.Client(api_key=api_key)

# إعداد Flask
app = Flask(__name__, static_folder="static")
CORS(app)

@app.route("/generate-image", methods=["POST"])
def generate_image():
    prompt = request.json.get("prompt", "")
    try:
        model = client.models.get("models/imagegeneration")
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
    # Railway توفر PORT تلقائيًا
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
