import cv2
import numpy as np
import easyocr
import csv
import os

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
        writer.writerow(["SI No", "Red", "Green", "Blue", "Voltage"])

# Initialize serial number for CSV
serial_number = 1

# EasyOCR reader
reader = easyocr.Reader(['en'])  

def process_image(image_path):
    global serial_number  # Access global serial number

    img = cv2.imread(image_path)

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
    voltage = None
    for detection in result:
        if detection[1].isdigit() and len(detection[1]) == 3:
            voltage = detection[1]
            break  # Take the first 3-digit number

    # Write to CSV 
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([serial_number, color_detected["Red"], color_detected["Green"], color_detected["Blue"], voltage])

    serial_number += 1

# Main loop
while True:
    image_path = input("Enter the image path (or type 'quit' to exit): ")
    if image_path.lower() == 'quit':
        break 

    if not os.path.isfile(image_path):
        print("Error: Image file not found.")
        continue

    process_image(image_path)

