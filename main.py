import cv2
import numpy as np  

cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()

    
    #togray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #ret, thresh = cv2.threshold(togray, 150,255, cv2.THRESH_BINARY)


    #contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE,method=cv2.CHAIN_APPROX_NONE)


    #cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    mask = cv2.inRange(hsv, (57, 150,255), (111, 255,255))

    ## slice the green
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    cv2.imshow("Image",green)
    cv2.waitKey(1)