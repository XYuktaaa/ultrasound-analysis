import pandas as pd
import json

# Load the Excel file
xlsx_file = "ObjectDetection.xlsx"
df = pd.read_excel(xlsx_file)

# Initialize COCO format dictionary
coco_data = {
    "images": [],
    "annotations": [],
    "categories": []
}

# Define category mapping (modify as per your dataset)
categories = {
    "thalami": 1, "midbrain": 2, "palate": 3, "4th ventricle": 4,
    "cisterna magna": 5, "NT": 6, "nasal tip": 7, "nasal skin": 8, "nasal bone": 9
}

# Add categories to COCO format
for cat_name, cat_id in categories.items():
    coco_data["categories"].append({
        "id": cat_id,
        "name": cat_name,
        "supercategory": "object"
    })

# Process each row in the Excel file
for index, row in df.iterrows():
    image_id = int(row["image_id"])
    filename = row["filename"]
    category_name = row["category"]
    
    # Ensure the category exists
    if category_name not in categories:
        continue
    
    category_id = categories[category_name]
    bbox = [row["xmin"], row["ymin"], row["xmax"] - row["xmin"], row["ymax"] - row["ymin"]]

    # Add image entry if not already added
    if not any(img["id"] == image_id for img in coco_data["images"]):
        coco_data["images"].append({
            "id": image_id,
            "file_name": filename,
            "width": row["width"],
            "height": row["height"]
        })

    # Add annotation
    annotation_id = len(coco_data["annotations"]) + 1
    coco_data["annotations"].append({
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "bbox": bbox,
        "area": bbox[2] * bbox[3],  # width * height
        "iscrowd": 0
    })

# Save as JSON
with open("coco_annotations.json", "w") as f:
    json.dump(coco_data, f, indent=4)

print("✅ Conversion to COCO format completed! Output: coco_annotations.json")
