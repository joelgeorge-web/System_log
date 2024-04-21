import easyocr
import cv2 
import numpy as np
import csv
import os

reader = easyocr.Reader(['en'])  # For English, use a list of language codes 

# Create CSV file if it doesn't exist
if not os.path.isfile('data.csv'):
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Voltage"])

# Main processing loop
while True:
    image_path = input("Enter the image path (or type 'quit' to exit): ")
    if image_path.lower() == 'quit':
        break  # Exit the loop

    if not os.path.isfile(image_path):
        print("Error: Image file not found.")
        continue

    img = cv2.imread(image_path)

    # Detect text in the image
    result = reader.readtext(img, allowlist ='0123456789')

    # Only extract 3 digit numbers from result
    

    # Print the extracted text
    for detection in result:
        text = detection[1]
        print(text)
