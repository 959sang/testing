import cv2
import numpy as np
import serial           # get serial communication by pyserial library
import time

ser = serial.Serial('COM10', baudrate=9600)   # serial communication between arduino & python
time.sleep(0.1)                                    # time delay for waiting serial communication

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)    # fast open camera to capture video

while True:
    success, img = cam.read()   # read image via camera

    while ser.inWaiting() == 0:
        pass
    potentiometer = ser.readline()
    potentiometer = str(potentiometer, 'utf-8')
    potentiometer = potentiometer.strip('\r\n')
    print(potentiometer)

    a = 'potentiometer simulated value = ' + potentiometer
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.putText(img, a, (10, 50), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow('img', img)

    if cv2.waitKey(1) == 27:
            break

cam.release()
cv2.destroyAllWindows()