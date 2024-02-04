from picamera2 import Picamera2
import cv2
import numpy as np

cv2.startWindowThread()

picam2 = Picamera2()
picam2.sensor_resolution = (205, 154)  # Set the camera resolution
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (820, 616)}))
picam2.start()

# Initialize HOG for human detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while True:
    frame = picam2.capture_array()

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect humans in the grayscale frame using HOG
    boxes, _ = hog.detectMultiScale(gray_frame)

    # Draw rectangles around detected humans
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with human detection
    cv2.imshow("frame", frame)

    # Wait for a key event (cv2.waitKey(1) allows the OpenCV window to update)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release resources
cv2.destroyAllWindows()
picam2.stop()
