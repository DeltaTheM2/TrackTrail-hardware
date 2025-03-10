import tensorflow as tf
import numpy as np
import pygame
import time
from picamera2 import Picamera2
import cv2
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, name='helmet')
db = firestore.client()
USER_ID = 'oF0C5dWBXNdZuwg9VF2YmzrmPNy1'

model = tf.keras.models.load_model("helmet_detection_model.h5")
pygame.mixer.init()
sound = pygame.mixer.Sound("no_helmet.mp3")
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())

def preprocess_image(image):
    image = np.array(image, dtype=np.float32, copy=True)
    image.setflags(write=1)
    image = cv2.resize(image, (224, 224))
    image = np.expand_dims(image, axis=0)
    return tf.keras.applications.resnet50.preprocess_input(image)

def predict_image(image):
    preprocessed_image = preprocess_image(image)
    prediction = model.predict(preprocessed_image)
    return np.argmax(prediction, axis=-1)

def capture_image():
    picam2.start()
    time.sleep(1)
    image = picam2.capture_array()
    picam2.stop()
    return image

def play_warning_sound(repeat_times=3):
    for _ in range(repeat_times):
        sound.play()
        time.sleep(5)
        sound.stop()

def main():
    while True:
        image = capture_image()
        helmet_status = predict_image(image)
        
        if helmet_status == 0:
            print("No Helmet Detected!")
            play_warning_sound()
        else:
            print("Helmet Detected.")
            # Set initial trip status to false when helmet is detected
            db.collection('users').document(USER_ID).set({"is_in_trip": False}, merge=True)
            break
        time.sleep(5)

if __name__ == "__main__":
    main()
