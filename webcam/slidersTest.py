import cv2
import sliders
import library.functions as functions
print(1)
sliders.start(0)
print(2)
cap = cv2.VideoCapture(0)
print(3)
while True:
    isTrue, frame = cap.read()
    filter = sliders.getFilter()
    hue = filter["hue"]
    val = filter["val"]
    sat = filter["sat"]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]))
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    if cv2.waitKey(10) & 0xFF == ord("d"):
        break