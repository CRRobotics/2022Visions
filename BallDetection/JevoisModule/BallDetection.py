import libjevois as jevois # type: ignore
import cv2
import numpy as np
from datetime import datetime
import re
import functions as f
import constants
import traceback
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
class BallDetection:
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
        self.redBallAngle = -1
        self.redBallDistance = -1

        self.blueBallAngle = -1
        self.blueBallDistance = -1  
        jevois.sendSerial("Constructor called")
        jevois.LINFO("Constructor  logging info")


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
        frame = inframe.getCvBGR()
        
        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()
        pipline_start_time = datetime.now()






        blur = f.blur(frame)
        """BLUE FILTER"""
        mask = f.HSVFilterBLUE(blur)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            try:
                contours = f.circleFilter(contours)
                contours = f.filterContours(contours)
                convexHulls = [cv2.convexHull(contour) for contour in contours]
                cv2.drawContours(frame, convexHulls, -1, (0, 255, 0), 1)
            except:
                pass
        try:
            centersB = f.getCenters(frame, convexHulls) ##WILL GET 2 LARGEST CONTOURS
            if centersB:
                opticalHorizontalAngleB = f.getAngle(frame, 0, centersB[0]) if centersB[0] is not None else f.getAngle(frame, 0, centersB[0])
                opticalVerticalAngleB = f.getAngle(frame, 1, centersB[0]) if centersB[0] is not None else f.getAngle(frame, 1, centersB[0])
                
                opticalHorizontalAngleB = f.angleToRadians(opticalHorizontalAngleB)
                opticalVerticalAngleB = f.angleToRadians(opticalVerticalAngleB)
                
                groundHorizontalAngleB = f.getGroundHorizontalAngle(opticalVerticalAngleB, opticalHorizontalAngleB)


                horizontalDistanceB = abs(f.getDistance(opticalVerticalAngleB, opticalHorizontalAngleB))

                horizontalDistanceB = round(f.getCorrection(horizontalDistanceB), 2)
                bothorizontalDistanceB = abs(round(f.getCorrection((f.getDistanceRelativeToBot(horizontalDistanceB, groundHorizontalAngleB)), constants.ERROR_SLOPE_POST_TRANSLATION, constants.ERROR_INTERCEPT_POST_TRANSLATION), 2))

                centerOfRotationAngleB = round(f.angleToDegrees(f.getAngleRelativeToCenterOfRotation(horizontalDistanceB, groundHorizontalAngleB)),2)

                self.blueBallAngle = centerOfRotationAngleB
                self.blueBallDistance = bothorizontalDistanceB


                "draws blue ball data onto frame"
                cv2.putText(frame, "Horizontal Angle: %.2f"%(centerOfRotationAngleB), \
                    (frame.shape[1] - 300, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 0, 0), 2)
                cv2.putText(frame, "Distance (bot): %.3f"%(bothorizontalDistanceB), \
                    (frame.shape[1] - 300, 20), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 0, 0), 2)
        except:
            print(traceback.format_exc())


        maskR = f.HSVFilterRED(blur)
        contoursR, hierarchy = cv2.findContours(maskR, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contoursR:
            try:
                contoursR = f.circleFilter(contoursR)
                contoursR = f.filterContours(contoursR)
                convexHullsR = [cv2.convexHull(contour) for contour in contoursR]
                cv2.drawContours(frame, convexHullsR, -1, (0, 255, 0), 1)
            except:
                print("failed")
        try:
            centersR = f.getCenters(frame, convexHullsR) ##WILL GET 2 LARGEST CONTOURS
            if centersR:
                opticalHorizontalAngleR = f.getAngle(frame, 0, centersR[0]) if centersR[0] is not None else f.getAngle(frame, 0, centersR[0])
                opticalVerticalAngleR = f.getAngle(frame, 1, centersR[0]) if centersR[0] is not None else f.getAngle(frame, 1, centersR[0])

                opticalHorizontalAngleR = f.angleToRadians(opticalHorizontalAngleR)
                opticalVerticalAngleR = f.angleToRadians(opticalVerticalAngleR)

                groundHorizontalAngleR = f.getGroundHorizontalAngle(opticalVerticalAngleR, opticalHorizontalAngleR)

                # STEP 4: DETERMINE HORIZONTAL DISTANCE TO TARGET (FROM THE ROROT)

                horizontalDistanceR = abs(f.getDistance(opticalVerticalAngleR, opticalHorizontalAngleR))
                horizontalDistanceR = round(f.getCorrection(horizontalDistanceR), 2)

                bothorizontalDistanceR = round(f.getDistanceRelativeToBot(horizontalDistanceR, groundHorizontalAngleR), 2)
                bothorizontalDistanceR = abs(round(f.getCorrection((f.getDistanceRelativeToBot(horizontalDistanceR, groundHorizontalAngleR)), constants.ERROR_SLOPE_POST_TRANSLATION, constants.ERROR_INTERCEPT_POST_TRANSLATION), 2))

                centerOfRotationAngleR = round(f.angleToDegrees(f.getAngleRelativeToCenterOfRotation(horizontalDistanceR, groundHorizontalAngleR)),2)

                self.redBallAngle = centerOfRotationAngleR
                self.redBallDistance = bothorizontalDistanceR

                "draws red ball data onto frame"
                cv2.putText(frame, "Horizontal Angle: %.2f"%(centerOfRotationAngleR), \
                    (10, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)
                cv2.putText(frame, "Distance: %.3f"%(bothorizontalDistanceR), \
                    (frame.shape[1] - 600, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        except:
            print(traceback.format_exc())
        f.putCenterPixelIn(frame=frame)





        if outframe:
            outframe.sendCv(frame)



        pipeline_end_time = datetime.now() - pipline_start_time
        self.pipelineDelay_us = pipeline_end_time.microseconds
        results = self.pattern.match(self.timer.stop())
        if(results is not None):
            self.framerate_fps = results.group(1)
            self.CPULoad_pct = results.group(2)
            self.CPUTemp_C = results.group(3)

        # Example of sending some serial output message:
        data = "{ %d %.2f %.3f  %.2f %.3f %s %s %s %s }"%(
            self.frame,
            self.blueBallAngle, self.blueBallDistance,
            self.redBallAngle, self.redBallDistance,
            self.framerate_fps,self.CPULoad_pct,self.CPUTemp_C,self.pipelineDelay_us
        )
        jevois.sendSerial(data)

        self.frame += 1
        self.frame %= 999
        self.redBallAngle = -1
        self.redBallDistance = -1
        self.blueBallAngle = -1
        self.blueBallDistance = -1  


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
        
