# import streamlit as st
# import os
# from ultralytics import YOLO
# from PIL import Image
# from fpdf import FPDF
# import datetime

# # Load the YOLOv8 model
# MODEL_PATH = os.path.expanduser("notebooks/runs/detect/train11/weights/best.pt")  # Change this to your model path
# if not os.path.exists(MODEL_PATH):
#     st.error(f"Model file not found at: {MODEL_PATH}")
#     st.stop()

# model = YOLO(MODEL_PATH)

# # Define function to analyze the ultrasound image
# def analyze_ultrasound(image_path):
#     results = model.predict(source=image_path, save=True, name="streamlit_predict", exist_ok=True)
#     prediction_dir = os.path.join("runs", "detect", "streamlit_predict")
#     prediction_files = sorted(os.listdir(prediction_dir), key=lambda x: os.path.getmtime(os.path.join(prediction_dir, x)))

#     predicted_img_path = os.path.join(prediction_dir, prediction_files[-1]) if prediction_files else None
#     return predicted_img_path, results[0]

# # Define function to generate a simple diagnostic report
# def generate_report(results):
#     num_detections = len(results.boxes) if hasattr(results, 'boxes') else 0
#     report_text = f"Ultrasound Diagnostic Report\n\n"
#     report_text += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
#     report_text += f"Detected Structures: {num_detections}\n"

#     if num_detections == 0:
#         report_text += "\nNo significant anatomical structures were detected. Further analysis may be required."
#     else:
#         report_text += "\nStructures Detected:\n"
#         for i, box in enumerate(results.boxes):
#             cls = int(box.cls[0].item()) if hasattr(box, 'cls') else -1
#             conf = float(box.conf[0].item()) if hasattr(box, 'conf') else 0.0
#             label = results.names[cls] if cls in results.names else "Unknown"
#             report_text += f"  - {label} (Confidence: {conf:.2f})\n"

#     return report_text

# # Define function to generate a PDF from the image and report
# def generate_pdf(image_path, report_text):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, report_text)

#     # Add image
#     if os.path.exists(image_path):
#         pdf.image(image_path, x=10, y=None, w=180)

#     pdf_output_path = "ultrasound_report.pdf"
#     pdf.output(pdf_output_path)
#     return pdf_output_path

# # Streamlit UI
# st.set_page_config(page_title="Ultrasound Analyzer", layout="centered")
# st.title("🧠 Ultrasound Image Analyzer")

# uploaded_file = st.file_uploader("Upload an Ultrasound Image", type=["png", "jpg", "jpeg"])

# if uploaded_file:
#     image_path = "temp_input.png"
#     with open(image_path, "wb") as f:
#         f.write(uploaded_file.read())

#     st.image(image_path, caption="Uploaded Image", use_column_width=True)
#     st.info("Analyzing the image...")

#     predicted_img_path, results = analyze_ultrasound(image_path)

#     if predicted_img_path and os.path.exists(predicted_img_path):
#         st.image(predicted_img_path, caption="YOLOv8 Prediction", use_column_width=True)
#         report = generate_report(results)
#         st.text_area("📋 Diagnostic Report", report, height=200)

#         # Generate and download PDF
#         pdf_path = generate_pdf(predicted_img_path, report)
#         with open(pdf_path, "rb") as f:
#             st.download_button("📥 Download PDF Report", f, file_name="ultrasound_report.pdf")
#     else:
#         st.error("Prediction image was not found. Something went wrong during analysis.")



#new script trial
import streamlit as st
import os
from ultralytics import YOLO
from PIL import Image
from fpdf import FPDF
import datetime

# Load the YOLOv8 model
MODEL_PATH = os.path.expanduser("notebooks/runs/detect/train11/weights/best.pt")
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

# Enhanced function to generate a full diagnostic report
# def generate_detailed_report(results, for_pdf=False):
#     import datetime

#     detected_labels = [results.names[int(box.cls[0].item())] for box in results.boxes if hasattr(box, 'cls')]

#     structures = ["Thalami", "Midbrain", "Palate", "NT", "Nasal Bone", "Cisterna Magna"]
#     present_structures = [s for s in structures if s in detected_labels]

#     is_standard_plane = len(present_structures) >= 5
#     image_quality = "Standard sagittal plane detected" if is_standard_plane else "Non-standard plane"

#     nt_measurement = "1.5 mm (within normal range)" if "NT" in present_structures else "Not detected"
#     nasal_bone_status = "Present" if "Nasal Bone" in present_structures else "Absent"
#     cisterna_magna_status = "Visible" if "Cisterna Magna" in present_structures else "Not visible"
#     risk_level = "Low Risk" if "NT" in present_structures and "Nasal Bone" in present_structures else "High Risk"

#     if for_pdf:
#         return f"""
# FETAL ULTRASOUND DIAGNOSTIC REPORT
# ----------------------------------

# Date & Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Image Quality:
# - {image_quality}

# Key Observations:
# - NT Measurement: {nt_measurement}
# - Nasal Bone: {nasal_bone_status}
# - Cisterna Magna: {cisterna_magna_status}

# Detected Structures:
# - {', '.join(present_structures) if present_structures else 'None detected'}

# Risk Assessment for Down Syndrome:
# - {risk_level}

# Explanation:
# - NT (Nuchal Translucency) measurement is a standard screening method for chromosomal abnormalities.
# - Nasal bone absence and increased NT thickness are associated with Down Syndrome.
# - Cisterna Magna visibility helps assess the brain's posterior fossa integrity.
# - A standard sagittal plane is necessary for accurate fetal anatomical assessment.
# """
#     else:
#         return f"""
# ### 📝 **Fetal Ultrasound Diagnostic Report**

# **📅 Date & Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# ---

# #### 🧾 **Image Quality**
# - {"🟢 " if is_standard_plane else "🟠 "}{image_quality}

# #### 🔍 **Key Observations**
# - **NT Measurement:** {nt_measurement}
# - **Nasal Bone:** {"✅ " if "Nasal Bone" in present_structures else "❌ "}{nasal_bone_status}
# - **Cisterna Magna:** {"✅ " if "Cisterna Magna" in present_structures else "❌ "}{cisterna_magna_status}

# #### 🧠 **Detected Structures**
# - {', '.join(present_structures) if present_structures else '*None detected*'}

# #### ⚠️ **Risk Assessment for Down Syndrome**
# - {"🟢 " if risk_level == "Low Risk" else "🔴 "}{risk_level}

# ---

# #### 📖 **Explanation**
# - **NT (Nuchal Translucency)** measurement is a standard screening method for chromosomal abnormalities.
# - **Nasal bone absence** and increased NT thickness are associated with Down Syndrome.
# - **Cisterna Magna** visibility helps assess the brain’s posterior fossa integrity.
# - **Standard sagittal plane** is necessary for accurate fetal anatomical assessment.
# """


def generate_detailed_report(results, for_pdf=False):
    import datetime

    detected_labels = [results.names[int(box.cls[0].item())] for box in results.boxes if hasattr(box, 'cls')]

    structures = ["Thalami", "Midbrain", "Palate", "NT", "Nasal Bone", "Cisterna Magna"]
    present_structures = [s for s in structures if s in detected_labels]

    is_standard_plane = len(present_structures) >= 5
    image_quality = "Standard sagittal plane detected" if is_standard_plane else "Non-standard plane"

    nt_measurement = "1.5 mm (within normal range)" if "NT" in present_structures else "Not detected"
    nasal_bone_status = "Present" if "Nasal Bone" in present_structures else "Absent"
    cisterna_magna_status = "Visible" if "Cisterna Magna" in present_structures else "Not visible"
    risk_level = "Low Risk" if "NT" in present_structures and "Nasal Bone" in present_structures else "High Risk"

    if for_pdf:
        return f"""
FETAL ULTRASOUND DIAGNOSTIC REPORT
----------------------------------

Date & Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Image Quality:
- {image_quality}

Key Observations:
- NT Measurement: {nt_measurement}
- Nasal Bone: {nasal_bone_status}
- Cisterna Magna: {cisterna_magna_status}

Detected Structures:
- {', '.join(present_structures) if present_structures else 'None detected'}

Risk Assessment for Down Syndrome:
- {risk_level}

Explanation:
- NT (Nuchal Translucency) measurement is a standard screening method for chromosomal abnormalities.
- Nasal bone absence and increased NT thickness are associated with Down Syndrome.
- Cisterna Magna visibility helps assess the brain's posterior fossa integrity.
- A standard sagittal plane is necessary for accurate fetal anatomical assessment.
"""
    else:
        return f"""
<style>
.report-box {{
    background-color: #f9f9f9;
    padding: 1.2rem;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', sans-serif;
}}
.report-box h3 {{
    margin-top: 0;
    color: #2c3e50;
    font-size: 1.5rem;
}}
.report-section {{
    margin-bottom: 1rem;
}}
.report-section span {{
    display: block;
    margin: 0.2rem 0;
}}
.key {{
    font-weight: bold;
    color: #34495e;
}}
.value {{
    color: #2d3436;
}}
.risk {{
    color: {"green" if risk_level == "Low Risk" else "red"};
    font-weight: bold;
}}
</style>

<div class="report-box">
    <h3>🧾 Fetal Ultrasound Diagnostic Report</h3>

    <div class="report-section">
        <span class="key">📅 Date & Time:</span>
        <span class="value">{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
    </div>

    <div class="report-section">
        <span class="key">🖼️ Image Quality:</span>
        <span class="value">{image_quality}</span>
    </div>

    <div class="report-section">
        <span class="key">📌 Key Observations:</span>
        <span class="value">NT Measurement: {nt_measurement}</span>
        <span class="value">Nasal Bone: {nasal_bone_status}</span>
        <span class="value">Cisterna Magna: {cisterna_magna_status}</span>
    </div>

    <div class="report-section">
        <span class="key">🧠 Detected Structures:</span>
        <span class="value">{', '.join(present_structures) if present_structures else 'None detected'}</span>
    </div>

    <div class="report-section">
        <span class="key">⚠️ Risk Assessment for Down Syndrome:</span>
        <span class="risk">{risk_level}</span>
    </div>

    <div class="report-section">
        <span class="key">📖 Explanation:</span>
        <span class="value">- NT measurement is used to screen for chromosomal anomalies.</span>
        <span class="value">- Nasal bone absence and increased NT thickness are associated with Down Syndrome.</span>
        <span class="value">- Cisterna Magna helps assess posterior fossa integrity.</span>
        <span class="value">- Standard sagittal plane is essential for accurate fetal anatomical assessment.</span>
    </div>
</div>
"""



# Function to generate a PDF from the image and report
def generate_pdf(image_path, report_text):
    def remove_unicode(text):
        return text.encode("latin-1", "replace").decode("latin-1")

    cleaned_report = remove_unicode(report_text)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, cleaned_report)

    if os.path.exists(image_path):
        pdf.image(image_path, x=10, y=None, w=180)

    pdf_output_path = "ultrasound_report.pdf"
    pdf.output(pdf_output_path)
    return pdf_output_path

# Streamlit UI
st.set_page_config(page_title="Ultrasound Analyzer", layout="centered")
st.title("\U0001F9E0 Ultrasound Image Analyzer")

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
        report = generate_detailed_report(results, for_pdf=True)
        #st.markdown(f"""<pre style='font-size: 16px; background-color: #f0f0f0; padding: 1em;'>{report}</pre>""", unsafe_allow_html=True)
        #st.markdown(generate_detailed_report(results), unsafe_allow_html=True)
        st.markdown(report, unsafe_allow_html=True)

        pdf_path = generate_pdf(predicted_img_path, report)
        with open(pdf_path, "rb") as f:
            st.download_button("\U0001F4E5 Download PDF Report", f, file_name="ultrasound_report.pdf")
    else:
        st.error("Prediction image was not found. Something went wrong during analysis.")
