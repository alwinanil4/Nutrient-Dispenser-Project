import cv2
from best import detect_leaf

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
if ret:
    label, confidence = detect_leaf(frame)
    print(label, confidence)
cap.release()
