import cv2 as cv
import numpy as np
import imutils
from imutils import paths

def findMarker(img):
    # grayscale, blur, detect edges
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5,), 0)
    edges = cv.Canny(blur, 35, 125)
    cv.imshow("edges", edges)
    # assume largest counter is tape
    cnts = cv.findContours(edges.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key = cv.contourArea)
    
    # compute the bounding box of the of the paper region and return it
    return cv.minAreaRect(c)

def getDistance(focalLength, width, pixelWidth):
    return (focalLength * width) / pixelWidth

WIDTH = 5.0
DISTANCE = 12.0

if __name__ == "__main__":
    img = cv.imread("tape8.jpg")
    marker = findMarker(img)
    print("marker: ", marker[1][0])
    focalLength = (marker[1][0] * DISTANCE) / WIDTH
    inches = getDistance(focalLength, WIDTH, marker[1][0])
    print("focalLength: ", focalLength)
    box = cv.cv.BoxPoints(marker) if imutils.is_cv2() else cv.boxPoints(marker)
    box = np.int0(box)
    cv.drawContours(img, [box], -1, (0, 255, 0), 2)
    cv.putText(img, "%.2fin" % inches, (img.shape[1] - 200, img.shape[0] - 40), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
    cv.imshow("img", img)

    cv.waitKey(0)