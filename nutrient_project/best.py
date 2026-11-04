from ultralytics import YOLO

model = YOLO("best.pt")

def detect_leaf(frame):
    results = model(frame, verbose=False)
    boxes = results[0].boxes
    if boxes is not None and len(boxes) > 0:
        idx = int(boxes.conf.argmax())
        label = model.names[int(boxes.cls[idx])]
        confidence = float(boxes.conf[idx])
        return label, confidence
    return "No Detection", 0.0
