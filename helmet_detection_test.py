import tensorflow as tf
import numpy as np
import cv2
import pygame
import time

# Load the saved .h5 model
model = tf.keras.models.load_model("helmet_detection_model.h5")

# Initialize pygame mixer for playing sound
pygame.mixer.init()
sound = pygame.mixer.Sound("helmet_warning.wav")

# Function to preprocess the input image
def preprocess_image(image):
    image = cv2.resize(image, (224, 224))  # Resize image to 224x224
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = tf.keras.applications.resnet50.preprocess_input(image)  # Preprocess for ResNet50
    return image

# Function to make predictions on the image
def predict_image(image, model):
    preprocessed_image = preprocess_image(image)
    prediction = model.predict(preprocessed_image)
    return np.argmax(prediction, axis=-1)  # Returns 0 for "No Helmet", 1 for "With Helmet"

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
    else:
        print("Helmet Detected.")
    
    time.sleep(1)  # Wait for 1 second before capturing the next image
