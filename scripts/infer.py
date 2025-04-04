from ultralytics import YOLO

# Load trained model
model = YOLO("runs/detect/train/weights/best.pt")

# Run inference on a test image
results = model("/home/yukta/devel/wip/AIML/ultrasound-analysis/data/test_image.png", save=True)

# Display results
for result in results:
    print(result)

