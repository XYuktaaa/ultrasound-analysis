#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd

# 📌 Paths
xlsx_file = "/home/yukta/devel/wip/AIML/ultrasound-analysis/data/annotations/ObjectDetection.xlsx"  # Update path
images_base_path = "/home/yukta/devel/wip/AIML/ultrasound-analysis/data/images/DatasetForFetus"
labels_base_path = images_base_path  # YOLO labels will be saved inside this

# 🔹 Class mapping (same as dataset.yaml)
class_mapping = {
    "thalami": 0,
    "midbrain": 1,
    "palate": 2,
    "fourth_ventricle": 3,
    "cisterna_magna": 4,
    "nuchal_translucency": 5,
    "nasal_tip": 6,
    "nasal_skin": 7,
    "nasal_bone": 8
}

# 🔹 Read the annotations
df = pd.read_excel(xlsx_file)

# 🔹 Create YOLO labels folder if not exists
for folder in ["Set1-Training&Validation Sets CNN", "Internal Test Set", "External Test Set"]:
    labels_path = os.path.join(labels_base_path, folder, "labels")
    os.makedirs(labels_path, exist_ok=True)

# 🔹 Process each annotation
for _, row in df.iterrows():
    img_filename = row["fname"]
    structure = row["structure"]
    h_min, w_min, h_max, w_max = row["h_min"], row["w_min"], row["h_max"], row["w_max"]

    # 🔹 Get class ID
    if structure not in class_mapping:
        print(f"Warning: {structure} not in class mapping! Skipping...")
        continue
    class_id = class_mapping[structure]

    # 🔹 Find image path (which dataset folder it belongs to)
    found = False
    for folder in ["Set1-Training&Validation Sets CNN", "Internal Test Set", "External Test Set"]:
        image_path = os.path.join(images_base_path, folder, img_filename)
        if os.path.exists(image_path):
            labels_path = os.path.join(labels_base_path, folder, "labels")
            found = True
            break

    if not found:
        print(f"Error: Image {img_filename} not found in dataset folders! Skipping...")
        continue

    # 🔹 Get image size
    from PIL import Image
    img = Image.open(image_path)
    img_width, img_height = img.size

    # 🔹 Normalize YOLO values
    x_center = ((w_min + w_max) / 2) / img_width
    y_center = ((h_min + h_max) / 2) / img_height
    width = (w_max - w_min) / img_width
    height = (h_max - h_min) / img_height

    # 🔹 Format: class_id x_center y_center width height
    yolo_line = f"{class_id} {x_center} {y_center} {width} {height}\n"

    # 🔹 Save to corresponding `.txt` file
    label_file = os.path.join(labels_path, img_filename.replace(".png", ".txt"))
    with open(label_file, "a") as f:
        f.write(yolo_line)

    print(f"✅ Saved: {label_file}")

print("\n🎯 Annotation conversion complete! Now labels are in /labels/ folders.")

