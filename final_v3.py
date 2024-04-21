import cv2
import numpy as np
import easyocr
import csv
import os
import time
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import streamlit as st

# Load your custom model
model_path = "model_weights.h5"
loaded_model = load_model(model_path)

img_width, img_height = 128, 128  # Change to the input size your model expects
batch_size = 1
classes = ['off', 'on']


cap = cv2.VideoCapture(0)

# Color detection thresholds
lowerRed = np.array([-15, 40, 140])
upperRed = np.array([15, 140, 255])
lowerBlue = np.array([110, 100, 200])
upperBlue = np.array([130, 255, 255])
lowerGreen = np.array([45, 40, 140])
upperGreen = np.array([75, 200, 255])

# Create CSV file if it doesn't exist
if not os.path.isfile('data.csv'):
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["SI No", "Red", "Green", "Blue", "Voltage", "Knob"])

# Initialize serial number for CSV after fnding the last serial number in the data.csv file and adding 1 to it
serial_number = 1  # Initialize the serial number in case the CSV is empty
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        serial_number = int(row[0])  # Update serial_number

# EasyOCR reader
reader = easyocr.Reader(['en'])  

def process_image(image_path):
    global serial_number  # Access global serial number

    img = cv2.imread(image_path)
    img1 = Image.open(image_path)

    # Color Detection
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_red = cv2.inRange(img_hsv, lowerRed, upperRed)
    mask_blue = cv2.inRange(img_hsv, lowerBlue, upperBlue)
    mask_green = cv2.inRange(img_hsv, lowerGreen, upperGreen)

    color_detected = {
        "Red": int(cv2.countNonZero(mask_red) > 500),
        "Green": int(cv2.countNonZero(mask_green) > 500),
        "Blue": int(cv2.countNonZero(mask_blue) > 500)
    }

    # OCR Voltage Reading
    result = reader.readtext(img, allowlist='0123456789')
    result = [item for item in result if item[1].isdigit() and len(item[1]) == 3]
    voltage = None
    for detection in result:
        print(detection[1])
        if detection[1] > str(250):
            voltage = '1' + detection[1][1:]
        elif detection[1] > str(100):
            voltage = detection[1]
            break
        else:

            break

    img_array = preprocess_image(img1)

    # Make predictions
    predictions = loaded_model.predict(img_array)
    Knob = classes[np.argmax(predictions)]
    print(predictions, Knob)



    # Write to CSV 
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([serial_number, color_detected["Red"], color_detected["Green"], color_detected["Blue"], voltage, Knob])

    serial_number += 1

def preprocess_image(img1):
    # Preprocess the image based on your model's requirements

    img1 = img1.resize((img_width, img_height))
    img_array = image.img_to_array(img1)
    img_array = img_array / 255.0  # Normalize the image
    img_array = tf.expand_dims(img_array, 0)  # Add batch dimension
    return img_array



while True:
    ret, frame = cap.read()  # Read a frame from the camera
    print("Frame read successfully.")

    if ret:  # Check if a frame was successfully captured
        cv2.imshow("Live Feed", frame)  # Display the frame

        if cv2.waitKey(2000) & 0xFF == ord('q'):  # Wait for 2 seconds or 'q' key to exit
            break

        cv2.destroyAllWindows()  # Close the display window
        # Save a copy of the image for processing:
        cv2.imwrite("temp_image.jpg", frame)

        process_image("temp_image.jpg")  # Process the saved image
        print("Image processed successfully.")
        os.remove("temp_image.jpg")  # Remove the temporary image
        time.sleep(5)  # Wait 20 seconds
    else:
        print("Error: Could not read frame from camera.")
        break

