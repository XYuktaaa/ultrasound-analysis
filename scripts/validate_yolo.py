from ultralytics import YOLO
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Validate YOLO model performance")
parser.add_argument("--model", type=str, required=True, help="Path to trained YOLO model (e.g., best.pt)")
parser.add_argument("--data", type=str, required=True, help="Path to dataset.yaml")
parser.add_argument("--imgsz", type=int, default=640, help="Image size for validation (default: 640)")
parser.add_argument("--device", type=str, default="cpu", help="Device to run validation on (cpu or cuda)")
args = parser.parse_args()

# Load trained YOLO model
model = YOLO(args.model)

# Run validation
metrics = model.val(
    data=args.data,
    imgsz=args.imgsz,
    device=args.device,
    save_json=True,  # Save results in COCO format
    save_hybrid=True # Save results with labels and predictions
)

# Print results
print("Validation Complete!")
print(f"mAP50: {metrics.box.map50:.3f}")
print(f"mAP50-95: {metrics.box.map:.3f}")
print(f"Precision: {metrics.box.precision:.3f}")
print(f"Recall: {metrics.box.recall:.3f}")
print(f"F1 Score: {metrics.box.f1:.3f}")

