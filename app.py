import streamlit as st
import os
from ultralytics import YOLO
from PIL import Image
from fpdf import FPDF
import datetime

# Load the YOLOv8 model
MODEL_PATH = os.path.expanduser("notebooks/runs/detect/train11/weights/best.pt")  # Change this to your model path
if not os.path.exists(MODEL_PATH):
    st.error(f"Model file not found at: {MODEL_PATH}")
    st.stop()

model = YOLO(MODEL_PATH)

# Define function to analyze the ultrasound image
def analyze_ultrasound(image_path):
    results = model.predict(source=image_path, save=True, name="streamlit_predict", exist_ok=True)
    prediction_dir = os.path.join("runs", "detect", "streamlit_predict")
    prediction_files = sorted(os.listdir(prediction_dir), key=lambda x: os.path.getmtime(os.path.join(prediction_dir, x)))

    predicted_img_path = os.path.join(prediction_dir, prediction_files[-1]) if prediction_files else None
    return predicted_img_path, results[0]

# Define function to generate a simple diagnostic report
def generate_report(results):
    num_detections = len(results.boxes) if hasattr(results, 'boxes') else 0
    report_text = f"Ultrasound Diagnostic Report\n\n"
    report_text += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report_text += f"Detected Structures: {num_detections}\n"

    if num_detections == 0:
        report_text += "\nNo significant anatomical structures were detected. Further analysis may be required."
    else:
        report_text += "\nStructures Detected:\n"
        for i, box in enumerate(results.boxes):
            cls = int(box.cls[0].item()) if hasattr(box, 'cls') else -1
            conf = float(box.conf[0].item()) if hasattr(box, 'conf') else 0.0
            label = results.names[cls] if cls in results.names else "Unknown"
            report_text += f"  - {label} (Confidence: {conf:.2f})\n"

    return report_text

# Define function to generate a PDF from the image and report
def generate_pdf(image_path, report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, report_text)

    # Add image
    if os.path.exists(image_path):
        pdf.image(image_path, x=10, y=None, w=180)

    pdf_output_path = "ultrasound_report.pdf"
    pdf.output(pdf_output_path)
    return pdf_output_path

# Streamlit UI
st.set_page_config(page_title="Ultrasound Analyzer", layout="centered")
st.title("🧠 Ultrasound Image Analyzer")

uploaded_file = st.file_uploader("Upload an Ultrasound Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image_path = "temp_input.png"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.read())

    st.image(image_path, caption="Uploaded Image", use_column_width=True)
    st.info("Analyzing the image...")

    predicted_img_path, results = analyze_ultrasound(image_path)

    if predicted_img_path and os.path.exists(predicted_img_path):
        st.image(predicted_img_path, caption="YOLOv8 Prediction", use_column_width=True)
        report = generate_report(results)
        st.text_area("📋 Diagnostic Report", report, height=200)

        # Generate and download PDF
        pdf_path = generate_pdf(predicted_img_path, report)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF Report", f, file_name="ultrasound_report.pdf")
    else:
        st.error("Prediction image was not found. Something went wrong during analysis.")
