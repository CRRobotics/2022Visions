import cv2
import constants
import math

def putCenterPixelIn(frame):
    h, w, c = frame.shape
    centerPixel = (int(w / 2), int(h / 2))
    cv2.circle(frame, centerPixel, 3, (255, 0, 255), -1)

def HSVFilterBLUE(frame):
    "returns filtered img"
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (constants.hue_B[0], constants.sat_B[0], constants.val_B[0]), (constants.hue_B[1], constants.sat_B[1], constants.val_B[1]))
    return mask

def filterContours(contours, min_size = constants.MIN_AREA_CONTOUR):
    "filters out contours that are smaller than min_size"
    filteredContours = []
    numContours = 2 if len(contours) > 2 else len(contours)
    sortedContours = sorted(contours, key=lambda contour: -cv2.contourArea(contour))
    for i in range(numContours):
        # area = cv2.contourArea(sortedContours[i])
        # if area < min_size:
        #     break
        filteredContours.append(sortedContours[i])
    return filteredContours



def getCenters(img,contours):
    """_, contours, _ = cv2.findContours 
    returns centers of all polygons"""

    centres = []
    for i in range(len(contours)):
        moments = cv2.moments(contours[i])
        centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
        cv2.circle(img, centres[-1], 3, (0, 0, 0), -1)
    
    return centres

def getHorizontalDistance(angle, degrees=True, heightToTarget=constants.HEIGHT_TO_TARGET):
    return heightToTarget / math.tan(angleToRadians(angle)) if degrees else heightToTarget / math.tan(angle)
    

def groundAngleToHypotnuse(angle, distance, inRadians = False):
    if not inRadians:
        return abs(distance / math.cos(angleToRadians(angle)))
    else:
        return abs(distance / math.cos(angle))

# converts the horizontal angle relative to the optical axis to the horizontal angle relative to the ground
def horizontalOpticalToGround(angle):
    return math.atan((1 / math.cos(constants.CAMERA_ANGLE)) * math.tan(angle))


def getAngle(img, orientation:int, coordinate:tuple):
    """
 gets the angle based on the fov, orientation, and coordinate of the parabola representing the target
 @param img The image or frame to use
 @param orientation The orientation of the angle (0 gets horizontal angle to the coordinate, 1 gets vertical angle to the tape)
 NOTE: vertical angle is only accurate if the x-coordinate of the center coordinate is in the middle of the frame
 @param coordinate The coordinate of the center of the tape or parabola"""
    h, w, c = img.shape
    cX = coordinate[0]
    cY = coordinate[1]

    # centerPixel = (int(h/2), int(w/2))
    # distanceFromCenter = (math.sqrt(((cX - centerPixel[0]) **2 ) + ((cY - centerPixel[1]) ** 2)))
    centerPixel = (int(w / 2), int(h / 2))
    if orientation == 0:
        distanceFromCenter = cX - centerPixel[0]
        angle = constants.RADIANS_PER_PIXEL_X * distanceFromCenter
    elif orientation == 1:
        distanceFromCenter = centerPixel[1] - cY
        angle = constants.RADIANS_PER_PIXEL_Y * distanceFromCenter + angleToRadians(constants.CAMERA_ANGLE)
    return angleToDegrees(angle)
    # pixelRepresent = fov/(math.sqrt(h ** 2 + w ** 2))
    # return int(pixelRepresent * distanceFromCenter)

def angleToRadians(degrees):
    "degrees to radians"
    return degrees*(math.pi / 180)

def angleToDegrees(radians):
    "radians to degrees"
    return (radians / math.pi) * 180

