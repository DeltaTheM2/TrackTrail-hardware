import torch
from torchvision import transforms
from PIL import Image
import cv2
import pygame
import time

# Load the saved .pt model
model = torch.load("helmet_detection_model.pt")
model.eval()  # Set the model to evaluation mode

# Initialize pygame mixer for playing sound
pygame.mixer.init()
sound = pygame.mixer.Sound("helmet_warning.wav")

# Function to preprocess the input image for PyTorch
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.ToPILImage(),  # Convert OpenCV image (NumPy array) to PIL Image
        transforms.Resize((224, 224)),  # Resize to 224x224
        transforms.ToTensor(),  # Convert PIL Image to PyTorch tensor
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize for ResNet50
    ])
    return transform(image).unsqueeze(0)  # Add batch dimension

# Function to make predictions on the image
def predict_image(image, model):
    preprocessed_image = preprocess_image(image)
    with torch.no_grad():  # No need for gradients during inference
        outputs = model(preprocessed_image)
        _, predicted = torch.max(outputs, 1)  # Get the index of the class with the highest probability
    return predicted.item()  # Returns 0 for "No Helmet", 1 for "With Helmet"

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
