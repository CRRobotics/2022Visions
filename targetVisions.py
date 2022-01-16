import cv2
import numpy as np
import library.helperFunctions as helperFunctions

# filter = {"hue": [57, 111], "sat":[148, 255], "val": [255, 255]}
# hue = [57, 111]
# sat = [148, 255]
# val = [255, 255]

hue = [0, 180]
sat = [73, 255]
val = [255, 255]

cap = cv2.VideoCapture(0)


def HSVFilter(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]))
    return mask

# runs target tracking
def main():
    while True:
        try:
            # STEP 1: IDENTIFY THE TARGET
            isTrue, frame = cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, (hue[0], sat[0], val[0]), (hue[1], sat[1], val[1]))

            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            contours = helperFunctions.filterContours(contours)

            convexHulls = [cv2.convexHull(contour) for contour in contours]
            
            if convexHulls:
                print("\n\n\n")
                cx = convexHulls[0].tolist()
                coordsOfConvexHulls = [x[0] for x in cx] #[[x1,y1], [x2,y2],[x3,y3],...]
                #im having a stroke trying to get a list of (x,y) coordinates
                c = helperFunctions.get_leftmost_and_rightmost_coords(frame, coordsOfConvexHulls)
                if c:
                    print(helperFunctions.Center(frame, c[0],c[1]))
                #action = functions.Center(frame, c[0], c[1])
                #print(action)


            cv2.drawContours(frame, convexHulls, -1, (0, 0, 255), 1)

            cv2.imshow("mask", mask)
            cv2.imshow("frame", frame)

            if cv2.waitKey(20) & 0xFF == ord("d"):
                print("done")
                break

            # STEP 2: DETERMINE THE PARABOLIC FIT WITH LEAST SQUARES USING THE CENTER COORDINATES OF THE TAPE

            # STEP 3: DETERMINE HORIZONTAL DISTANCE TO TARGET (FROM THE CENTER OF THE FRAME)

            # STEP 4: DETERMINE EITHER DISTANCE OR HORIZONTAL ANGLE TO TARGET (FROM THE ROBOT)?

            # STEP 5: DETERMINE EITHER DISTANCE OR HORIZONTAL ANGEL TO TARGET (FROM THE ROBOT)?

            # STEP 6: DETERMINE VERTICAL/ELEVATION ANGLE TO TARGET (FROM THE ROBOT)

            # STEP 7: DETERMINE HORIZONTAL DISTANCE TO TARGET (FROM THE ROBOT)
        except:
            pass

if __name__ == "__main__":
    main()