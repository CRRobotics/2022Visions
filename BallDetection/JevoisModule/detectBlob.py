import constants
import cv2
import numpy as np

import functions as f

def main():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()

        f.putCenterPixelIn(frame=frame)

        ksize = int(2 * round(constants.BLUR_RADIUS) + 1)
        blur = cv2.blur(frame, (ksize,ksize))
        mask = f.HSVFilterBLUE(blur)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = f.filterContours(contours)
        convexHulls = [cv2.convexHull(contour) for contour in contours]
        cv2.drawContours(frame, convexHulls, -1, (0, 0, 255), 1)
        
        try:
            centers = f.getCenters(frame, convexHulls) ##WILL GET 2 LARGEST CONTOURS
            print(centers)
            if centers:
                verticalAngle = round(f.getAngle(frame, 1, centers[0]),2)
                opticalHorizontalAngle = f.getAngle(frame, 0, centers[0])
                groundHorizontalAngle = round(f.horizontalOpticalToGround(opticalHorizontalAngle), 2)
                horizontalDistance = round(f.getHorizontalDistance(verticalAngle), 2)
                
                finalDistance = f.groundAngleToHypotnuse(groundHorizontalAngle, horizontalDistance)


                cv2.putText(frame, "Horizontal Angle: " + str(groundHorizontalAngle) + "  Vertical Angle: " + str(verticalAngle), \
                    (frame.shape[1] - 310, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)

                # displaying the horizontal distance to the target on the frame
                cv2.putText(frame, "Distance: " + str(finalDistance), \
                    (frame.shape[1] - 300, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        except:
            pass
        


        cv2.imshow("Frame", frame)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()