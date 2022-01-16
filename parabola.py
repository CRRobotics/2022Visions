import math
import cv2
import numpy as np
import library.helperFunctions as helperFunctions
import targetVisions
import tape

cap = cv2.VideoCapture(1)
while True:
    success, frame = cap.read()
    h, w, c = frame.shape
    mask = targetVisions.HSVFilter(frame)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = helperFunctions.filterSmallContours(contours)
    convexHulls = [cv2.convexHull(contour) for contour in contours]
    cv2.drawContours(frame, convexHulls, -1, (255,0,0), 1)
    centers = tape.reflectiveTape.getCenters(frame, contours)
    #print(centers)
    #print(w)
    if len(centers) >= 3:
        yVals = [x[1] for x in centers]
        xVals = [x[0] for x in centers]

        fit = np.polyfit(xVals, yVals, 2)
        a, b, c = fit

        xVals = np.linspace(1,w-1,100).astype(np.int32)
        #xVals = np.array(xVals)
        #print(xVals)
        fit_equation = a * np.square(xVals) + b * xVals + c 
        #print(f"{a} * {np.square(xVals)} + {b} * {xVals} + c")
        #print(fit_equation)
        newXY = list(zip(xVals, fit_equation))
        ctr = np.array(newXY).reshape((-1,1,2)).astype(np.int32)
        #print(f"\n\n{newXY}")

        cv2.drawContours(frame, [ctr], -1, (255,0,0), 1)


        #for some reason, going up decreases the y value
        vertex = helperFunctions.getVertex(a,b,c)
        #print(vertex)
        
        angle = helperFunctions.getAngle(frame, vertex)
        angle = helperFunctions.angleToRadians(angle)
        print(angle)

        distance = h/math.tan(angle)
        cv2.putText(frame, f"{distance} pixels", (frame.shape[1] - 200, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 3 )
    




    cv2.imshow("img", frame)
    cv2.waitKey(1)
    

