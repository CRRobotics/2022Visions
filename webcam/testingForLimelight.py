import cv2
import os
import sys
import library.constants as constants
import library.functions as functions
from networktables import NetworkTables

print("imports done")
cap = cv2.VideoCapture(0)
print("we out")

while True:
        try:
            # STEP 1: IDENTIFY THE TARGET
            isTrue, frame = cap.read()
            cv2.imshow("frame2", frame)
            
            # getting HSV filter to distinguish the target from surroundings
            # mask1 = functions.HSVFilter(frame).astype("float32")
            # mask2 = functions.binarizeSubt(frame).astype("float32")
            # mask = 255 * (mask1 + mask2)
            # mask = mask.clip(0, 255).astype("uint8")

            # mask = functions.binarizeSubt(frame)

            mask1 = functions.HSVFilter(frame)
            mask2 = functions.binarizeSubt(frame)
            mask = cv2.bitwise_and(mask2, mask2, mask = mask1)
            

            # finding and filtering the contours in the frame to only get the contour of the tape
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = functions.filterContours(contours)

            # if len(contours) == 0:
            #     cv2.imshow("frame", frame)
            #     if cv2.waitKey(20) & 0xFF == ord("d"):
            #         print("done")
            #         break
            #     continue

            # getting convex hulls
            convexHulls = [cv2.convexHull(contour) for contour in contours]
            
            # drawing convexHulls on the frame to display
            cv2.drawContours(frame, convexHulls, -1, (0, 0, 255), 1)

            # # getting the centers of the contours in the frame
            # centers = functions.getCenters(frame, convexHulls)

            # # STEP 2: DETERMINE THE PARABOLIC FIT WITH LEAST SQUARES USING THE CENTER COORDINATES OF THE TAPE
            # vertex = functions.getParabola(frame, centers) if len(centers) >= 3 else None
            
            # displaying the frame with the convex hull of the tape
            cv2.imshow("mask1", mask1)
            cv2.imshow("mask2", mask2)
            cv2.imshow("mask", mask)
            cv2.imshow("frame", frame)

            # for testing purposes
            if cv2.waitKey(20) & 0xFF == ord("d"):
                print("done")
                break

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            # isTrue, frame = cap.read()
            # cv2.imshow("frame", frame)

            # if cv2.waitKey(20) & 0xFF == ord("d"):
            #     print("done")
            #     break
