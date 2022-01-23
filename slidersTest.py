import cv2
import sliders
import library.functions as functions

sliders.start(0)
print(1)
cap = cv2.VideoCapture(0)
print(2)
while True:
    isTrue, frame = cap.read()
    filter = sliders.getFilter()
    hue = filter["hue"]
    val = filter["val"]
    sat = filter["sat"]
    mask = functions.HSVFilter(frame)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    if cv2.waitKey(10) & 0xFF == ord("d"):
        break