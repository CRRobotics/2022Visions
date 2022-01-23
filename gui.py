import cv2
import numpy as np

#GET THESE FROM CONSTANTS
Hue = [0,255]
Sat = [0,255]
Val = [0,255]


def HSVFilter(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (Hue[0], Sat[0], Val[0]), (Hue[1], Sat[1], Val[1]))
    return mask

def nothing(x):
    pass

# Create a black image, a window
cv2.namedWindow('image')



# create trackbars for color change
cv2.createTrackbar('HueLow','image',0,255,nothing)
cv2.createTrackbar('HueMax','image',0,255,nothing)
cv2.createTrackbar('SatLow','image',0,255,nothing)
cv2.createTrackbar('SatMax','image',0,255,nothing)
cv2.createTrackbar('ValLow','image',0,255,nothing)
cv2.createTrackbar('ValMax','image',0,255,nothing)

cap = cv2.VideoCapture(0)
while(1):
    istrue, img = cap.read()
    cv2.imshow("image", img)

    # get current positions of four trackbars
    HueLow = cv2.getTrackbarPos("HueLow", "image")
    HueMax = cv2.getTrackbarPos("HueMax", "image")

    SatLow = cv2.getTrackbarPos("SatLow", "image")
    SatMax = cv2.getTrackbarPos("SatMax", "image")

    ValLow = cv2.getTrackbarPos("ValLow", "image")
    ValMax = cv2.getTrackbarPos("ValMax", "image")

    #CHANGE THE ONES FROM CONSTANTS
    Hue = [HueLow, HueMax]
    Sat = [SatLow, SatMax]
    Val = [ValLow, ValMax]







    img = HSVFilter(img)
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break


    

cv2.destroyAllWindows()