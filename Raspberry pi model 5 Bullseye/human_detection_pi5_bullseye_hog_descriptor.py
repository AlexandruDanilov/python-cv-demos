from picamera2 import Picamera2
import cv2
import numpy as np

cv2.startWindowThread()

picam2 = Picamera2()
picam2.sensor_resolution = (2304, 1296)  # Set the camera resolution
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (2304, 1296)}))
picam2.start()

# Initialize HOG for human detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Set the desired processing resolution
processing_resolution = (picam2.sensor_resolution[0] // 4, picam2.sensor_resolution[1] // 4)

while True:
    frame = picam2.capture_array()

    # Resize the frame by averaging 4x4 blocks of pixels
    resized_frame = cv2.resize(frame, processing_resolution, interpolation=cv2.INTER_AREA)

    # Convert the resized frame to grayscale
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    # Detect humans in the grayscale frame using HOG
    boxes, _ = hog.detectMultiScale(gray_frame)

    # Scale the bounding boxes back to the original frame size
    boxes = [(int(x * 4), int(y * 4), int(w * 4), int(h * 4)) for x, y, w, h in boxes]

    # Draw rectangles around detected humans in the original frame
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
