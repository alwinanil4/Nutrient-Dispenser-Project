import cv2
import numpy as np
import serial
import time
import datetime
from best import detect_leaf

COM_PORT = "COM10"
BAUD_RATE = 9600
CAM_INDEX = 1

COLORS = {
    "nutrient-leaf-detector": (50, 205, 50),
    "wilted plant leaf transpiration stress": (50, 50, 240),
    "No Detection": (160, 160, 160),
}

COMMANDS = {
    "nutrient-leaf-detector": b"G",
    "wilted plant leaf transpiration stress": b"R",
}

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(3)
except Exception:
    ser = None

cap = cv2.VideoCapture(CAM_INDEX)

log = []
last_label = None
label = "No Detection"
confidence = 0.0
frame_count = 0

def get_color(lbl):
    return COLORS.get(lbl, (160, 160, 160))

def send_signal(lbl):
    if ser and lbl in COMMANDS:
        ser.write(COMMANDS[lbl])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % 20 == 0:
        new_label, new_conf = detect_leaf(frame)
        if new_label != "No Detection":
            label = new_label
            confidence = new_conf
            if new_label != last_label:
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                log.append((timestamp, label, confidence))
                if len(log) > 10:
                    log.pop(0)
                send_signal(label)
                last_label = new_label
        else:
            label = "No Detection"
            confidence = 0.0
            last_label = "No Detection"

    frame_count += 1

    color = get_color(label)
    h, w, _ = frame.shape

    cv2.rectangle(frame, (10, 10), (w - 10, 65), (0, 0, 0), -1)
    cv2.rectangle(frame, (10, 10), (w - 10, 65), color, 2)

    display_label = label if len(label) <= 22 else label[:22]
    cv2.putText(frame, display_label, (20, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)
    cv2.putText(frame, f"Confidence: {confidence * 100:.1f}%", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (220, 220, 220), 1, cv2.LINE_AA)

    min_height = max(h, 500)
    sidebar = np.full((min_height, 360, 3), (28, 24, 20), dtype=np.uint8)
    frame_padded = np.zeros((min_height, w, 3), dtype=np.uint8)
    frame_padded[:h, :] = frame
    frame = frame_padded

    cv2.rectangle(sidebar, (0, 0), (360, 52), (38, 32, 26), -1)
    cv2.putText(sidebar, "NUTRIENT DISPENSER", (16, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.line(sidebar, (0, 52), (360, 52), (55, 46, 38), 1)

    cv2.putText(sidebar, "CURRENT STATUS", (16, 76), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (160, 160, 160), 1, cv2.LINE_AA)
    cv2.rectangle(sidebar, (16, 88), (344, 158), (40, 34, 28), -1)
    cv2.rectangle(sidebar, (16, 88), (344, 158), color, 2)

    status_line1 = label if len(label) <= 20 else label[:20]
    status_line2 = label[20:] if len(label) > 20 else ""
    cv2.putText(sidebar, status_line1, (26, 112), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA)
    if status_line2:
        cv2.putText(sidebar, status_line2, (26, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2, cv2.LINE_AA)
    cv2.putText(sidebar, f"Confidence: {confidence * 100:.1f}%", (26, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 200, 200), 1, cv2.LINE_AA)

    cv2.line(sidebar, (16, 172), (344, 172), (55, 46, 38), 1)
    cv2.putText(sidebar, "DETECTION LOG (LAST 10)", (16, 194), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (160, 160, 160), 1, cv2.LINE_AA)

    for idx, (t, lbl, c) in enumerate(reversed(log)):
        row_y = 220 + idx * 26
        if row_y > min_height - 10:
            break
        dot_color = get_color(lbl)
        short_lbl = lbl if len(lbl) <= 18 else lbl[:18]
        cv2.circle(sidebar, (26, row_y - 4), 4, dot_color, -1, cv2.LINE_AA)
        cv2.putText(sidebar, t, (38, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1, cv2.LINE_AA)
        cv2.putText(sidebar, short_lbl, (112, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (225, 225, 225), 1, cv2.LINE_AA)
        cv2.putText(sidebar, f"{int(c * 100)}%", (318, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, dot_color, 1, cv2.LINE_AA)

    dashboard = np.hstack((frame, sidebar))
    cv2.imshow("Nutrient Dispenser", dashboard)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
if ser:
    ser.close()
cv2.destroyAllWindows()
