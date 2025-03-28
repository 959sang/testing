import cv2
import numpy as np
import serial           # get serial communication by pyserial library
import time

ser = serial.Serial('COM11', baudrate=9600, timeout=1)   # serial communication between arduino & python
time.sleep(0.1)         # time delay for waiting serial communication

servoPos1 = 50          # set original position of servo motor 1
servoPos2 = 90          # set original position of servo motor 2

def nothing(x): pass

cv2.namedWindow('Trackbars')        # create window named 'Trackbars'
    # create Trackbars with specified value for red object
cv2.createTrackbar('Hue Low', 'Trackbars', 0, 19, nothing)
cv2.createTrackbar('Hue High', 'Trackbars', 15, 179, nothing)
cv2.createTrackbar('Sat Low', 'Trackbars', 180, 255, nothing)
cv2.createTrackbar('Sat High', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('Val Low', 'Trackbars', 150, 255, nothing)
cv2.createTrackbar('Val High', 'Trackbars', 255, 255, nothing)

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)    # fast open camera to capture video

while True:         # start capturing and showing frames on windows
    success, image = cam.read()
    img = cv2.flip(image, 1)        # 1: flip 'image' around y-axis

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hueLow = cv2.getTrackbarPos('Hue Low', 'Trackbars')
    hueHigh = cv2.getTrackbarPos('Hue High', 'Trackbars')
    satLow = cv2.getTrackbarPos('Sat Low', 'Trackbars')
    satHigh = cv2.getTrackbarPos('Sat High', 'Trackbars')
    valLow = cv2.getTrackbarPos('Val Low', 'Trackbars')
    valHigh = cv2.getTrackbarPos('Val High', 'Trackbars')

        # find specified colour and isolate it by inRange
    FGmask = cv2.inRange(hsv,(hueLow,satLow,valLow), (hueHigh,satHigh,valHigh))
    cv2.imshow('FG mask', FGmask)
    final = cv2.bitwise_and(img, img, mask=FGmask)

        # find contours and draw contours/bounding boxes around them
    contours, hierarchy = cv2.findContours(FGmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        (x, y, w, h) = cv2.boundingRect(cnt)

        if area > 80:       # area of bounding boxes > 80
            cv2.drawContours(img,[cnt],0,(255,0,0),3)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)

            servoPos1_error = -(y + h/2) + 240    # vertical error of colour object from centre of screen
            if abs(servoPos1_error) > 15:         # adjust servo motor-1 (vertical position)
                servoPos1 = float(servoPos1) + servoPos1_error/240
                print('servoPos1 = ', servoPos1)
            if float(servoPos1) > 80:             # limit top position
                servoPos1 = 80
                print("servoPos1 = 80")
            if float(servoPos1) < 40:             # limit bottom position
                servoPos1 = 40
                print("servoPos1 = 40")

            servoPos2_error = (x + w/2) - 320     # horizontal error of colour object from centre of screen
            if abs(servoPos2_error) > 15:         # adjust servo motor-2 (horizontal position)
                servoPos2 = float(servoPos2) + servoPos2_error/320
                print('servoPos2 = ', servoPos2)
            if float(servoPos2) > 120:            # limit right position
                servoPos2 = 120
                print("servoPos2 = 120")
            if float(servoPos2) < 60:             # limit left position
                servoPos2 = 60
                print("servoPos2 = 60")

            servoPos1 = str(servoPos1) + '\r'     # read string until '\r' received to end
            servoPos2 = str(servoPos2) + '\n'     # read string until '\n' received to end
            ser.write(servoPos1.encode())         # convert string to binary and then send converted binary
            ser.write(servoPos2.encode())         # convert string to binary and then send converted binary
            time.sleep(0.08)

    cv2.imshow('Frame', img)              # show frame on window
    cv2.imshow('Final', final)

    """ hints provided by teacher
        w = x2 - x
        errorPan = (x + w / 2) - 640 / 2
        print('errorPan', errorPan)
        if abs(errorPan) > 20:
            pos = pos - errorPan / 200
            # print(type(pos))
        if pos > 170:
            pos = 170
            print("Out of range")
        if pos < 10:
            pos = 10
            print("out of range")
    """

    if cv2.waitKey(1) == 27:
            break

cam.release()
cv2.destroyAllWindows()