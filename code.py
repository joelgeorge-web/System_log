import os
import cv2
import numpy as np
import sys
import easyocr
import re
from PIL import Image
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew
from typing import Union
import math
import keyboard

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)
test = False


# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")


# Define the texts that the model should recognize
aadhar_regex = r'^\d{4}\s\d{4}\s\d{4}$'
male = r'(?i)^Male\s*$'
dob = r'\d{2}/\d{2}/\d{4}'
name_regex = r'^(?!(?:GOVERNMENT|TIbGoupami|TTsGoupAmi)).*[A-Za-z]+\s[A-Za-z]+(?:\s[A-Za-z]+)?$'
pan_regex = r'^[A-Z\d]{10}$'
name_found = False  # Flag to track if a name has been printed
name_found1 = False  # Flag to track if a name has been printed
name_found2 = False  # Flag to track if a name has been printed
id_match_found = False # Flag to track if an ID match has been found
n1 = ""
n2 = ""

#rotate function
def rotate(
        image: np.ndarray, angle: float, background: Union[int, tuple[int, int, int]]
) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)


# Load the captured image
#change the name here like aadhar or pan or the name of your image.
#add the images 
a = input("Enter the name of the image: ")
image = cv2.imread(a)
grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
angle = determine_skew(grayscale)
rotated = rotate(image, angle, (0, 0, 0))
cv2.imwrite('rotated.jpg', rotated)

# Perform OCR on the image
result = reader.readtext('rotated.jpg')

for detection in result:
    text = detection[1]
    aadhar_match = re.search(aadhar_regex, text)
    pan_match = re.search(pan_regex, text)
    if aadhar_match:
        print("\n")
        print("AADHAR CARD")
        aadhar_no = aadhar_match.group()
        print("Aadhar No:", aadhar_no)
        for detection in result:
            text = detection[1]
            name_match = re.search(name_regex, text)
            if name_match and name_match.group().upper() != "TISGOUPGMI LGS UTY" and name_match.group().upper().replace(" ","") != "GOVERNMENTOFINDIA" and name_match.group().upper() != "GOVERNMENT QF INDIA":
                name = name_match.group()
                print("Name:", name)
                name_found = True
                break  # Stop iterating after finding a valid name
        for detection in result:
            text = detection[1]
            dob_match = re.search(dob, text)
            if dob_match:
                dob = dob_match.group()
                print("Date of Birth:", dob)
        for detection in result:
            text = detection[1]
            male_match = re.search(male, text)
            if male_match:
                print("Gender: Male")
        # Handle Aadhar card fields
        id_match_found = True
        break  # Stop iterating after finding a valid ID

    elif pan_match:
        print("\n")
        print("PAN CARD")
        pan_no = pan_match.group()
        corrected_pan = pan_no[:5].upper() + pan_no[5:9].upper() + pan_no[9:].upper()
        pan_no = corrected_pan[:5] + corrected_pan[5:9].replace('I', '1').replace('i', '1').replace('o', '0').replace('O', '0').replace('z', '2').replace('Z', '2') + corrected_pan[9:]
        print("Pan Account No:", pan_no)
        for detection in result:
            text = detection[1]
            text.upper()
            name_match = re.search(name_regex, text)
            if name_match and name_match.group() != "GOVT OF INDIA" and name_match.group() != "GOVErNMENT Of INDIA" and name_match.group().upper() != "TISGOUPGMI LGS UTY" and name_match.group() != "PERMANENT ACCOUNT NUMBER CARD" and name_match.group() != "Dale of Birtn" and name_match.group() != "INCOME TAX DEPARTMENT" and name_match.group() != "GOVERNMENT OF INDIA" and name_match.group() != "GOvernment OFINDIA" and name_match.group() != "GOVERNMENT Of INDIA" and name_match.group() != "Government of India" and name_match.group().upper() != n1:
                name = name_match.group()
                print("Name:", name.upper())
                name_found = True
                n1 = name.upper()
                break  # Stop iterating after finding a valid name
        for detection in result:
            text = detection[1]
            text.upper()
            name_match = re.search(name_regex, text)
            if name_match and name_match.group() != "GOVT OF INDIA" and name_match.group() != "GOVErNMENT Of INDIA" and name_match.group() != "Dale of Birtn" and name_match.group() != "INCOME TAX DEPARTMENT" and name_match.group() != "GOVERNMENT OF INDIA" and name_match.group() != "GOvernment OFINDIA" and name_match.group() != "GOVERNMENT Of INDIA" and name_match.group() != "Government of India" and name_match.group().upper() != n1:
                name1 = name_match.group()
                print("Father's Name:", name1.upper()) 
                name_found = True
                break  # Stop iterating after finding a valid name       
        for detection in result:
            text = detection[1]
            dob_match = re.search(dob, text)
            if dob_match:
                dob = dob_match.group()
                print("Date of Birth:", dob)

        # Handle Aadhar card fields
        id_match_found = True
        break  # Stop iterating after finding a valid ID

print("\n")

if not id_match_found:
    print("No valid ID card found")
    print("The following text was detected:")
    for detection in result:
        text = detection[1]
        print(text.upper())

    print("\n")

os.remove('rotated.jpg')

     



    
