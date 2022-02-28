import traceback
import constants
import cv2
import numpy as np
import math
import functions as f
import constants
"run this with a webcam to test lol"
# ((((((%(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((#(((((((((((((
# (((((((%((((((((((((((((((((((((((((((((((@@@@*,/@@@@(((((((((((((%(((((((((((((
# (((((((%(((((((((((((((((((@@/.@@,.,,@&,.,.,.,.,.,.,.,.,@@(((((((((%((((((((((((
# ((((((((%(%((((((((((((@@,.,@,@,.,@,.,,,.,,,.,,,.,,,.,,,.,,@((((((((%(#(((((((((
# (((((((((#(((((((((((@,......@@@@...................,,,,,,..,@(((((((%((((((((((
# (((((((((%((((((((((@,,,.,,,.,,,.,,,.,,,.,,,.,,,,,,,,,,,,,,,,,@((((((##(((((((((
# ((((((((((%(#(((((((@@@@.,.,.,.,.,.,.,.,.,.,,,,,,,,,,,,,,,,,,,,@((((((%(((((((((
# ((((((((((%((((((&*.**@..,,,,,,,.,,,.,,,.,,,,,,,,,,,,,,,,,,,,,,@(((((((&@@@&&&&&
# (((((((((((%((((((((((@@,,,,,,........,,,,,,,,,,,,,,,,,,,,,,,,,@&&&&&&&&&&&@@@@%
# ((((((((((((%(((((((((((@@,,,,,,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,@@@@@%%%%%&&. ..&
# ((((((((((((%(((((((((((((@*,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,@&#&%%%%%%%&&&&%%%
# (((((((((((((%(%(((((((((((@@,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,@,.,&&%%%%@@@@*/*///
# (((((((((((((##(@@@@&&&&&&&&&&@,,,,,,,,,,,,,,,,,,,,#@@,,,,@@@@@***/*/***/(((((((
# (((((@@@@&&&&&&&&&&@@@@@#%%%%%%@,,,,,,,,,,,,@@@@@@@,,,,,@/*//(((((((((//////////
# &&&&&&&&@@@@@%%%%%%%#. ... &%%%%@,,,,,,,@**//*/(((@@@@#####((/*/*/*/*/*/*/((((((
# @@%%%%%&/....&%%%%%%%%%%%%@@@@*/@*,,,,,@########((((((((((//**(((((((((((((/*/*/
def main():
    cap = cv2.VideoCapture(r"C:\Users\trexx\Documents\CodeRed\2022Visions\BallDetection\cargoDetect.mp4")

    while cap.isOpened():
        success, frame = cap.read()

        blur = f.blur(frame)
        """BLUE FILTER"""
        mask = f.HSVFilterBLUE(blur)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            try:
                contours = f.circleFilter(contours)
                contours = f.filterContours(contours)
                convexHulls = [cv2.convexHull(contour) for contour in contours]
                cv2.drawContours(frame, convexHulls, -1, (255, 255, 0), 1)
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



                "draws blue ball data onto frame"
                cv2.putText(frame, "Horizontal Angle: %.2f"%(centerOfRotationAngleB), \
                    (frame.shape[1] - 300, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 0, 0), 2)
                cv2.putText(frame, "Distance (bot): %.3f"%(bothorizontalDistanceB), \
                    (frame.shape[1] - 300, 20), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 0, 0), 2)
                cv2.putText(frame, "groundHorizontal (radians): %.3f"%(groundHorizontalAngleB), \
                    (frame.shape[1] - 500, 40), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 0, 0), 2)
        except:
            print(traceback.format_exc())

        maskR = f.HSVFilterRED(blur)
        contoursR, hierarchy = cv2.findContours(maskR, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contoursR:
            try:
                contoursR = f.circleFilter(contoursR)

                contoursR = f.filterContours(contoursR)
                convexHullsR = [cv2.convexHull(contour) for contour in contoursR]
                cv2.drawContours(frame, convexHullsR, -1, (0, 255, 255), 1)
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

                "draws red ball data onto frame"
                cv2.putText(frame, "Horizontal Angle: %.2f"%(centerOfRotationAngleR), \
                    (10, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)
                cv2.putText(frame, "Distance: %.3f"%(bothorizontalDistanceR), \
                    (frame.shape[1] - 600, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        except:
            print(traceback.format_exc())
        f.putCenterPixelIn(frame=frame)

        cv2.imshow("Frame", frame)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()