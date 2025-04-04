import os
import pandas as pd
from tqdm import tqdm

# Define paths
xls_file = "/home/yukta/devel/wip/AIML/ultrasound-analysis/data/annotations/ObjectDetection.xlsx"
image_dir = "/home/yukta/devel/wip/AIML/ultrasound-analysis/data/images/DatasetForFetus/Set1-Training&Validation Sets CNN"
output_label_dir = "/home/yukta/devel/wip/AIML/ultrasound-analysis/data/labels"

# Ensure output directory exists
os.makedirs(output_label_dir, exist_ok=True)

# Read Excel file
df = pd.read_excel(xls_file)

# Define class mappings
class_names = ["thalami", "midbrain", "palate", "fourth_ventricle",
               "cisterna_magna", "nuchal_translucency", "nasal_tip", "nasal_skin", "nasal_bone"]
class_map = {name: i for i, name in enumerate(class_names)}

# Iterate over annotations
for _, row in tqdm(df.iterrows(), total=len(df), desc="Converting Annotations"):
    fname = row["fname"]
    structure = row["structure"]
    h_min, w_min, h_max, w_max = row["h_min"], row["w_min"], row["h_max"], row["w_max"]

    # Construct image path
    image_path = os.path.join(image_dir, fname)

    # Check if image exists
    if not os.path.exists(image_path):
        print(f"⚠️ Warning: Image {fname} not found in {image_dir}. Skipping...")
        continue  # Skip missing images

    # Get class index
    class_id = class_map.get(structure, -1)
    if class_id == -1:
        print(f"⚠️ Warning: Class {structure} not found in class map! Skipping...")
        continue

    # Placeholder image dimensions (update if needed)
    img_width, img_height = 640, 480  

    # Convert to YOLO format
    x_center = (w_min + w_max) / 2 / img_width
    y_center = (h_min + h_max) / 2 / img_height
    width = (w_max - w_min) / img_width
    height = (h_max - h_min) / img_height

    # Define output label file
    label_filename = os.path.join(output_label_dir, fname.replace(".png", ".txt"))

    # Write YOLO annotation
    with open(label_filename, "w") as f:
        f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

print("✅ Annotation conversion completed successfully!")
