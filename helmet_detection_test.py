from ultralytics import YOLO
import cv2
import pygame
import time

# Load the YOLO model
model = YOLO("helmet_detection_model.pt")

# Initialize pygame mixer for playing sound
pygame.mixer.init()
sound = pygame.mixer.Sound("helmet_warning.wav")

# Function to preprocess the input image
def preprocess_image(image):
    return cv2.resize(image, (640, 640))  # Resize image to YOLO's default input size

# Function to make predictions on the image
def predict_image(image, model):
    # Preprocess the image
    image = preprocess_image(image)
    
    # Run inference using YOLO
    results = model.predict(source=image, save=False, save_txt=False)
    
    # Extract predictions
    for result in results:
        # Assuming class 0 is "No Helmet" and class 1 is "With Helmet"
        if result.boxes.cls == 0:  # Replace with actual class IDs for your model
            return 0  # No Helmet
        elif result.boxes.cls == 1:
            return 1  # With Helmet
    return -1  # Default if no detection is made

# Capture an image from the camera
def capture_image():
    cap = cv2.VideoCapture(0)  # Change the index if you're using an external camera
    ret, frame = cap.read()
    cap.release()

    if ret:
        return frame
    else:
        raise Exception("Failed to capture image.")

# Function to play a warning sound if no helmet is detected
def play_warning_sound(repeat_times=3):
    for _ in range(repeat_times):
        sound.play()
        time.sleep(2)  # Play the sound for 2 seconds
        sound.stop()  # Stop the sound after playing

# Main loop to capture image and check for helmet
while True:
    # Capture the image from the camera
    image = capture_image()

    # Run inference to check if helmet is detected
    helmet_status = predict_image(image, model)

    if helmet_status == 0:  # No helmet detected
        print("No Helmet Detected!")
        play_warning_sound(repeat_times=3)
    elif helmet_status == 1:  # Helmet detected
        print("Helmet Detected.")
    else:
        print("No detection made.")
    
    time.sleep(1)  # Wait for 1 second before capturing the next image
