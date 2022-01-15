import cv2
import numpy




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

def Center(img, leftMostCoordinate, rightMostCoordinate):
    h, w, c = img.shape
    xLeft = leftMostCoordinate[0]

    xRight = rightMostCoordinate[0]
    Offset = int(w/10)

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



