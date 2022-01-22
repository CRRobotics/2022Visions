import cv2
import numpy
import math


class Visions2022:

    def __init__(self) -> None:
        self.status = "we out"

    def process(self, inframe, outframe):
        frame = inframe.getCvBGR()

        cv2.putText(frame, self.status, (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),
                     1, cv2.LINE_AA)
        
        outframe.sendCvBGR(frame)

