import libjevois as jevois # type: ignore
import cv2
import numpy as np
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
        data = "{ %d }"%(
            self.frame
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
        
