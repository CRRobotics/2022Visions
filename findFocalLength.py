import cv2 as cv
import numpy as np
import imutils
from imutils import paths

def findMarker(img):
    # grayscale, blur, detect edges
    gray = cv.cvtColor(img, cv.COLOR_BGR2Gray)
    blur = cv.GaussianBlur(gray, (5, 5,), 0)
    edges = cv.Canny(blur, 35, 125)

    # assume largest counter is tape
    cnts = cv.findContours(edges.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key = cv.contourArea)
    
    # compute the bounding box of the of the paper region and return it
    return cv.minAreaRect(c)