import json
import os
import gradio as gr

def load_metadata(metadata_path="./outputs/metadata.json"):
    if not os.path.exists(metadata_path):
        return "لا توجد بيانات محفوظة بعد."
    with open(metadata_path, "r") as f:
        data = json.load(f)
    return json.dumps(data, indent=2, ensure_ascii=False)

gr.Interface(fn=load_metadata, inputs=[], outputs="text", title="📋 واجهة إدارية للصور").launch()
