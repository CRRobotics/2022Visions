import cv2
import constants



def HSVFilter(frame):
    "returns filtered img"
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (constants.hue[0], constants.sat[0], constants.val[0]), (constants.hue[1], constants.sat[1], constants.val[1]))
    return mask

def filterContours(contours, min_size = constants.MIN_AREA_CONTOUR):
    "filters out contours that are smaller than min_size"
    filteredContours = []
    numContours = 4 if len(contours) > 4 else len(contours)
    sortedContours = sorted(contours, key=lambda contour: -cv2.contourArea(contour))
    for i in range(numContours):
        # area = cv2.contourArea(sortedContours[i])
        # if area < min_size:
        #     break
        filteredContours.append(sortedContours[i])
    return filteredContours