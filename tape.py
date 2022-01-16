from inspect import ismethoddescriptor
from unittest import makeSuite
import cv2
import numpy as np
import targetVisions
import library.helperFunctions as helperFunctions

class reflectiveTape():
    """reflective tape object, will hold the convex hulls of the object. trying to get convex hulls for each object"""
    def __init__(self, width) -> None:
        self.width = width

    @staticmethod
    def getCenters(img,contours):
        """_, contours, _ = cv2.findContours 
        returns centers of all polygons"""

        centres = []
        for i in range(len(contours)):
            moments = cv2.moments(contours[i])
            centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
            cv2.circle(img, centres[-1], 3, (0, 0, 0), -1)
        
        return centres

def main():
    cap = cv2.VideoCapture(1)
    while True:
        success, frame = cap.read()

        mask = targetVisions.HSVFilter(frame)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours = helperFunctions.filterSmallContours(contours)
        try:
            centers = reflectiveTape.getCenters(frame, contours=contours)
        except:
            pass

        convexHulls = [cv2.convexHull(contour) for contour in contours]
        cv2.drawContours(frame, convexHulls, -1, (0, 0, 255), 1)


        cv2.imshow("image", frame)
        cv2.waitKey(1)
        break

if __name__ == "__main__":
    main()