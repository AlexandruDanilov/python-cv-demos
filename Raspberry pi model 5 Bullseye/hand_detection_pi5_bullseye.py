# Virtual env required, must have local file access
# python3 -m venv --system-site-packages (env name)
# Must install both opencv and mediapipe
# On bullseye no camera init required
from picamera2 import Picamera2
import cv2
import numpy as np
import mediapipe as mp

cv2.startWindowThread()

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

picam2 = Picamera2()
picam2.sensor_resolution = (205, 154)  # Set the camera resolution
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (820, 616)}))
picam2.start()

while True:
    frame = picam2.capture_array()

    # Convert the frame to RGB for MediaPipe Hands
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # If hands are detected, count fingers and display landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            h, w, _ = frame.shape

            # Count fingers based on the position of the tips, excluding the thumb
            # Will follow with thumb counting logic
            fingers_up = [landmarks[i].y < landmarks[i - 1].y for i in [8, 12, 16, 20]]

            # Display the count at the top corner of the screen
            count = fingers_up.count(True)
            cv2.putText(frame, f"Fingers: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Display green dots at the fingertips
            for i in [8, 12, 16, 20]:
                cx, cy = int(landmarks[i].x * w), int(landmarks[i].y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            # Connect all landmarks with purple lines, excluding specific pairs
            for i in range(1, len(landmarks)):
                if (i-1, i) not in [(8, 9), (12, 13), (16, 17)] and (i, i-1) not in [(8, 9), (12, 13), (15, 17)]:
                    x1, y1 = int(landmarks[i - 1].x * w), int(landmarks[i - 1].y * h)
                    x2, y2 = int(landmarks[i].x * w), int(landmarks[i].y * h)
                    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)

    # Display the frame with hand landmarks
    cv2.imshow("frame", frame)

    # Wait for a key event (cv2.waitKey(1) allows the OpenCV window to update)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release resources
cv2.destroyAllWindows()
picam2.stop()
