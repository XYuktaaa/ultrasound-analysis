import pandas as pd
import os

# Paths
csv_file = "~/files/ObjectDetection.csv"  # Update if needed
images_dir = "~/devel/wip/AIML/ultrasound-analysis/data/images/DatasetForFetus/Set1-Training&Validation Sets CNN/Standard"  # Directory containing images
labels_dir = "~/devel/wip/AIML/ultrasound-analysis/data/images/DatasetForFetus/Set1-Training&Validation Sets CNN/labels/"  # Directory to save YOLO annotations

# Ensure labels directory exists
os.makedirs(labels_dir, exist_ok=True)

# Read CSV file
df = pd.read_csv(csv_file)

# Column names (from your dataset)
IMAGE_COL = "fname"
CLASS_COL = "structure"
X_MIN = "w_min"
Y_MIN = "h_min"
X_MAX = "w_max"
Y_MAX = "h_max"

# Assuming all images have the same resolution (update if dynamic per image)
IMG_WIDTH = 1024  # Change this to the correct width of your images
IMG_HEIGHT = 768  # Change this to the correct height of your images

# Convert each annotation to YOLO format
for _, row in df.iterrows():
    image_name = row[IMAGE_COL]
    class_id = row[CLASS_COL]  # If class names are in text, map to numerical IDs

    # Bounding box coordinates
    xmin, ymin, xmax, ymax = row[X_MIN], row[Y_MIN], row[X_MAX], row[Y_MAX]

    # Convert to YOLO format (normalize)
    x_center = ((xmin + xmax) / 2) / IMG_WIDTH
    y_center = ((ymin + ymax) / 2) / IMG_HEIGHT
    width = (xmax - xmin) / IMG_WIDTH
    height = (ymax - ymin) / IMG_HEIGHT

    # Create label file
    label_filename = os.path.join(labels_dir, os.path.splitext(image_name)[0] + ".txt")
    with open(label_filename, "a") as f:
        f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

print("Conversion complete! YOLO annotations saved in 'labels/' directory.")
