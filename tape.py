import cv2
import numpy as np

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