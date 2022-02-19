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
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()


        ksize = int(2 * round(constants.BLUR_RADIUS) + 1)
        blur = cv2.blur(frame, (ksize,ksize))

        """BLUE FILTER"""
        mask = f.HSVFilterBLUE(blur)
        contoursB, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contoursB:
            try:
                contoursB = f.filterContours(contoursB)
                convexHullsB = [cv2.convexHull(contour) for contour in contoursB]
                cv2.drawContours(frame, convexHullsB, -1, (0, 255, 0), 1)
            except:
                pass
        try:
            if contoursB:
                centersB = f.getCenters(frame, convexHullsB) ##WILL GET 2 LARGEST CONTOURS
            if centersB:
                opticalHorizontalAngleB = f.getAngle(frame, 0, centersB[0]) if centersB[0] is not None else f.getAngle(frame, 0, centersB[0])
                opticalVerticalAngleB = f.getAngle(frame, 1, centersB[0]) if centersB[0] is not None else f.getAngle(frame, 1, centersB[0])
                
                opticalHorizontalAngleB = f.angleToRadians(opticalHorizontalAngleB)
                opticalVerticalAngleB = f.angleToRadians(opticalVerticalAngleB)
                
                groundHorizontalAngleB = f.getGroundHorizontalAngle(opticalVerticalAngleB, opticalHorizontalAngleB)

                horizontalDistanceB = f.getDistance(opticalVerticalAngleB, opticalHorizontalAngleB)
                groundHorizontalAngleB = round(f.angleToDegrees(groundHorizontalAngleB), 2)
                horizontalDistanceB = abs(round(horizontalDistanceB, 2))

                "draws blue ball data onto frame"
                cv2.putText(frame, "Horizontal Angle: %.2f"%(groundHorizontalAngleB), \
                    (frame.shape[1] - 200, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 0, 0), 2)
                cv2.putText(frame, "Distance: %.3f"%(horizontalDistanceB), \
                    (frame.shape[1] - 300, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        except:
            print(traceback.format_exc())

        "RED FILTER"
        maskR = f.HSVFilterRED(blur)
        contoursR, hierarchy = cv2.findContours(maskR, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contoursR:
            try:
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

                horizontalDistanceR = f.getDistance(opticalVerticalAngleR, opticalHorizontalAngleR)
                groundHorizontalAngleR = round(f.angleToDegrees(groundHorizontalAngleR), 2)
                horizontalDistanceR = abs(round(horizontalDistanceR, 2))


                "draws red ball data onto frame"
                cv2.putText(frame, "Horizontal Angle: %.2f"%(groundHorizontalAngleR), \
                    (10, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)
                cv2.putText(frame, "Distance: %.3f"%(horizontalDistanceR), \
                    (frame.shape[1] - 600, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        except:
            print(traceback.format_exc())
        f.putCenterPixelIn(frame=frame)

        cv2.imshow("Frame", frame)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()