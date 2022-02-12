import cv2
import numpy as np
import math
import os
import sys

# global variables go here:\
# test script 0
testVar = 0

# CONSTANTS
# these are random numbers for now, will change later
# HEIGHT_OF_CAMERA        = 38.5
HEIGHT_OF_CAMERA        = 29.5
# HEIGHT_OF_TARGET        = 107.0
HEIGHT_OF_TARGET        = 66.0
HEIGHT_TO_TARGET        = HEIGHT_OF_TARGET - HEIGHT_OF_CAMERA
# CAMERA_ANGLE		    = 16.4
CAMERA_ANGLE		    = 30.0 * (math.pi / 180)


# THIS VALUE HAS BEEN DETERMINED BY CLOSE-TESTING, CAHNGE THESE VALUES LATER
MIN_AREA_CONTOUR        = 1.0

FOV_X                   = 54 * (math.pi / 180)
FOV_Y                   = 41 * (math.pi / 180)

RADIANS_PER_PIXEL_X     = FOV_X / 320
RADIANS_PER_PIXEL_Y     = FOV_Y / 240

# CAMERA_EXPERIMENTAL_DISTANCE = 92
# CAMERA_X = 85
# CAMERA_Y = 47
# FOV_X = math.atan((CAMERA_X / 2) / CAMERA_EXPERIMENTAL_DISTANCE) * 2
# FOV_Y = math.atan((CAMERA_Y / 2) / CAMERA_EXPERIMENTAL_DISTANCE) * 2
# RADIANS_PER_PIXEL_X = FOV_X / 1280
# RADIANS_PER_PIXEL_Y = FOV_Y / 720
# RADIANS_PER_PIXEL_X = FOV_X / 640
# RADIANS_PER_PIXEL_Y = FOV_Y / 480

# values for cafeteria
# hue = [45, 122]
# sat = [167, 255]
# val = [186, 255]

# hue = [45, 122]
# sat = [131, 255]
# val = [158, 255]

hue = [73, 122]
sat = [78, 255]
val = [158, 255]

# HELPER FUNCTIONS
def HSVFilter(frame):
    "returns filtered img"
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]))
    return mask

def filterContours(contours, min_size = MIN_AREA_CONTOUR):
    "filters out contours that are smaller than min_size"
    filteredContours = []
    numContours = 4 if len(contours) > 4 else len(contours)
    sortedContours = sorted(contours, key=lambda contour: -cv2.contourArea(contour))
    for i in range(numContours):
        area = cv2.contourArea(sortedContours[i])
        if area < min_size:
            break
        filteredContours.append(sortedContours[i])
    return filteredContours

def getCenters(img, contours):
    """_, contours, _ = cv2.findContours 
    returns centers of all polygons"""
    centers = []
    for i in range(len(contours)):
        moments = cv2.moments(contours[i])
        centers.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
        cv2.circle(img, centers[-1], 3, (0, 0, 0), -1)
        # try:
        #     print("--------------------------------")
        #     print("m00: ", moments['m00'])
        #     print("m10: ", moments['m10'])
        #     print("m01: ", moments['m01'])
        #     print("contour:", contours[i])
        #     x = moments['m10'] / moments['m00']
        #     y = moments['m01'] / moments['m00']
        #     centers.append((int(x), int(y)))
        #     cv2.circle(img, centers[-1], 3, (0, 0, 0), -1)
        # except Exception as e:
        #     print("-------------------------------")
        #     print(moments)
        #     print(moments['m00'])
        #     print("contour:", contours[i])
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #     print(exc_type, fname, exc_tb.tb_lineno)
        #     centers.append([0, 0])
    return centers

def getParabola(frame, centers):
    "draws parabola on frame, returns vertex (x,y)"
    h, w, _ = frame.shape

    yVals = [x[1] for x in centers]
    xVals = [x[0] for x in centers]

    # coefficients of parabola that best fits centroids
    fit = np.polyfit(xVals, yVals, 2)
    a, b, c = fit

    # x points for drawing the parabols
    xVals = np.linspace(1, w - 1, 100).astype(np.int32)

    # returns Y values for parabola
    fit_equation = a * np.square(xVals) + b * xVals + c 

    # drawing parabola
    newXY = list(zip(xVals, fit_equation))
    ctr = np.array(newXY).reshape((-1,1,2)).astype(np.int32)
    cv2.drawContours(frame, [ctr], -1, (255, 0, 0), 1)

    # for some reason, going up decreases the y value
    # getting vertex
    #plotting vertex
    vertex = getVertex(a,b,c)
    cv2.circle(frame, vertex, 3, (0, 0, 255), -1)
    return vertex

def getVertex(a, b, c):
    "y = ax^2+bx+c"
    return (int(-b / (2 * a)), int(((4 * a * c) - (b * b)) / (4 * a)))

def angleToRadians(degrees):
    "degrees to radians"
    return degrees * (math.pi / 180)

def angleToDegrees(radians):
    "radians to degrees"
    return (radians / math.pi) * 180

# gets the angle based on the fov, orientation, and coordinate of the parabola representing the target
# @param img The image or frame to use
# @param orientation The orientation of the angle (0 gets horizontal angle to the coordinate, 1 gets vertical angle to the tape)
# NOTE: vertical angle is only accurate if the x-coordinate of the center coordinate is in the middle of the frame
# @param coordinate The coordinate of the center of the tape or parabola
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
        angle = RADIANS_PER_PIXEL_X * distanceFromCenter
    elif orientation == 1:
        distanceFromCenter = centerPixel[1] - cY
        angle = RADIANS_PER_PIXEL_Y * distanceFromCenter + CAMERA_ANGLE
    return angle
    # pixelRepresent = fov/(math.sqrt(h ** 2 + w ** 2))
    # return int(pixelRepresent * distanceFromCenter)

# converts the horizontal angle relative to the optical axis to the horizontal angle relative to the ground
def horizontalOpticalToGround(angle):
    return math.atan((1 / math.cos(CAMERA_ANGLE)) * math.tan(angle))

# converts the vertical angle relative to the optical axis to the vertical angle relative to the ground
def verticalOpticalToGround(opticalHorizontalAngle, opticalVerticalAngle):
    return math.asin(math.cos(CAMERA_ANGLE) * math.sin(opticalVerticalAngle) + \
        math.cos(opticalHorizontalAngle) * math.cos(opticalVerticalAngle) * math.sin(CAMERA_ANGLE))

# determines the horizontal distance to the target based on the angle and height of the target relative to the robot
def getHorizontalDistance(angle, degrees=True, heightToTarget=HEIGHT_TO_TARGET):
    return heightToTarget / math.tan(angleToRadians(angle)) if degrees else heightToTarget / math.tan(angle)
    
# runPipeline() is called every frame by Limelight's backend.
def runPipeline(image, llrobot):
    llpython = [0, 0, 0, 0, 0, 0, 0, 0]
    # STEP 1: IDENTIFY THE TARGET

    # getting HSV filter to distinguish the target from surroundings
    mask = HSVFilter(image)

    # finding and filtering the contours in the image to only get the contour of the tape
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = filterContours(contours)
    convexHulls = [cv2.convexHull(contour) for contour in contours]
    largestConvex = convexHulls[0] if len(convexHulls) > 0 else np.array([[]])

    # getting convex hulls
    if len(convexHulls) > 0:
        
        # if convexHulls:
        #     print("\n\n\n")
        #     cx = convexHulls[0].tolist()
        #     coordsOfConvexHulls = [x[0] for x in cx] #[[x1,y1], [x2,y2],[x3,y3],...]
        #     #im having a stroke trying to get a list of (x,y) coordinates
        #     c = get_leftmost_and_rightmost_coords(image, coordsOfConvexHulls)
        #     if c:
        #         print(Center(image, c[0],c[1]))
        #     #action = Center(image, c[0], c[1])
        #     #print(action)
        
        # drawing convexHulls on the image to display
        cv2.drawContours(image, convexHulls, -1, (0, 0, 255), 1)

        # getting the centers of the contours in the image
        centers = getCenters(image, convexHulls)
        
        # STEP 2: DETERMINE THE PARABOLIC FIT WITH LEAST SQUARES USING THE CENTER COORDINATES OF THE TAPE
        vertex = getParabola(image, centers) if len(centers) >= 3 else None

        # STEP 3: DETERMINE HORIZONTAL AND VERTICAL ANGLES TO TARGET (FROM THE ROBOT)
        opticalHorizontalAngle = getAngle(image, 0, vertex) if vertex is not None else getAngle(image, 0, centers[0])
        groundHorizontalAngle = horizontalOpticalToGround(opticalHorizontalAngle)
        opticalVerticalAngle = getAngle(image, 1, vertex) if vertex is not None else getAngle(image, 1, centers[0])
        groundVerticalAngle = verticalOpticalToGround(opticalHorizontalAngle, opticalVerticalAngle)

        # STEP 4: DETERMINE HORIZONTAL DISTANCE TO TARGET (FROM THE ROBOT)
        horizontalDistance = getHorizontalDistance(groundVerticalAngle)

        opticalHorizontalAngle = round(angleToDegrees(opticalHorizontalAngle), 2)
        opticalVerticalAngle = round(angleToDegrees(opticalVerticalAngle), 2)
        groundHorizontalAngle = round(angleToDegrees(groundHorizontalAngle), 2)
        groundVerticalAngle = round(angleToDegrees(groundVerticalAngle), 2)
        horizontalDistance = round(angleToDegrees(horizontalDistance), 2)

        # writing to the NetworkTable
        llpython = [groundHorizontalAngle, horizontalDistance, 0, 0, 0, 0, 0, 0]

        # displaying the horizontal and vertical angles on the image
        cv2.putText(image, "Horizontal Angle: " + str(groundHorizontalAngle) + "  Vertical Angle: " + str(groundVerticalAngle), \
            (image.shape[1] - 310, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)

        # displaying the horizontal distance to the target on the image
        cv2.putText(image, "Distance: " + str(horizontalDistance), \
            (image.shape[1] - 300, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
    # make sure to return a contour,
    # an image to stream,
    # and optionally an array of up to 8 values for the "llpython"
    # networktables array
    return largestConvex, image, llpython