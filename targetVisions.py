import cv2
import numpy as np
import math
import functions

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

hue = [0, 180]
sat = [73, 255]
val = [255, 255]

cap = cv2.VideoCapture(1)


def HSVFilter(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]))
    return mask

def main():
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
            
            if convexHulls:
                print("\n\n\n")
                cx = convexHulls[0].tolist()
                coordsOfConvexHulls = [x[0] for x in cx] #[[x1,y1], [x2,y2],[x3,y3],...]
                #im having a stroke trying to get a list of (x,y) coordinates
                c = functions.get_leftmost_and_rightmost_coords(frame, coordsOfConvexHulls)
                if c:
                    print(functions.Center(frame, c[0],c[1]))
                #action = functions.Center(frame, c[0], c[1])
                #print(action)


            cv2.drawContours(frame, convexHulls, -1, (0, 0, 255), 1)

            cv2.imshow("mask", mask)
            cv2.imshow("frame", frame)

            if cv2.waitKey(20) & 0xFF == ord("d"):
                print("done")
                break
        except:
            pass

if __name__ == "__main__":
    main()