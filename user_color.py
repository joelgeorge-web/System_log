import cv2
import numpy as np


# Color detection thresholds
lowerRed = np.array([-15, 40, 140])
upperRed = np.array([15, 140, 255])
lowerBlue = np.array([110, 100, 200])
upperBlue = np.array([130, 255, 255])
lowerGreen = np.array([45, 40, 140])
upperGreen = np.array([75, 200, 255])


def process_image(image_path):
    img = cv2.imread(image_path)  # Load the image

    if img is None:
        print("Error: Could not load the image.")
        return

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask2 = cv2.inRange(img_hsv, lowerRed, upperRed)
    mask3 = cv2.inRange(img_hsv, lowerBlue, upperBlue)
    mask4 = cv2.inRange(img_hsv, lowerGreen, upperGreen)

    mask4_contours, hierarchy = cv2.findContours(mask4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(mask4_contours) != 0:
        for mask4_contour in mask4_contours:
            if cv2.contourArea(mask4_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask4_contour)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, 'Green', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                print("Green detected")  # Print when green is found

    mask3_contours, hierarchy = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(mask3_contours) != 0:
        for mask3_contour in mask3_contours:
            if cv2.contourArea(mask3_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask3_contour)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, 'Blue', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                print("Blue detected")  # Print when blue is found

    mask2_contours, hierarchy = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(mask2_contours) != 0:
        for mask2_contour in mask2_contours:
            if cv2.contourArea(mask2_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask2_contour)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, 'Red', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                print("Red detected")  # Print when red is found 

# ... (Rest of your code remains the same) ...

# Get image path from user
image_path = input("Enter the image path: ")

# Process the image
process_image(image_path)

cv2.waitKey(0)  # Wait for key press before closing
cv2.destroyAllWindows() 
