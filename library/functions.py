import math
from re import X
from tkinter import W
import cv2
import numpy
import library.constants as constants



#def center(img, coordinate):
#    h, w, c = img.shape
#
#
#    y = img[1]
#    x = img[0]
#    Offset = int(w/10)
#
    #yRange = range(h/2-Offset, h/2+Offset)
    #xRange = range(w/2-Offset, w/2+Offset)

#    toReturn = {
#        "y":"centered",
#        "x":"centered"
#    }

#    if y < h/2-Offset:
#        toReturn["y"] = "up"
#    elif y > h/2 + Offset:
#        toReturn["y"] = "down"
#
#    if x < w/2-Offset:
#        toReturn["x"] = "right"
#    elif x > w/2 + Offset:
#        toReturn["x"] = "left"
#    
#    return toReturn

# HELPER FUNCTIONS
def HSVFilter(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (constants.hue[0], constants.sat[0], constants.val[0]), (constants.hue[1], constants.sat[1], constants.val[1]))
    return mask

def filterContours(contours, min_size = constants.MIN_AREA_CONTOUR):
    tempCounters = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_size:
            continue
        tempCounters.append(contour)
    return tempCounters

def get_leftmost_and_rightmost_coords(img, convex_hulls:list):
    h, w, c = img.shape

    minX = None
    maxX = None

    for cx, cy in convex_hulls:
        if not minX:
            minX = (cx, cy)
            maxX = (cx, cy)
        if cx < minX[0]:
            minX = (cx, cy)
        if cx > maxX[0]:
            maxX = (cx, cy)

    return [minX,maxX]
    
def Center(img, leftMostCoordinate, rightMostCoordinate):
    h, w, c = img.shape
    xLeft = leftMostCoordinate[0]

    xRight = rightMostCoordinate[0]
    Offset = int(w/9)

    distanceFromSideL = w - xRight - Offset
    distanceFromSideR = w - xRight + Offset

    # 1 == go right
    # -1 == go left
    # 0 == centered
    if xLeft < distanceFromSideL:
        return 1
    elif xLeft > distanceFromSideR:
        return -1
    return 0

# MATH
def getVertex(a,b,c):
    "y = ax^2+bx+c"
    return ((-b / (2 * a)), (((4 * a * c) - (b * b)) / (4 * a)))

def getAngle(img, coordinate:tuple):
    h, w, c = img.shape
    fov = 45
    cX = coordinate[0]
    cY = coordinate[1]

    centerPixel = (int(h/2), int(w/2))
    distanceFromCenter = (math.sqrt(((cX-centerPixel[0])**2)+((cY-centerPixel[1])**2)))
    pixelRepresent = fov/(math.sqrt(h**2 + w**2))
    return int(pixelRepresent*distanceFromCenter)

#def getPixelRepresent(img, pixel):
#    h, w, c = img.shape
#    fov = 45
#    pixelRepresent = fov/(math.sqrt(h**2 + w**2))
#    return pixelRepresent
def angleToRadians(degrees):
    return degrees*(math.pi/180)