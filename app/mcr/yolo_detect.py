from ultralytics import YOLO

model = YOLO("/weights/best.pt")

def yolo_detect(image) -> list:
    detections = model.predict(
        source=image,
        imgsz=1280,
    )
    results = []
    for r in detections:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            results.append([x1, y1, x2, y2, conf, cls_id])
    return results
