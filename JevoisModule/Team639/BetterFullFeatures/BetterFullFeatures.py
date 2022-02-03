import libjevois as jevois # type: ignore
import cv2
import numpy as np
import functions
import json
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
        
        # a simple frame counter used to demonstrate sendSerial():
        self.frame = 0
        
    # ###################################################################################################
    ## Process function with no USB output
    def processNoUSB(self, inframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inimg = inframe.getCvBGR()

        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()
        
        jevois.LINFO("Processing video frame {} now...".format(self.frame))

        # TODO: you should implement some processing.
        # Once you have some results, send serial output messages:

        # Get frames/s info from our timer:
        fps = self.timer.stop()

        # Send a serial output message:
        jevois.sendSerial("DONE frame {} - {}".format(self.frame, fps));
        self.frame += 1
        
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        jevois.LINFO("inframe type is "+str(type(inframe)))
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inframe = inframe.getCvBGR()
        
        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()
    





        # STEP 1: IDENTIFY THE TARGET
        # isTrue, frame = cap.read()
        # cv2.imshow("frame2", frame)
        
        # getting HSV filter to distinguish the target from surroundings
        mask = functions.HSVFilter(inframe)

        # finding and filtering the contours in the inframe to only get the contour of the tape
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = functions.filterContours(contours)

        if len(contours) > 0:

            # getting convex hulls
            convexHulls = [cv2.convexHull(contour) for contour in contours]
            
            # if convexHulls:
            #     print("\n\n\n")
            #     cx = convexHulls[0].tolist()
            #     coordsOfConvexHulls = [x[0] for x in cx] #[[x1,y1], [x2,y2],[x3,y3],...]
            #     #im having a stroke trying to get a list of (x,y) coordinates
            #     c = functions.get_leftmost_and_rightmost_coords(inframe, coordsOfConvexHulls)
            #     if c:
            #         print(functions.Center(inframe, c[0],c[1]))
            #     #action = functions.Center(inframe, c[0], c[1])
            #     #print(action)
            
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
            outframe.sendCv(inframe)

            # Example of sending some serial output message:
            data = {
                "horizontalDistance": horizontalDistance,
                "horizontalAngle": groundHorizontalAngle
            }
            jsonData = json.dumps(data)

            jevois.sendSerial(jsonData)


            
        # displaying the inframe with the convex hull of the tape
        # cv2.imshow("mask", mask)
        # cv2.imshow("inframe", inframe)

        # for testing purposes



        # Detect edges using the Laplacian algorithm from OpenCV:
        #
        # Replace the line below by your own code! See for example
        # - http://docs.opencv.org/trunk/d4/d13/tutorial_py_filtering.html
        # - http://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
        # - http://docs.opencv.org/trunk/d5/d0f/tutorial_py_gradients.html
        # - http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
        #
        # and so on. When they do "img = cv2.imread('name.jpg', 0)" in these tutorials, the last 0 means they want a
        # gray image, so you should use getCvGRAY() above in these cases. When they do not specify a final 0 in imread()
        # then usually they assume color and you should use getCvBGR() above.
        #
        # The simplest you could try is:
        #    outimg = inimg
        # which will make a simple copy of the input image to output.








        #outimg = cv2.Laplacian(inimg, -1, ksize=5, scale=0.25, delta=127)
        
        # Write a title:
        #cv2.putText(outimg, "JeVois FullFeater", (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
        # Write frames/s info from our timer into the edge map (NOTE: does not account for output conversion time):
        else:
            fps = self.timer.stop()
            height = inframe.shape[0]
            width = inframe.shape[1]
            cv2.putText(inframe, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
            # Convert our output image to video output format and send to host over USB:
            outframe.sendCv(inframe)

            # Example of sending some serial output message:
            jevois.sendSerial(f"DONE frame {self.frame}")
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
        
