import math 

MIN_AREA_CONTOUR        = 53.0

hue_B = [89, 119]
sat_B = [144, 255]
val_B= [41, 255]

BLUR_RADIUS = 2.7027027027027173

CAMERA_EXPERIMENTAL_DISTANCE = 92
CAMERA_X = 85
CAMERA_Y = 47
FOV_X = math.atan((CAMERA_X / 2) / CAMERA_EXPERIMENTAL_DISTANCE) * 2
FOV_Y = math.atan((CAMERA_Y / 2) / CAMERA_EXPERIMENTAL_DISTANCE) * 2
# RADIANS_PER_PIXEL_X = FOV_X / 1280
# RADIANS_PER_PIXEL_Y = FOV_Y / 720
RADIANS_PER_PIXEL_X = FOV_X / 640
RADIANS_PER_PIXEL_Y = FOV_Y / 480

HEIGHT_OF_CAMERA        = 30
# HEIGHT_OF_TARGET        = 107.0
HEIGHT_OF_TARGET        = 4.5
HEIGHT_TO_TARGET        = HEIGHT_OF_TARGET - HEIGHT_OF_CAMERA
# CAMERA_ANGLE		    = 16.4
CAMERA_ANGLE		    = 10.0