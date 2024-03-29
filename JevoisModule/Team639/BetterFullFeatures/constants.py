import math

# CONSTANTS
# these are random numbers for now, will change later

# HEIGHT_OF_CAMERA        = 38.5
HEIGHT_OF_CAMERA        = 29.5
# HEIGHT_OF_TARGET        = 107.0
HEIGHT_OF_TARGET        = 66.0
HEIGHT_TO_TARGET        = HEIGHT_OF_TARGET - HEIGHT_OF_CAMERA
# CAMERA_ANGLE		    = 16.4
CAMERA_ANGLE		    = 10.0

# THIS VALUE HAS BEEN DETERMINED BY CLOSE-TESTING, CAHNGE THESE VALUES LATER
MIN_AREA_CONTOUR        = 50.0

CAMERA_EXPERIMENTAL_DISTANCE = 74.75
CAMERA_X = 70.875
CAMERA_Y = 47
FOV_X = math.atan((CAMERA_X / 2) / CAMERA_EXPERIMENTAL_DISTANCE) * 2
FOV_Y = math.atan((CAMERA_Y / 2) / CAMERA_EXPERIMENTAL_DISTANCE) * 2
# RADIANS_PER_PIXEL_X = FOV_X / 1280
# RADIANS_PER_PIXEL_Y = FOV_Y / 720
RADIANS_PER_PIXEL_X = FOV_X / 640
RADIANS_PER_PIXEL_Y = FOV_Y / 480