import cv2
import numpy as np

import JevoisModule.functions as f

def main():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()

        mask = f.HSVFilter(frame)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = f.filterContours(contours)
        convexHulls = [cv2.convexHull(contour) for contour in contours]
        cv2.drawContours(frame, convexHulls, -1, (0, 0, 255), 1)

        cv2.imshow("Frame", frame)
        cv2.waitKey()

if __name__ == "__main__":
    main()