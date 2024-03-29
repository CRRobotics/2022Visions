import libjevois as jevois # type: ignore
import cv2
import numpy as np
import functions
import json
from datetime import datetime
import re
## creator
#
# Add some description of your module here.
#
# @author Bradford Smith
# 
# @videomapping YUYV 320 240 30 YUYV 320 240 30 Team639 FullFeater
# @email scarecrow@gmail.com
# @address 123 first street, Los Angeles CA 90012, USA
# @copyright Copyright (C) 2018 by Bradford Smith
# @mainurl 
# @supporturl 
# @otherurl 
# @license 
# @distribution Unrestricted
# @restrictions None
# @ingroup modules
class BetterFullFeatures:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        self.pattern = re.compile('([0-9]*\.[0-9]+|[0-9]+) fps, ([0-9]*\.[0-9]+|[0-9]+)% CPU, ([0-9]*\.[0-9]+|[0-9]+)C,')
        # a simple frame counter used to demonstrate sendSerial():
        self.frame = 0
        self.framerate_fps = "0"
        self.CPULoad_pct = "0"
        self.CPUTemp_C = "0"
        self.pipelineDelay_us = "0"

        self.groundHorizontalAngle = -1
        self.horizontalDistance = -1

        self.redBallAngle = -1
        self.redBallDistance = -1

        self.blueBallAngle = -1
        self.blueBallDistance = -1  
        jevois.sendSerial("Constructor called")
        jevois.LINFO("Constructor logging info")


    # ###################################################################################################
    ## Process function with no USB output
    def processNoUSB(self, inframe):
        self.commonProcess(inframe=inframe)
        
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        self.commonProcess(inframe=inframe, outframe=outframe)
        


    def commonProcess(self, inframe, outframe = None):
        # jevois.LINFO("inframe type is "+str(type(inframe)))
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inframe = inframe.getCvBGR()
        
        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()
        pipline_start_time = datetime.now()
        mask = functions.HSVFilter(inframe)

        # finding and filtering the contours in the inframe to only get the contour of the tape
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = functions.filterContours(contours)

        if len(contours) > 0:

            # getting convex hulls
            convexHulls = [cv2.convexHull(contour) for contour in contours]
            # drawing convexHulls on the inframe to display
            cv2.drawContours(inframe, convexHulls, -1, (0, 0, 255), 1)

            # getting the centers of the contours in the inframe
            centers = functions.getCenters(inframe, convexHulls)
            h, w, c = inframe.shape
            centerPixel = (int(w / 2), int(h / 2))
            inframe = cv2.circle(inframe, centerPixel, 3, (255, 0, 255), -1)
            # STEP 2: DETERMINE THE PARABOLIC FIT WITH LEAST SQUARES USING THE CENTER COORDINATES OF THE TAPE
            vertex = functions.getParabola(inframe, centers) if len(centers) >= 3 else None

             # STEP 3: DETERMINE HORIZONTAL AND VERTICAL ANGLES TO TARGET (FROM THE ROBOT)
            opticalHorizontalAngle = functions.getAngle(inframe, 0, vertex) if vertex is not None else functions.getAngle(inframe, 0, centers[0])
            groundHorizontalAngle = functions.horizontalOpticalToGround(opticalHorizontalAngle)
            opticalVerticalAngle = functions.getAngle(inframe, 1, vertex) if vertex is not None else functions.getAngle(inframe, 1, centers[0])
            groundVerticalAngle = functions.verticalOpticalToGround(opticalHorizontalAngle, opticalVerticalAngle)

            # displaying the horizontal and vertical angles on the frame
            cv2.putText(inframe, "Horizontal Angle: " + str(groundHorizontalAngle) + "  Vertical Angle: " + str(groundVerticalAngle), \
                (inframe.shape[1] - 600, inframe.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # STEP 4: DETERMINE HORIZONTAL DISTANCE TO TARGET (FROM THE ROBOT)
            horizontalDistance = functions.getHorizontalDistance(groundVerticalAngle)

            # displaying the horizontal distance to the target on the frame
            cv2.putText(inframe, "Distance: " + str(horizontalDistance), \
                (inframe.shape[1] - 300, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            self.groundHorizontalAngle = groundHorizontalAngle
            self.horizontalDistance = horizontalDistance
        else:
            self.groundHorizontalAngle = -1
            self.horizontalDistance = -1

        if outframe:
            outframe.sendCv(inframe)

        pipeline_end_time = datetime.now() - pipline_start_time
        self.pipelineDelay_us = pipeline_end_time.microseconds
        results = self.pattern.match(self.timer.stop())
        if(results is not None):
            self.framerate_fps = results.group(1)
            self.CPULoad_pct = results.group(2)
            self.CPUTemp_C = results.group(3)

    
        # Example of sending some serial output message:
        data = "{ %d %.1f %.3f  %.1f %.3f %.1f %.3f %s %s %s 0 }"%(
            self.frame,
            self.groundHorizontalAngle, self.horizontalDistance,
            15.6, 6.78,
            15.6, 6.78,
            self.framerate_fps,self.CPULoad_pct,self.CPUTemp_C,self.pipelineDelay_us
        )
        #data = f"*{self.frame} 1234567890  1234567890"
        jevois.sendSerial(data)
        # Write frames/s info from our timer into the edge map (NOTE: does not account for output conversion time):
        self.frame += 1


    # ###################################################################################################
    ## Parse a serial command forwarded to us by the JeVois Engine, return a string
    def parseSerial(self, str):
        jevois.LINFO("parseserial received command [{}]".format(str))
        if str == "hello":
            return self.hello()
        return "ERR Unsupported command"
    
    # ###################################################################################################
    ## Return a string that describes the custom commands we support, for the JeVois help message
    def supportedCommands(self):
        # use \n seperator if your module supports several commands
        return "hello - print hello using python"

    # ###################################################################################################
    ## Internal method that gets invoked as a custom command
    def hello(self):
        return "Hello from python!"
        
