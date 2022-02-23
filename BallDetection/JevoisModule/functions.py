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

def HSVFilterRED(frame):
    "returns filtered img"
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (constants.hue_R[0], constants.sat_R[0], constants.val_R[0]), (constants.hue_R[1], constants.sat_R[1], constants.val_R[1]))
    return mask

def filterContours(contours, min_size = constants.MIN_AREA_CONTOUR):
    "filters out contours that are smaller than min_size and of certain vertices and of valid solidity"
    filteredContours = []
    numContours = 1 if len(contours) > 1 else len(contours)
    sortedContours = sorted(contours, key=lambda contour: -cv2.contourArea(contour))
    finalContours = []
    for i in range(numContours):
        # area = cv2.contourArea(sortedContours[i])
        # if area < min_size:
        #     break
        if len(sortedContours[i]) > constants.MIN_VERTICES_CONTOUR:
            area = cv2.contourArea(sortedContours[i])
            hull = cv2.convexHull(sortedContours[i])
            solid = 100 * area / cv2.contourArea(hull)
            if (solid > constants.SOLIDITY[0] and solid < constants.SOLIDITY[1]):
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

def getGroundHorizontalAngle(verticalOptical, horizontalOptical, tilt = constants.CAMERA_ANGLE):
    "TAKES IN RADIANS, OUTPUTS RADIANS"
    if tilt == 0:
        return horizontalOptical
    return math.atan(math.tan(horizontalOptical) * (math.tan(tilt)/math.sin(tilt)))

def getDistance(verticalOptical, horizontalOptical, height_to_target = constants.HEIGHT_TO_TARGET, tilt = constants.CAMERA_ANGLE):
    "takes in radians for angles, and outputs the same unit as HEIGHT_TO_TARGET"
    if tilt == 0:
        return (1/math.cos(horizontalOptical))*(height_to_target/math.tan(verticalOptical))
    return (1/math.cos(math.atan(math.tan(horizontalOptical) * (math.tan(tilt)/math.sin(tilt))))) * (height_to_target/math.tan(tilt + verticalOptical))


def getCorrection(reportedDistance, slope=constants.ERROR_SLOPE, intercept = constants.ERROR_INTERCEPT):
    "returns actual distance based on error calculation takes in raw distance from getDistance()"
    approx_Error = slope * reportedDistance + intercept
    return reportedDistance + approx_Error

def getDistanceRelativeToBot(actualDistance, groundHorizontalAngle, distanceToMiddleOfBot=constants.DISTANCE_FROM_MIDDLE_OF_BOT):
    "returns distance relative to the bot based on approx distance from getActualDistance() and ground Horizontal angle from getGroundHorizontalAngle() This will be sent to the rio via serial"
    if groundHorizontalAngle < 0:
        phi = math.pi/2-abs(groundHorizontalAngle)
        d = math.atan((math.sin(phi) * actualDistance)/(distanceToMiddleOfBot + math.cos(phi) * distanceToMiddleOfBot))
        return (math.sin(phi) * actualDistance)
    else:
        phi = math.pi/2-abs(groundHorizontalAngle)
        cb = math.cos(phi) * actualDistance
        db = abs(distanceToMiddleOfBot - cb)
        ab = math.tan(phi) * cb
        d = math.atan(ab/db)
        return ab/math.sin(d)


def getAngleRelativeToCenterOfRotation(actualDistance, groundHorizontalAngle, distanceToMiddleOfBot=constants.DISTANCE_FROM_MIDDLE_OF_BOT, distanceToCenterOfRotation = constants.DISTANCE_FROM_MIDDLE_TO_CENTER_OF_ROTATION):
    """returns the angle (radians) relative to the center of rotation. 
    This will be send through serial to the rio"""
    if groundHorizontalAngle < 0:
        print("less than 0")
        phi = math.pi/2-abs(groundHorizontalAngle)
        tg = math.sin(phi) * actualDistance
        th = tg + distanceToCenterOfRotation
        b = (th/math.tan(phi)) - (distanceToCenterOfRotation/math.tan(phi))
        hr = b + distanceToMiddleOfBot
        r = math.atan(th/hr)
        return -(math.pi/2-r)
    else:
        cnst = 1
        phi = math.pi/2-groundHorizontalAngle
        cb = math.cos(phi) * actualDistance
        dbRAW = distanceToMiddleOfBot - cb
        if dbRAW > 0:
            cnst = -1
        db = abs(dbRAW)
        ab = math.tan(phi) * cb
        abP = distanceToCenterOfRotation + ab
        center = math.atan(abP/db)
        return cnst * (math.pi/2-center)




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
    centerPixel = (int(w / 2), int(h / 2))
    if orientation == 0:
        distanceFromCenter = cX - centerPixel[0]
        angle = constants.RADIANS_PER_PIXEL_X * distanceFromCenter
    elif orientation == 1:
        distanceFromCenter = centerPixel[1] - cY
        angle = constants.RADIANS_PER_PIXEL_Y * distanceFromCenter + angleToRadians(constants.CAMERA_ANGLE)
    return angleToDegrees(angle)

def angleToRadians(degrees):
    "degrees to radians"
    return degrees*(math.pi / 180)

def angleToDegrees(radians):
    "radians to degrees"
    return (radians / math.pi) * 180

