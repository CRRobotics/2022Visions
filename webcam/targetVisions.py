import cv2
import os
import sys
import library.constants as constants
import library.functions as functions
# from networktables import NetworkTables
# # from testing.gripTest import GripPipeline


# # set up network tables
# NetworkTables.initialize(server="roborio-639-frc.local")
# sd = NetworkTables.getTable("Visions")

print("imports done")
cap = cv2.VideoCapture(0)
print("we out")

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# runs target tracking
def process():
    while True:
        try:
            # STEP 1: IDENTIFY THE TARGET
            isTrue, frame = cap.read()
            print(type(frame))
            cv2.imshow("frame2", frame)
            
            # getting HSV filter to distinguish the target from surroundings
            mask = functions.HSVFilter(frame)

            # finding and filtering the contours in the frame to only get the contour of the tape
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = functions.filterContours(contours)

            if len(contours) == 0:
                cv2.imshow("frame", frame)
                if cv2.waitKey(20) & 0xFF == ord("d"):
                    print("done")
                    break
                continue

            # getting convex hulls
            convexHulls = [cv2.convexHull(contour) for contour in contours]
            
            # if convexHulls:
            #     print("\n\n\n")
            #     cx = convexHulls[0].tolist()
            #     coordsOfConvexHulls = [x[0] for x in cx] #[[x1,y1], [x2,y2],[x3,y3],...]
            #     #im having a stroke trying to get a list of (x,y) coordinates
            #     c = functions.get_leftmost_and_rightmost_coords(frame, coordsOfConvexHulls)
            #     if c:
            #         print(functions.Center(frame, c[0],c[1]))
            #     #action = functions.Center(frame, c[0], c[1])
            #     #print(action)
            
            # drawing convexHulls on the frame to display
            cv2.drawContours(frame, convexHulls, -1, (0, 0, 255), 1)

            # getting the centers of the contours in the frame
            centers = functions.getCenters(frame, convexHulls)

            # STEP 2: DETERMINE THE PARABOLIC FIT WITH LEAST SQUARES USING THE CENTER COORDINATES OF THE TAPE
            vertex = functions.getParabola(frame, centers) if len(centers) >= 3 else None

            # STEP 3: DETERMINE HORIZONTAL AND VERTICAL ANGLES TO TARGET (FROM THE ROBOT)
            opticalHorizontalAngle = functions.getAngle(frame, 0, vertex) if vertex is not None else functions.getAngle(frame, 0, centers[0])
            groundHorizontalAngle = functions.horizontalOpticalToGround(opticalHorizontalAngle)
            opticalVerticalAngle = functions.getAngle(frame, 1, vertex) if vertex is not None else functions.getAngle(frame, 1, centers[0])
            groundVerticalAngle = functions.verticalOpticalToGround(opticalHorizontalAngle, opticalVerticalAngle)

            # STEP 4: DETERMINE HORIZONTAL DISTANCE TO TARGET (FROM THE ROBOT)
            horizontalDistance = functions.getHorizontalDistance(groundVerticalAngle)

            positionHub = [groundHorizontalAngle, horizontalDistance]

            # STEP 5: WRITING TO THE NETWORK TABLE
            sd.putNumberArray("positionHub", positionHub)

            # displaying the horizontal and vertical angles on the frame
            cv2.putText(frame, "Horizontal Angle: " + str(groundHorizontalAngle) + "  Vertical Angle: " + str(groundVerticalAngle), \
                (frame.shape[1] - 600, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # displaying the horizontal distance to the target on the frame
            cv2.putText(frame, "Distance: " + str(horizontalDistance), \
                (frame.shape[1] - 300, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # displaying the frame with the convex hull of the tape
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


# def process_2():
#     g = GripPipeline()
#     while True:
#         isTrue, frame = cap.read()
#         g.process(frame)
#         cv2.imshow("mask", g.mask_output)
#         cv2.imshow("frame", frame)

#         # for testing purposes
#         if cv2.waitKey(20) & 0xFF == ord("d"):
#             print("done")
#             break


if __name__ == "__main__":
    process()
    # process_2()