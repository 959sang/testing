import cv2
import numpy as np

#cam1 = cv2.VideoCapture(0)                 # slow open camera to capture video
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)    # fast open camera to capture video
while True:
    ret, frame = cam.read()
    cv2.imshow('original', frame)    # show captured frame as original

    frameCanny = cv2.Canny(frame, 100, 100)
    cv2.imshow('Canny', frameCanny)  # show captured frame as canny

    frameGaussianBlur = cv2.GaussianBlur(frame, (0, 0), 3)
    cv2.imshow('Gaussian Blur', frameGaussianBlur)      # show captured frame as GaussianBlur

    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV', frameHSV)      # show captured frame as HSV

    if cv2.waitKey(1) == ord('q'):          # only enter 'q' can quit cam window
        break
cam.release()
cv2.destroyAllWindows()
