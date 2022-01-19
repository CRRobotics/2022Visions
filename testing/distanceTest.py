import testing.findFocalLength as findFocalLength
import cv2 as cv
import numpy as np
import imutils

cap = cv.VideoCapture(1)

if not cap.isOpened():
    print("error")
    quit()

while True:
    isTrue, frame = cap.read()
    if isTrue:
        #frame = targetVisions.HSVFilter(frame)
        try:
            marker = findFocalLength.findMarker(frame)
        except:
            pass
        # focalLength = 1502.5880859375
        focalLength = 800
        inches = findFocalLength.getDistance(focalLength, findFocalLength.WIDTH, marker[1][0])
        box = cv.cv.BoxPoints(marker) if imutils.is_cv2() else cv.boxPoints(marker)
        box = np.int0(box)



        cv.drawContours(frame, [box], -1, (0, 255, 0), 2)
        cv.putText(frame, "%.2fin" % inches, (frame.shape[1] - 275, frame.shape[0] - 20), cv.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
        cv.imshow("frame", frame)
        if cv.waitKey(20) & 0xFF == ord("d"):
            print("done")
            break
    else:
        print("done")
        break