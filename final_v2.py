import cv2
import numpy as np
import easyocr
import csv
import os
import time



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
        writer.writerow(["SI No", "Red", "Green", "Blue", "Voltage"])

# Initialize serial number for CSV after fnding the last serial number in the data.csv file and adding 1 to it
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        pass
    serial_number = int(row[0]) + 1 if row else 1

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



    # Write to CSV 
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([serial_number, color_detected["Red"], color_detected["Green"], color_detected["Blue"], voltage])

    serial_number += 1

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

