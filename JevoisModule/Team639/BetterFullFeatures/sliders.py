import cv2
import os
import json
import library.functions as functions

# Grip Filters
FILE_NAME = "filter.json"
CAM_ID = 0

# "exposure": 10
filter = {
          "hue": [70, 94],
          "sat": [128.0, 255.0],
          "val": [228.0, 255.0],
         }


def loadParameters():
    global filter
    try:
        ip = open(FILE_NAME, "r")
        filter = json.load(ip)
    except:
        print("Filter settings file could not be found!")

    # print("COMMAND: ",
    #       'sudo v4l2-ctl -c -d /dev/video' + str(CAM_ID) + ' exposure_auto=1 -c exposure_absolute=' + str(filter["exposure"]))
    # os.system('sudo v4l2-ctl -d /dev/video' + str(CAM_ID) + ' -c exposure_auto=1 -c exposure_absolute=' + str(filter["exposure"]))

def saveParameters(*arg):
    global filter
    hue = filter["hue"]
    sat = filter["sat"]
    val = filter["val"]
    # exposure = filter["exposure"]
    
    # # See if the exposure changed. If so, write it to the camera.
    # if (exposure != cv2.getTrackbarPos("EXPOS", "sliders")):
    #     filter["exposure"] = cv2.getTrackbarPos("EXPOS", "sliders")
    #     print("COMMAND: ", 'sudo v4l2-ctl -d /dev/video' + str(CAM_ID) + ' -c exposure_auto=1 -c exposure_absolute='+str(cv2.getTrackbarPos("EXPOS", "sliders")))
    #     os.system('sudo v4l2-ctl -c exposure_auto=1 -d /dev/video' + str(CAM_ID) + ' -c exposure_absolute='+str(cv2.getTrackbarPos("EXPOS", "sliders")))

    hue[0] = cv2.getTrackbarPos("H_Min", "sliders")
    hue[1] = cv2.getTrackbarPos("H_Max", "sliders")
    sat[0] = cv2.getTrackbarPos("S_Min", "sliders")
    sat[1] = cv2.getTrackbarPos("S_Max", "sliders")
    val[0] = cv2.getTrackbarPos("V_Min", "sliders")
    val[1] = cv2.getTrackbarPos("V_Max", "sliders")
    
    output = open(FILE_NAME, "w")
    json.dump(filter, output)
    output.close()

def startSliders():
    global filter
    hue = filter["hue"]
    sat = filter["sat"]
    val = filter["val"]
    # exposure = filter["exposure"]

    cv2.namedWindow("sliders")
    cv2.createTrackbar("H_Min", "sliders", int(hue[0]), 255, saveParameters)
    cv2.createTrackbar("H_Max", "sliders", int(hue[1]), 255, saveParameters)
    cv2.createTrackbar("S_Min", "sliders", int(sat[0]), 255, saveParameters)
    cv2.createTrackbar("S_Max", "sliders", int(sat[1]), 255, saveParameters)
    cv2.createTrackbar("V_Min", "sliders", int(val[0]), 255, saveParameters)
    cv2.createTrackbar("V_Max", "sliders", int(val[1]), 255, saveParameters)
    # cv2.createTrackbar("EXPOS", "sliders", int(exposure), 500, saveParameters)
    # os.system('sudo v4l2-ctl -d /dev/video' + str(CAM_ID) + ' -c exposure_auto=1 -c exposure_absolute='+str(cv2.getTrackbarPos("EXPOS", "sliders")))


def getFilter():
    return filter


def start(cam_id):
    CAM_ID = cam_id
    loadParameters()
    startSliders()


if __name__ == "__main__":
    start(0)
    cv2.waitKey(0)