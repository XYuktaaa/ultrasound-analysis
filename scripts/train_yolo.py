
from ultralytics import YOLO

# Load YOLO model (you can change 'yolov8n.pt' to 'yolov8s.pt' for a bigger model)
model = YOLO("yolov8n.pt")

# Train the model
model.train(
    data="/home/yukta/devel/wip/AIML/ultrasound-analysis/notebooks/dataset.yaml",  # Path to dataset.yaml
    epochs=50,         # Number of training epochs
    imgsz=640,         # Image size
    batch=16,          # Batch size (adjust based on your GPU)
    workers=4,         # Number of workers for data loading
    device="cpu"      # Use cpu if available
)
