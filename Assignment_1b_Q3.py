import cv2
import numpy as np

#cam1 = cv2.VideoCapture(0)                 # slow open camera to capture video
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)    # fast open camera to capture video
while True:
    ret, frame = cam.read()
    cv2.imshow('original', frame)   # show captured frame as original

    frame1 = cv2.flip(frame, -1)            # -1: flip original around both axes
    cv2.imshow('right bottom', frame1)

    frame2 = cv2.flip(frame, 1)     # 1: flip original around y-axis
    cv2.imshow('right top', frame2)

    frame3 = cv2.flip(frame, 0)     # 0: flip original around x-axis
    cv2.imshow('left bottom', frame3)

    h_top = np.concatenate((frame, frame2), axis=1)    # merge top 2 frames horizontally
    h_bottom = np.concatenate((frame3, frame1), axis=1)  # merge bottom 2 frames horizontally
    vertical = np.concatenate((h_top, h_bottom), axis=0) # merge frames vertically

    cv2.imshow('horizontal top', h_top)
    cv2.imshow('horizontal bottom', h_bottom)
    cv2.imshow('final display', vertical)

    if cv2.waitKey(1) == ord('q'):          # only enter 'q' can quit cam window
        break
cam.release()
cv2.destroyAllWindows()
