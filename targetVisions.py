import cv2
import numpy as np
import math

# CONSTANTS
# these are random numbers for now, will change later
WIDTH                   = 5.0
HEIGHT                  = 480.0
HEIGHT_OF_CAMERA        = 38.5
HEIGHT_OF_TARGET        = 102.25 #8 * 12 + 2.25
HEIGHT_TO_TARGET        = HEIGHT_OF_TARGET - HEIGHT_OF_CAMERA
CAMERA_ANGLE		    = 16.4
OUTER_TARGET_WIDTH      = 39.25
INNER_TARGET_DEPTH      = 29.25
BALL_RADIUS             = 3.5
MIN_AREA_CONTOUR        = 50.0

# filter = {"hue": [57, 111], "sat":[148, 255], "val": [255, 255]}
# hue = [57, 111]
# sat = [148, 255]
# val = [255, 255]

hue = [73, 112]
sat = [108, 174]
val = [162, 255]

cap = cv2.VideoCapture(0)

while True:
    try:
        isTrue, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]))

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tempCounters = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < MIN_AREA_CONTOUR:
                continue
            tempCounters.append(contour)
        contours = tempCounters

        convexHulls = [cv2.convexHull(contour) for contour in contours]
        cv2.drawContours(frame, convexHulls, -1, (0, 0, 255), 1)

        cv2.imshow("mask", mask)
        cv2.imshow("frame", frame)

        if cv2.waitKey(20) & 0xFF == ord("d"):
            print("done")
            break
    except:
        pass