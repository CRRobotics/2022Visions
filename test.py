import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("error")
    quit()

while True:
    isTrue, frame = cap.read()
    if isTrue:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Threshold of blue in HSV space
        lowerGreen = np.array([40, 40, 40])
        upperGreen = np.array([70, 255, 255])

        # preparing the mask to overlay
        mask = cv.inRange(hsv, lowerGreen, upperGreen)

        # The black region in the mask has the value of 0,
        # so when multiplied with original image removes all non-blue regions
        result = cv.bitwise_and(frame, frame, mask = mask)

        cv.imshow('frame', frame)
        cv.imshow("frame", mask)
        cv.imshow('mask', mask)
        cv.imshow('result', result)
        if cv.waitKey(20) & 0xFF == ord("d"):
            print("done")
            break
    else:
        print("done")
        break