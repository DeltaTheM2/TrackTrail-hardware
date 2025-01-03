import tensorflow as tf
import numpy as np
import pygame
import time
from picamera2 import Picamera2
import cv2
# Load the saved .h5 model
model = tf.keras.models.load_model("helmet_detection_model.h5")

# Initialize pygame mixer for playing sound
pygame.mixer.init()
sound = pygame.mixer.Sound("no_helmet.mp3")
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())

# Function to preprocess the input image
def preprocess_image(image):
    # Convert the image to a writable NumPy array with dtype float32
    image = np.array(image, dtype=np.float32, copy=True)

    # Ensure the array is writable
    image.setflags(write=1)

    # Print image flags to verify
    print("Image flags after conversion:")
    print(image.flags)

    # Resize the image to 224x224 using OpenCV
    image = cv2.resize(image, (224, 224))

    # Expand dimensions to match the model's input shape
    image = np.expand_dims(image, axis=0)

    # Preprocess the image using ResNet50's preprocess_input function
    image = tf.keras.applications.resnet50.preprocess_input(image)

    return image

# Function to make predictions on the image
def predict_image(image, model):
    preprocessed_image = preprocess_image(image)
    prediction = model.predict(preprocessed_image)
    return np.argmax(prediction, axis=-1)  # Returns 0 for "No Helmet", 1 for "With Helmet"

# Capture an image using the PiCamera2
def capture_image():
    picam2.start()
    time.sleep(1)  # Give the camera time to adjust before capturing the image
    image = picam2.capture_array()
    picam2.stop()
    time.sleep(1)
    # Return the captured image
    return image

# Function to play a warning sound if no helmet is detected
def play_warning_sound(repeat_times=3):
    for _ in range(repeat_times):
        sound.play()
        time.sleep(5)  # Play the sound for 2 seconds
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
        break
    time.sleep(5)  # Wait for 1 second before capturing the next image
