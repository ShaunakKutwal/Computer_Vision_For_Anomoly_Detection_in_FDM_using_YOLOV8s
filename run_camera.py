import numpy as np
import cv2
from ultralytics import YOLO
import time
from datetime import datetime
import os
import sys

# Adjusted to pull from the src folder
from src.notifier import trigger_email_alert

def main():
    print("="*60)
    print("3D PRINT DEFECT MONITOR - LIVE INFERENCE")
    print("="*60)

    # Adjusted path to look directly into the models folder
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'best.pt')

    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at: {model_path}")
        print("Please ensure your best.pt file is inside a 'models' folder at the project root.")
        sys.exit(1)

    print("\nLoading model...")
    model = YOLO(model_path)
    print("Model loaded successfully!")
    print(f"Detecting: {list(model.names.values())}")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open webcam. Check USB connection.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Adjusted path for alerts
    alerts_dir = os.path.join(os.path.dirname(__file__), 'alerts', 'snapshots')
    os.makedirs(alerts_dir, exist_ok=True)

    CONF_THRESHOLD = 0.5
    ALERT_THRESHOLD = 0.6
    IOU_THRESHOLD = 0.5
    ALERT_COOLDOWN = 5
    last_alert_time = 0
    fps = 0
    frame_count = 0
    last_time = time.time()

    print("\nPress 'q' to quit | 's' to save manual snapshot\n")

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame_count += 1
        current_time = time.time()
        if current_time - last_time >= 1:
            fps = frame_count
            frame_count = 0
            last_time = current_time

        h, w, _ = frame.shape
        roi = frame[int(0.3*h):int(0.9*h), int(0.2*w):int(0.8*w)]

        results = model(roi, conf=CONF_THRESHOLD, iou=IOU_THRESHOLD)
        annotated_roi = results[0].plot()

        annotated = frame.copy()
        annotated[int(0.3*h):int(0.9*h), int(0.2*w):int(0.8*w)] = annotated_roi

        defects_detected = []

        if results[0].boxes is not None:
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = model.names[cls_id]

                if class_name in ['stringing', 'cracking', 'off_platform'] and conf >= ALERT_THRESHOLD:
                    defects_detected.append(f"{class_name} ({conf:.2%})")
                    if time.time() - last_alert_time > ALERT_COOLDOWN:
                        last_alert_time = time.time()
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        snapshot = os.path.join(alerts_dir, f"{class_name}_{timestamp}.jpg")
                        cv2.imwrite(snapshot, annotated)
                        print(f"ALERT: {class_name} ({conf:.2%}) | Snapshot saved")
                        trigger_email_alert(class_name, conf, snapshot)

        if defects_detected:
            status = "DEFECT: " + ", ".join(defects_detected)
            color = (0, 0, 255)
        else:
            status = "NORMAL OPERATION"
            color = (0, 255, 0)

        cv2.putText(annotated, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(annotated, f"FPS: {fps}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow("FDM Anomaly Monitor", annotated)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        elif key == ord('s'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(alerts_dir, f"manual_{timestamp}.jpg")
            cv2.imwrite(filename, annotated)
            print(f"Manual snapshot saved: {filename}")

    cap.release()
    cv2.destroyAllWindows()
    print("\nMonitoring stopped")

if __name__ == "__main__":
    main()