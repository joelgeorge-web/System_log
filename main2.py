import streamlit as st
import os
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np

# Load your custom model
model_path = "model_weights.h5"
loaded_model = load_model(model_path)

img_width, img_height = 128, 128  # Change to the input size your model expects
batch_size = 1
classes = ['off', 'on']

picture = st.camera_input("Take a picture")

def preprocess_image(img):
    # Preprocess the image based on your model's requirements
    img = img.resize((img_width, img_height))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalize the image
    img_array = tf.expand_dims(img_array, 0)  # Add batch dimension
    return img_array

def save_image(img, folder_path, file_name):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    img.save(os.path.join(folder_path, file_name))

if picture:
    pil_image = Image.open(picture)
    st.image(pil_image, caption="Captured Image", use_column_width=True)
    
    folder_path = "saved_images"
    file_name = "sample.jpg"
    
    save_image(pil_image, folder_path, file_name)
    st.success(f"Image saved successfully as {file_name} in the folder {folder_path}")

    # Preprocess the image for prediction
    img_array = preprocess_image(pil_image)

    # Make predictions
    predictions = loaded_model.predict(img_array)
    print(predictions)
    print(classes[np.argmax(predictions)])
    st.text(f"Predicted Class: {predictions}")
    