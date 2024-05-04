import cv2  
import time
import pygame

# Load Haar cascade classifiers for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to detect eyes in a region of interest (ROI)
def detect_eyes(roi_gray):
    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=6, minSize=(30, 30))
    return eyes

# Function to start the alarm
def start_alarm():
    pygame.mixer.init()  # Initialize the pygame mixer module
    pygame.mixer.music.load("alarm.mp3")  # Load the alarm sound file
    pygame.mixer.music.play(-1)  # Play the alarm sound in a loop (-1 means loop)
    print("Alarm started")  # Print a message indicating the alarm started

# Function to stop the alarm
def stop_alarm():
    pygame.mixer.music.stop()  # Stop the alarm sound
    print("Alarm stopped")  # Print a message indicating the alarm stopped

# Start video capture from default camera (0)
cap = cv2.VideoCapture(0)

# Initialize Pygame mixer for sound
pygame.mixer.init()

# Variable to track the start time of eye closure
start_time = None

# Flag to indicate if the alarm is currently playing
alarm_on = False

# Main loop to capture and process video frames
while True:
    # Read a frame from the video capture
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale for face and eye detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Extract the region of interest (ROI) containing the face
        roi_gray = gray[y:y+h, x:x+w]

        # Detect eyes in the ROI
        eyes = detect_eyes(roi_gray)

        # Check if eyes are closed
        if len(eyes) == 0:
            if start_time is None:
                start_time = time.time()  # Start the timer if it's not already started
            else:
                elapsed_time = time.time() - start_time  # Calculate elapsed time
                if elapsed_time >= 3 and not alarm_on:  # Start alarm after 3 seconds of eyes closed
                    start_alarm()  # Start the alarm if it's not already playing
                    alarm_on = True
        else:
            start_time = None  # Reset the timer if eyes are open
            if alarm_on:
                stop_alarm()  # Stop the alarm if it's playing
                alarm_on = False

        # Draw rectangles around detected eyes
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Drowsiness Detection', frame)
    cv2.waitKey(1)  # Add a small delay (1 millisecond)

    # Check for key press and exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
