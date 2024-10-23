# Import necessary libraries
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from lxml import etree

# Define paths to annotation and image directories
annotations_dir = "C:\\Users\\smirz\\OneDrive\\Documents\\Coding Minds\\Jerry Ku\\dataset\\annotations\\"
images_dir = "C:\\Users\\smirz\\OneDrive\\Documents\\Coding Minds\\Jerry Ku\\dataset\\images"

# Define classes
classes = ['With Helmet', 'Without Helmet']

# Parse XML annotations
def parse_annotation(annotation_file):
    tree = etree.parse(annotation_file)
    root = tree.getroot()
    objects = []
    for obj in root.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text), int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text), int(bbox.find('ymax').text)]
        objects.append(obj_struct)
    return objects

# Load images and annotations
def load_data(annotations_dir, images_dir):
    X, y = [], []
    for annotation_file in os.listdir(annotations_dir):
        if annotation_file.endswith('.xml'):
            annotation_path = os.path.join(annotations_dir, annotation_file)
            objects = parse_annotation(annotation_path)
            image_path = os.path.join(images_dir, annotation_file.replace('.xml', '.png'))
            image = load_img(image_path, target_size=(224, 224))
            image = img_to_array(image)
            X.append(preprocess_input(image))
            labels = [0] * len(classes)
            for obj in objects:
                label_idx = classes.index(obj['name'])
                labels[label_idx] = 1
            y.append(labels)
    return np.array(X), np.array(y)

# Load and preprocess data
X_train, y_train = load_data(annotations_dir, images_dir)

# Define Faster R-CNN model
def create_faster_rcnn():
    base_model = ResNet50(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    for layer in base_model.layers:
        layer.trainable = False
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(128, activation='relu')(x)
    output = layers.Dense(len(classes), activation='sigmoid')(x)
    model = models.Model(inputs=base_model.input, outputs=output)
    return model

# Compile model
model = create_faster_rcnn()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=25, batch_size=32, validation_split=0.2)

model.save("C:\\Users\\smirz\\OneDrive\\Documents\\Coding Minds\\Jerry Ku\\helmet_detection_model.h5")

# Load the saved model
loaded_model = tf.keras.models.load_model("C:\\Users\\smirz\\OneDrive\\Documents\\Coding Minds\\Jerry Ku\\helmet_detection_model.h5")

# Function to preprocess the input image
def preprocess_image(image_path):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = tf.keras.applications.resnet50.preprocess_input(image)
    return image

# Function to make predictions on images
def predict_image(image_path, model):
    preprocessed_image = preprocess_image(image_path)
    prediction = model.predict(preprocessed_image)
    return prediction

# Path to test images
test_images_dir = "C:\\Users\\smirz\\OneDrive\\Documents\\Coding Minds\\Jerry Ku\\dataset\\images\\"

# Choose some images to test
image_filenames = [
    "BikesHelmets0.png",
    "BikesHelmets100.png",
    "BikesHelmets105.png",
    # Add more image filenames as needed
]

# Make predictions on test images
for image_filename in image_filenames:
    image_path = os.path.join(test_images_dir, image_filename)
    prediction = predict_image(image_path, loaded_model)
    print("Prediction for", image_filename, ":", prediction)