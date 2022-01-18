import cv2
import numpy as np
import library.constants as constants
import library.functions as functions

cap = cv2.VideoCapture(0)

# runs target tracking
def main():
    while True:
        try:
            # STEP 1: IDENTIFY THE TARGET
            isTrue, frame = cap.read()

            # getting HSV filter to distinguish the target from surroundings
            mask = functions.HSVFilter(frame)

            # finding and filtering the contours in the frame to only get the contour of the tape
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = functions.filterContours(contours)

            # getting convex hulls
            convexHulls = [cv2.convexHull(contour) for contour in contours]
            
            if convexHulls:
                print("\n\n\n")
                cx = convexHulls[0].tolist()
                coordsOfConvexHulls = [x[0] for x in cx] #[[x1,y1], [x2,y2],[x3,y3],...]
                #im having a stroke trying to get a list of (x,y) coordinates
                c = functions.get_leftmost_and_rightmost_coords(frame, coordsOfConvexHulls)
                if c:
                    print(functions.Center(frame, c[0],c[1]))
                #action = functions.Center(frame, c[0], c[1])
                #print(action)
            
            # drawing contours on the frame to display
            cv2.drawContours(frame, convexHulls, -1, (0, 0, 255), 1)

            # displaying the frame with the convex hull of the tape
            cv2.imshow("mask", mask)
            cv2.imshow("frame", frame)

            # for testing purposes
            if cv2.waitKey(20) & 0xFF == ord("d"):
                print("done")
                break

            # STEP 2: DETERMINE THE PARABOLIC FIT WITH LEAST SQUARES USING THE CENTER COORDINATES OF THE TAPE

            # STEP 3: DETERMINE HORIZONTAL DISTANCE TO TARGET (FROM THE CENTER OF THE FRAME)

            # STEP 4: DETERMINE EITHER DISTANCE OR HORIZONTAL ANGLE TO TARGET? (FROM THE ROBOT)

            # STEP 5: DETERMINE EITHER DISTANCE OR HORIZONTAL ANGEL TO TARGET? (FROM THE ROBOT)

            # STEP 6: DETERMINE VERTICAL/ELEVATION ANGLE TO TARGET (FROM THE ROBOT)

            # STEP 7: DETERMINE HORIZONTAL DISTANCE TO TARGET (FROM THE ROBOT)
        except:
            pass

if __name__ == "__main__":
    main()