import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import curses
import threading
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

motor1a = 27
motor1b = 22
motor1e = 4

motor2a = 25
motor2b = 24
motor2e = 23

GPIO.setup(motor1a, GPIO.OUT)
GPIO.setup(motor1b, GPIO.OUT)
GPIO.setup(motor1e, GPIO.OUT)
GPIO.setup(motor2a, GPIO.OUT)
GPIO.setup(motor2b, GPIO.OUT)
GPIO.setup(motor2e, GPIO.OUT)

# Set up the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
camera.rotation = 270

rawCapture = PiRGBArray(camera, size=(640, 480))

# Initialize curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(True)
curses.noecho()

# Flag to indicate when to stop the threads
exit_flag = False

def show_frame():
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if exit_flag:
            break
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)

# Create a thread for displaying the camera feed
display_thread = threading.Thread(target=show_frame)
display_thread.start()

try:
    while True:
        char = stdscr.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_UP:
            GPIO.output(motor1a, GPIO.HIGH)
            GPIO.output(motor1b, GPIO.LOW)
            GPIO.output(motor1e, GPIO.HIGH)
            GPIO.output(motor2a, GPIO.LOW)
            GPIO.output(motor2b, GPIO.HIGH)
            GPIO.output(motor2e, GPIO.HIGH)
        elif char == curses.KEY_DOWN:
            GPIO.output(motor1a, GPIO.LOW)
            GPIO.output(motor1b, GPIO.HIGH)
            GPIO.output(motor1e, GPIO.HIGH)
            GPIO.output(motor2a, GPIO.HIGH)
            GPIO.output(motor2b, GPIO.LOW)
            GPIO.output(motor2e, GPIO.HIGH)
        elif char == curses.KEY_LEFT:
            GPIO.output(motor1a, GPIO.HIGH)
            GPIO.output(motor1b, GPIO.LOW)
            GPIO.output(motor1e, GPIO.HIGH)
            GPIO.output(motor2a, GPIO.HIGH)
            GPIO.output(motor2b, GPIO.LOW)
            GPIO.output(motor2e, GPIO.HIGH)
        elif char == curses.KEY_RIGHT:
            GPIO.output(motor1a, GPIO.LOW)
            GPIO.output(motor1b, GPIO.HIGH)
            GPIO.output(motor1e, GPIO.HIGH)
            GPIO.output(motor2a, GPIO.LOW)
            GPIO.output(motor2b, GPIO.HIGH)
            GPIO.output(motor2e, GPIO.HIGH)
        elif char == 10:  # Enter key
            GPIO.output(motor1a, GPIO.LOW)
            GPIO.output(motor1b, GPIO.LOW)
            GPIO.output(motor1e, GPIO.LOW)
            GPIO.output(motor2a, GPIO.LOW)
            GPIO.output(motor2b, GPIO.LOW)
            GPIO.output(motor2e, GPIO.LOW)

finally:
    exit_flag = True
    display_thread.join()
    curses.endwin()
    GPIO.cleanup()
    cv2.destroyAllWindows()
