#standard picamera
#raspberrypi model 3b running buster

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2

def get_color_threshold(color):
    if color == 'blue':
        return (90, 80, 0), (120, 255, 255)
    elif color == 'green':
        return (35, 80, 0), (85, 255, 255)
    elif color == 'white':
        return (0, 0, 200), (255, 30, 255)
    else:
        raise ValueError('Invalid color')
#hsv colors

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
camera.rotation = 0

rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

color = 'blue'
lower, upper = get_color_threshold(color)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array
    cv2.line(image, (213, 0), (213, 480), (204, 0, 204), 2)
    cv2.line(image, (426, 0), (426, 480), (204, 0, 204), 2)
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # filter out small areas to remove noise
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 51, 51), 2)
            cv2.line(image, (round((x + x + w) / 2), 0), (round((x + x + w) / 2), 480), (0, 153, 51), 2)
            if round((x + x + w) / 2) <= 213:
                print("1")
            if 213 < round((x + x + w) / 2) < 426:
                print("2")
            if round((x + x + w) / 2) >= 426:
                print("3")
            #print relative position

    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break
    elif key == ord("g"):
        color = 'green'
        lower, upper = get_color_threshold(color)
    #example on how to switch filter
    rawCapture.truncate(0)

cv2.destroyAllWindows()
