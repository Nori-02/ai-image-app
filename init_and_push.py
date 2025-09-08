import os
import subprocess

# 1. إنشاء ملفات البيئة
files = {
    "Procfile": 'web: gunicorn app:app --bind 0.0.0.0:$PORT\n',
    "runtime.txt": 'python-3.11.8\n',
    "pyproject.toml": '''[project]
name = "ai-image-generator"
version = "1.0.0"
description = "مولد صور باستخدام Google Generative AI و Flask"
requires-python = ">=3.11"
dependencies = [
    "flask",
    "flask-cors",
    "python-dotenv",
    "google-genai",
    "gunicorn"
]
'''
}

for name, content in files.items():
    with open(name, "w", encoding="utf-8") as f:
        f.write(content)
        print(f"✅ تم إنشاء الملف: {name}")

# 2. تهيئة Git
if not os.path.exists(".git"):
    subprocess.run(["git", "init"])
    print("🔧 تم تهيئة Git المحلي.")
else:
    print("ℹ️ Git مهيأ مسبقًا.")

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "تهيئة المشروع ورفع ملفات النشر"])

# 3. ربط المستودع البعيد
repo_url = input("🌐 أدخل رابط مستودع GitHub (HTTPS): ").strip()
subprocess.run(["git", "branch", "-M", "main"])
remotes = subprocess.run(["git", "remote"], capture_output=True, text=True).stdout.split()
if "origin" not in remotes:
    subprocess.run(["git", "remote", "add", "origin", repo_url])


print("\n🎉 تم رفع المشروع إلى GitHub بنجاح!")
