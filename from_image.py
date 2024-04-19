import easyocr
import cv2 
import numpy as np
import csv
import os

# Load the image
image_path = r'C:\Users\Joel\Desktop\PYTHON\module_log\185.jpg'  # Replace with your image file path
img = cv2.imread(image_path)

reader = easyocr.Reader(['en'])  # For English, use a list of language codes 

# Detect text in the image
result = reader.readtext(img, allowlist ='0123456789')

#only extract 3 digit numbers from result
result = [item for item in result if item[1].isdigit() and len(item[1]) == 3]

#create a csv file data.csv if it does not exist and write the header as "Voltage"
if not os.path.isfile('data.csv'):
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Voltage"])

# Print the extracted text
for detection in result:
    text = detection[1]
    #write to csv
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([text])
    print(text)



  