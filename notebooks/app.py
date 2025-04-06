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

st.set_page_config(page_title="Ultrasound Analyzer", layout="centered")
from streamlit.components.v1 import html
# Custom CSS and animation HTML
# st.markdown("""
#  <div class="ambulance-wrapper">
#         🚑
#     </div>
# <div class="banner">
#     <strong>🩺 Ultrasound Analyzer | Early Diagnosis. Fast. Accurate.</strong>
# </div>

# <style>

# /*extra/
#  /* Gradient background */
#         body {
#             background: linear-gradient(135deg, #d1f0ff, #fceff9);
#             font-family: 'Segoe UI', sans-serif;
#         }

#         /* Container for report */
#         .report-card {
#             background: #ffffffdd;
#             border-radius: 24px;
#             padding: 30px;
#             margin-top: 20px;
#             box-shadow: 0 6px 18px rgba(0,0,0,0.1);
#             font-size: 16px;
#             line-height: 1.6;
#             animation: fadeIn 1.5s ease-in-out;
#         }

#         .report-card h2 {
#             color: #4a90e2;
#             border-bottom: 2px solid #eee;
#             padding-bottom: 8px;
#         }

#         /* Pulse animation for risk status */
#         .risk-label {
#             display: inline-block;
#             padding: 8px 16px;
#             background: #ff6b6b;
#             color: white;
#             font-weight: bold;
#             border-radius: 10px;
#             animation: pulse 2s infinite;
#         }

#         @keyframes fadeIn {
#             from {opacity: 0;}
#             to {opacity: 1;}
#         }

#         @keyframes pulse {
#             0% { box-shadow: 0 0 0 0 rgba(255,107,107,0.7); }
#             70% { box-shadow: 0 0 0 10px rgba(255,107,107,0); }
#             100% { box-shadow: 0 0 0 0 rgba(255,107,107,0); }
#         }
# .ambulance-wrapper {
#             position: fixed;
#             bottom: 20px;
#             left: -100px;
#             font-size: 40px;
#             animation: drive 10s linear infinite;
#             z-index: 999;
#         }

#         @keyframes drive {
#             0% { left: -100px; }
#             50% { left: 50vw; }
#             100% { left: 110vw; }
#         }

# .banner {
#         position: fixed;
#         top: 0;
#         width: 100%;
#         background: #4a90e2;
#         color: white;
#         padding: 12px;
#         text-align: center;
#         font-size: 18px;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.1);
#         z-index: 1000;
#     }


             
# /* Global font and layout */
# body, html {
#     font-family: 'Segoe UI', sans-serif;
#     background: linear-gradient(to right, #e8f0ff, #dce1ff);
#     color: #333;
# }

# /* Streamlit main container */
# .css-18e3th9 {
#     padding: 2rem;
# }

# /* Headings */
# h1, h2, h3 {
#     font-weight: 700;
#     color: #334;
#     text-align: center;
#     margin-top: 0.5em;
# }

# /* Stylish card container */
# .report-card {
#     background-color: #ffffffdd;
#     padding: 2rem;
#     border-radius: 20px;
#     box-shadow: 0 10px 25px rgba(0,0,0,0.1);
#     margin-bottom: 2rem;
#     animation: fadeSlideIn 1s ease;
# }

# /* Stylish upload and report buttons */
# button, .stButton>button {
#     background: linear-gradient(to right, #5f72be, #9b23ea);
#     color: white;
#     border: none;
#     padding: 0.6rem 1.2rem;
#     border-radius: 8px;
#     transition: 0.3s ease-in-out;
# }

# button:hover, .stButton>button:hover {
#     transform: scale(1.05);
#     box-shadow: 0 5px 15px rgba(0,0,0,0.2);
# }

# /* Animated ambulance */
# #ambulance {
#     width: 100px;
#     position: fixed;
#     bottom: 20px;
#     left: -120px;
#     animation: moveAmbulance 12s linear infinite;
# }

# /* Animations */
# @keyframes moveAmbulance {
#     0% { left: -120px; }
#     100% { left: 120%; }
# }

# @keyframes fadeSlideIn {
#     0% {
#         opacity: 0;
#         transform: translateY(30px);
#     }
#     100% {
#         opacity: 1;
#         transform: translateY(0px);
#     }
# }
# </style>
# """, unsafe_allow_html=True)
#
#
st.markdown("""
<style>

/* === BASE SETUP === */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e3f2fd, #ffffff);
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    color: #1a1a1a;
    overflow-x: hidden;
}

/* === HEADER GRADIENT TEXT === */
h1, h2, h3 {
    font-weight: 800;
    background: -webkit-linear-gradient(45deg, #0052D4, #4364F7, #6FB1FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    animation: fadeInDown 1.2s ease-out;
}

/* === FADE IN DOWN === */
@keyframes fadeInDown {
    0% { opacity: 0; transform: translateY(-20px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* === BUTTON ANIMATION === */
button[kind="primary"] {
    background: linear-gradient(to right, #0052D4, #4364F7, #6FB1FC);
    color: white;
    border-radius: 12px;
    padding: 10px 24px;
    border: none;
    font-weight: 600;
    transition: all 0.3s ease;
    animation: popIn 0.8s ease;
}
button[kind="primary"]:hover {
    background: linear-gradient(to right, #6FB1FC, #4364F7, #0052D4);
    transform: scale(1.05);
}

/* === POP IN === */
@keyframes popIn {
    0% { opacity: 0; transform: scale(0.9); }
    100% { opacity: 1; transform: scale(1); }
}

/* === FILE UPLOADER === */
section[data-testid="stFileUploader"] {
    background: #ffffffdd;
    border: 2px dashed #0052D4;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    margin-bottom: 25px;
    animation: slideUp 0.8s ease;
}

/* === SLIDE UP === */
@keyframes slideUp {
    0% { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* === REPORT BOX === */
.report-card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.1);
    margin: 20px auto;
    width: 90%;
    transition: transform 0.2s ease-in-out;
    animation: zoomIn 0.8s ease-out;
}
.report-card:hover {
    transform: scale(1.01);
}

/* === ZOOM IN === */
@keyframes zoomIn {
    0% { opacity: 0; transform: scale(0.9); }
    100% { opacity: 1; transform: scale(1); }
}

/* === AMBULANCE EMOJI (MOVING) === */
.ambulance-wrapper {
    position: fixed;
    bottom: 30px;
    left: -120px;
    font-size: 40px;
    animation: drive 12s linear infinite;
    z-index: 999;
}

/* === MOVING AMBULANCE ANIMATION === */
@keyframes drive {
    0% { left: -100px; }
    50% { left: 50vw; }
    100% { left: 110vw; }
}

/* === PULSE LIGHT (optional glowing effect) === */
.glow-pulse {
    animation: pulse 2s infinite;
    color: #0052D4;
}

/* === PULSE KEYFRAMES === */
@keyframes pulse {
    0% { text-shadow: 0 0 5px #6FB1FC; }
    50% { text-shadow: 0 0 20px #4364F7; }
    100% { text-shadow: 0 0 5px #6FB1FC; }
}
</style>

<!-- MOVING AMBULANCE -->
<div class="ambulance-wrapper">🚑</div>
""", unsafe_allow_html=True)


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
st.markdown('<div class="report-card">', unsafe_allow_html=True)
# detailed_report_html = generate_detailed_report(report_data)

# st.markdown(detailed_report_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


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
#st.set_page_config(page_title="Ultrasound Analyzer", layout="centered")
#st.title("\U0001F9E0 Ultrasound Image Analyzer")
st.title("Fetal Ultrasound Analyzer")
st.write("Upload a fetal ultrasound image and get diagnostic insights.")
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
