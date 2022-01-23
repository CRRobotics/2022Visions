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

CAMERA_EXPERIMENTAL_DISTANCE = 92
CAMERA_X = 85
CAMERA_Y = 47
FOV_X = math.atan((CAMERA_X / 2) / CAMERA_EXPERIMENTAL_DISTANCE) * 2
FOV_Y = math.atan((CAMERA_Y / 2) / CAMERA_EXPERIMENTAL_DISTANCE) * 2
# RADIANS_PER_PIXEL_X = FOV_X / 1280
# RADIANS_PER_PIXEL_Y = FOV_Y / 720
RADIANS_PER_PIXEL_X = FOV_X / 640
RADIANS_PER_PIXEL_Y = FOV_Y / 480


# LOGITECH 310

# values for E4
# good values but don't work as well when the tape is directly under very bright light
# use testing/capture.png in grip instead of the webcam video since grip has different exposure for some reason
# hue = [71, 103]
# sat = [138, 255]
# val = [171, 255]

# best values so far
# hue = [73, 103]
# sat = [73, 255]
# val = [228, 255]


# values for cafeteria
hue = [70, 94]
sat = [128, 255]
val = [228, 255]





# LOGITECH C270?
# hue = [86, 122]
# sat = [23, 255]
# val = [255, 255]

# # good values for grip exposure
# hue = [0, 180]
# sat = [73, 255]
# val = [255, 255]