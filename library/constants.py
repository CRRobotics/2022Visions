import math

# CONSTANTS
# these are random numbers for now, will change later
WIDTH                   = 5.0
HEIGHT                  = 480.0
HEIGHT_OF_CAMERA        = 38.5
HEIGHT_OF_TARGET        = 102.25 #8 * 12 + 2.25
HEIGHT_TO_TARGET        = HEIGHT_OF_TARGET - HEIGHT_OF_CAMERA
CAMERA_ANGLE		    = 16.4
OUTER_TARGET_WIDTH      = 39.25
INNER_TARGET_DEPTH      = 29.25
BALL_RADIUS             = 3.5
MIN_AREA_CONTOUR        = 50.0

CAMERA_EXPERIMENTAL_DISTANCE = 92
CAMERA_X = 85
CAMERA_Y = 47
FOV_X = math.atan((CAMERA_X / 2) / CAMERA_EXPERIMENTAL_DISTANCE) * 2
FOV_Y = math.atan((CAMERA_Y / 2) / CAMERA_EXPERIMENTAL_DISTANCE) * 2

hue = [0, 180]
sat = [73, 255]
val = [255, 255]

# filter = {"hue": [57, 111], "sat":[148, 255], "val": [255, 255]}
# hue = [57, 111]
# sat = [148, 255]
# val = [255, 255]