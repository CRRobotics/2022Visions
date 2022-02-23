import cv2
import numpy as np
import math
import os
import sys

# global variables go here:
# test script 0
count = 0

# CONSTANTS

CAMERA_EXPOSURE         = 16 # 11 # (0.1 ms) to be set in "input" tab in limelight

# HEIGHT_OF_CAMERA        = 29.0   # actual
# HEIGHT_OF_TARGET        = 104.0  # actual

HEIGHT_OF_CAMERA        = 29.0   # test hub
HEIGHT_OF_TARGET        = 102.0  # test hub

# HEIGHT_OF_CAMERA        = 32.5   # test hub 2
# HEIGHT_OF_TARGET        = 102.0  # test hub 2
# HEIGHT_OF_CAMERA        = 32.0   # test hoop
# HEIGHT_OF_TARGET        = 74.0  # test hoop
# HEIGHT_OF_CAMERA        = 16.0   # test hoop 2
# HEIGHT_OF_TARGET        = 74.0  # test hoop 2

# HEIGHT_OF_CAMERA        = 29.0   # bert house
# HEIGHT_OF_TARGET        = 71.0  # bert house

HEIGHT_TO_TARGET        = HEIGHT_OF_TARGET - HEIGHT_OF_CAMERA
CAMERA_ANGLE		    = 28.1 * (math.pi / 180)
WIDTH                   = 320
HEIGHT                  = 240

MIN_AREA_CONTOUR        = 1.0

FOV_X                   = 59.6 * (math.pi / 180)
FOV_Y                   = 45.7 * (math.pi / 180)

RADIANS_PER_PIXEL_X     = FOV_X / WIDTH
RADIANS_PER_PIXEL_Y     = FOV_Y / HEIGHT

FOCAL_DISTANCE          = (WIDTH / 2) / math.tan((FOV_X) / 2)

# values for cafeteria
# hue = [45, 122]
# sat = [167, 255]
# val = [186, 255]

# hue = [45, 122]
# sat = [131, 255]
# val = [158, 255]

# hue = [73, 122]
# sat = [78, 255]
# val = [158, 255]

# values for E1
# hue = [73, 122]
# sat = [174, 255]
# val = [158, 255]

hue = [73, 122]
sat = [0, 255]
val = [146, 255]

# HELPER FUNCTIONS
def printConstants():
    print("CAMERA_EXPOSURE: ", CAMERA_EXPOSURE)
    print("HEIGHT_OF_CAMERA: ", HEIGHT_OF_CAMERA)
    print("HEIGHT_OF_TARGET: ", HEIGHT_OF_TARGET)
    print("HEIGHT_TO_TARGET: ", HEIGHT_TO_TARGET)
    print("CAMERA_ANGLE: ", CAMERA_ANGLE)
    print("MIN_AREA_CONTOUR: ", MIN_AREA_CONTOUR)
    print("FOV_X: ", FOV_X)
    print("FOV_Y: ", FOV_Y)
    print("RADIANS_PER_PIXEL_X: ", RADIANS_PER_PIXEL_X)
    print("RADIANS_PER_PIXEL_Y: ", RADIANS_PER_PIXEL_Y)

def HSVFilter(frame):
    "returns filtered img"
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]))
    return mask

# Alternative to HSVFilter
# Subtract red channel from green channel to filter image
def binarizeSubt(img):
    blue, green, red = cv2.split(img)
    # print(type(blue[0][0]), type(green[0][0]), type(red[0][0]))
    diff = cv2.subtract(green, red)
    # ret, binImage = cv2.threshold(diff, 0, 255, cv2.THRESH_OTSU)
    ret, binImage = cv2.threshold(diff, 79, 255, cv2.THRESH_BINARY)
    # ret, binImage = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # binImage = cv2.cvtColor(binImage, cv2.COLOR_BGR2GRAY) # idk if we need this
    return binImage

def binarizeSubt2(img):
    blue, green, red = cv2.split(img)
    cyan = blue.astype("float32") * 0.5 + green.astype("float32") * 0.5
    cyan = cyan.astype("uint8")
    diff = cv2.subtract(cyan, red)
    diff.astype("uint8")
    ret, binImage = cv2.threshold(diff, 110, 255, cv2.THRESH_BINARY)
    return binImage

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
def getOpticalAngle(img, orientation:int, coordinate:tuple):
    """
 gets the angle based on the fov, orientation, and coordinate of the parabola representing the target
 @param img The image or frame to use
 @param orientation The orientation of the angle (0 gets horizontal angle to the coordinate, 1 gets vertical angle to the tape)
 NOTE: vertical angle is only accurate if the x-coordinate of the center coordinate is in the middle of the frame
 @param coordinate The coordinate of the center of the tape or parabola"""
    h, w, c = img.shape
    # h = 240
    # w = 360

    px = coordinate[0]
    py = coordinate[1]
    # nx = (1/160) * (px - 159.5)
    # ny = (1/120) * (119.5 - py)

    # distanceFromCenter = (math.sqrt(((cX - centerPixel[0]) **2 ) + ((cY - centerPixel[1]) ** 2)))
    centerPixel = (int(w / 2), int(h / 2))
    if orientation == 0:
        # angle = math.atan(nx / FOCAL_DISTANCE)
        distanceFromCenter = px - centerPixel[0]
        angle = RADIANS_PER_PIXEL_X * distanceFromCenter
    elif orientation == 1:
        # angle = math.atan(ny / (math.sqrt(FOCAL_DISTANCE ** 2 + nx ** 2)))
        distanceFromCenter = centerPixel[1] - py
        # distanceFromCenter = math.sqrt(((px - centerPixel[0]) ** 2) + ((py - centerPixel[1]) ** 2))
        # if centerPixel[1] - py < 0:
        #     distanceFromCenter *= -1
        angle = RADIANS_PER_PIXEL_Y * distanceFromCenter
        # if count == 0:
        #     print("distanceFromCenter: ", distanceFromCenter)
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
def getHorizontalDistance(angle, degrees=False, heightToTarget=HEIGHT_TO_TARGET):
    return heightToTarget / math.tan(angleToRadians(angle)) if degrees else heightToTarget / math.tan(angle)
    
# runPipeline() is called every frame by Limelight's backend.
def runPipeline(image, llrobot):
    llpython = [361.0, -1.0, 0, 0, 0, 0, 0, 0]

    # STEP 1: IDENTIFY THE TARGET

    # getting HSV filter to distinguish the target from surroundings
    # mask1 = HSVFilter(image).astype("float32")
    # mask2 = binarizeSubt(image).astype("float32")
    # mask = 255 * (mask1 + mask2)
    # mask = mask.clip(0, 255).astype("uint8")

    mask = binarizeSubt(image)

    # mask = HSVFilter(image)

    # mask1 = HSVFilter(image)
    # mask2 = binarizeSubt(image)
    # mask = cv2.bitwise_and(mask2, mask2, mask = mask1)
    # # mask = cv2.bitwise_and(mask1, mask1, mask = mask2)

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
        try:
            vertex = getParabola(image, centers) if len(centers) >= 3 else None
        except Exception as e:
            vertex = None

        # STEP 3: DETERMINE HORIZONTAL AND VERTICAL ANGLES TO TARGET (FROM THE ROBOT)
        opticalHorizontalAngle = getOpticalAngle(image, 0, vertex) if vertex is not None else getOpticalAngle(image, 0, centers[0])
        groundHorizontalAngle = horizontalOpticalToGround(opticalHorizontalAngle)
        opticalVerticalAngle = getOpticalAngle(image, 1, vertex) if vertex is not None else getOpticalAngle(image, 1, centers[0])
        groundVerticalAngle = verticalOpticalToGround(opticalHorizontalAngle, opticalVerticalAngle)
        # groundVerticalAngle = opticalVerticalAngle + CAMERA_ANGLE

        # STEP 4: DETERMINE HORIZONTAL DISTANCE TO TARGET (FROM THE ROBOT)
        horizontalDistance = getHorizontalDistance(groundVerticalAngle)

        # global count
        # if count == 0:
        #     # printConstants
        #     print(HEIGHT_TO_TARGET)
        #     print(groundVerticalAngle)
        #     print(horizontalDistance)
        #     print(HEIGHT_TO_TARGET / math.tan(groundVerticalAngle))
        #     count += 1

        opticalHorizontalAngle = round(angleToDegrees(opticalHorizontalAngle), 2)
        opticalVerticalAngle = round(angleToDegrees(opticalVerticalAngle), 2)
        groundHorizontalAngle = round(angleToDegrees(groundHorizontalAngle), 2)
        groundVerticalAngle = round(angleToDegrees(groundVerticalAngle), 2)
        horizontalDistance = round(horizontalDistance, 2)

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

# if __name__ == "__main__":
#     printConstants()
#     verticalAngle = getAngle(1, (270, 240))
#     print("verticalAngle: ", angleToDegrees(verticalAngle))
#     horizontalDistance = getHorizontalDistance(verticalAngle)
#     print("horizontalDistance: ", horizontalDistance)
