import pandas as pd
import json

# Load Excel file
df = pd.read_excel("~/ultrasound-analysis/data/annotations/ObjectDetection.xlsx")

# Define COCO format structure
coco_format = {
    "images": [],
    "annotations": [],
    "categories": []
}

# Assign category IDs
category_mapping = {name: i+1 for i, name in enumerate(df["structure"].unique())}
coco_format["categories"] = [{"id": i, "name": name} for name, i in category_mapping.items()]

# Track image IDs
image_id_mapping = {}
annotation_id = 1

for index, row in df.iterrows():
    file_name = row["fname"]
    
    # Add image metadata if not already added
    if file_name not in image_id_mapping:
        image_id = len(image_id_mapping) + 1
        image_id_mapping[file_name] = image_id
        coco_format["images"].append({
            "id": image_id,
            "file_name": file_name,
            "width": 512,  # Replace with actual width
            "height": 512  # Replace with actual height
        })

    # Add annotation
    image_id = image_id_mapping[file_name]
    bbox = [row["w_min"], row["h_min"], row["w_max"] - row["w_min"], row["h_max"] - row["h_min"]]
    area = bbox[2] * bbox[3]

    coco_format["annotations"].append({
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_mapping[row["structure"]],
        "bbox": bbox,
        "area": area,
        "iscrowd": 0
    })
    annotation_id += 1

# Save as JSON
with open("ObjectDetection_COCO.json", "w") as f:
    json.dump(coco_format, f, indent=4)

print("COCO JSON file saved!")

