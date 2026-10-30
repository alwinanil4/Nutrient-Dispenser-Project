import cv2, time, serial
import numpy as np
from collections import deque
from datetime import datetime
from ultralytics import YOLO

# ---------- SETTINGS ----------
MODEL_PATH = "best.pt"
COM_PORT = "COM3"
BAUD = 9600
CAM_INDEX = 0
CONF_MIN = 0.5
# ------------------------------

CLASS_TO_CODE = {
    "Healthy": b"1",
    "Chlorosis": b"2",
    "Transpiration Stress": b"3",
    "No leaf": b"0",
}
COLORS = {
    "Healthy": (0, 200, 0),
    "Chlorosis": (0, 215, 255),
    "Transpiration Stress": (0, 0, 255),
    "No leaf": (200, 200, 200),
}

model = YOLO(MODEL_PATH)
print("Model classes:", model.names)
cap = cv2.VideoCapture(CAM_INDEX)

try:
    ser = serial.Serial(COM_PORT, BAUD, timeout=1)
    time.sleep(2)
except Exception as e:
    print("Arduino not connected:", e)
    ser = None

log = deque(maxlen=8)
last_label = None

def build_panel(height):
    panel = np.zeros((height, 320, 3), dtype=np.uint8)
    cv2.putText(panel, "DETECTION LOG", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    for i, (t, lbl, c) in enumerate(reversed(log)):
        cv2.putText(panel, f"{t} {lbl} {c:.0%}", (10, 65 + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    COLORS.get(lbl, (255, 255, 255)), 1)
    status = "Arduino: ON" if ser else "Arduino: OFF"
    cv2.putText(panel, status, (10, height - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    return panel

while True:
    ok, frame = cap.read()
    if not ok:
        break

    result = model(frame, conf=CONF_MIN, verbose=False)[0]
    label, conf = "No leaf", 0.0

    if len(result.boxes) > 0:
        i = int(result.boxes.conf.argmax())
        label = model.names[int(result.boxes.cls[i])]
        conf = float(result.boxes.conf[i])
        x1, y1, x2, y2 = map(int, result.boxes.xyxy[i])
        cv2.rectangle(frame, (x1, y1), (x2, y2),
                      COLORS.get(label, (255, 255, 255)), 2)

    # act only when the detection changes
    if label != last_label:
        log.append((datetime.now().strftime("%H:%M:%S"), label, conf))
        if ser and label in CLASS_TO_CODE:
            ser.write(CLASS_TO_CODE[label])
        last_label = label

    cv2.putText(frame, f"{label} ({conf:.0%})", (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                COLORS.get(label, (255, 255, 255)), 2)
    cv2.imshow("Nutrient Dispenser Dashboard",
               np.hstack((frame, build_panel(frame.shape[0]))))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# turn LEDs off on exit
if ser:
    ser.write(b"0")
    time.sleep(0.2)
    ser.close()
cap.release()
cv2.destroyAllWindows()