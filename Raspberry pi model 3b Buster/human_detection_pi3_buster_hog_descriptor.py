#standard picamera
#raspberrypi model 3b running buster

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2
#imports

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
camera.rotation = 270
#set frame resolution and rotation for sideways use

rawCapture = PiRGBArray(camera, size=(640, 480))
#start frame capture

time.sleep(0.1)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
#initialise descriptor

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#use the raw capture as frame to process
    image = frame.array
    cv2.line(image, (263, 0), (263, 480),(204, 0, 204), 2)
    cv2.line(image, (376, 0), (376, 480),(204, 0, 204), 2)
    #draw grid to view direction
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    boxes, weights = hog.detectMultiScale(image, winStride=(8,8) )
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    for (xA, yA, xB, yB) in boxes:
        cv2.rectangle(image, (xA, yA), (xB, yB),(204, 0, 204), 2)
        cv2.line(image, (round((xA+xB)/2), 0), (round((xA+xB)/2), 480),(0, 153, 51), 2)
        #mark target
        if round((xA+xB)/2)<=263:
            print("←")
        if round((xA+xB)/2)>263 and round((xA+xB)/2)<376:
            print("↑")
        if round((xA+xB)/2)>=376:
            print("→")
        #display target relative position
    
    cv2.imshow("Frame", image);
    #display frame
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
       break
