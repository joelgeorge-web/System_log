import cv2
import numpy as np

webcam_video = cv2.VideoCapture(0)

#lowerYellow = np.array([45, 100, 150])
#upperYellow = np.array([75, 255, 255])

lowerRed = np.array([-15, 40, 140])
upperRed = np.array([15, 140, 255])

lowerBlue = np.array([110, 100, 200])
upperBlue = np.array([130, 255, 255])

lowerGreen = np.array([45, 40, 140])
upperGreen = np.array([75, 200, 255])

while True:
    success, video = webcam_video.read()

    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)

    #mask1 = cv2.inRange(img, lowerYellow, upperYellow)
    #mask1 = cv2.GaussianBlur(mask1,(5,5),0)

    mask2 = cv2.inRange(img, lowerRed, upperRed)
    mask2 = cv2.GaussianBlur(mask2,(5,5),0)

    mask3 = cv2.inRange(img, lowerBlue, upperBlue)
    mask3 = cv2.GaussianBlur(mask3,(5,5),0)

    mask4 = cv2.inRange(img, lowerGreen, upperGreen)
    mask4 = cv2.GaussianBlur(mask4,(5,5),0)

    mask4_contours, hierarchy = cv2.findContours(mask4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(mask4_contours) != 0:
        for mask4_contour in mask4_contours:
            if cv2.contourArea(mask4_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask4_contour)
                cv2.rectangle(video, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(video, 'Green', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    mask3_contours, hierarchy = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(mask3_contours) != 0:
        for mask3_contour in mask3_contours:
            if cv2.contourArea(mask3_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask3_contour)
                cv2.rectangle(video, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(video, 'Blue', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    mask2_contours, hierarchy = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(mask2_contours) != 0:
         for mask2_contour in mask2_contours:
            if cv2.contourArea(mask2_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask2_contour)
                cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(video, 'Red', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    """mask1_contours, hierarchy = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(mask1_contours) != 0:
        for mask1_contour in mask1_contours:
            if cv2.contourArea(mask1_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask1_contour)
                cv2.rectangle(video, (x, y), (x + w, y + h), (0, 255, 255), 2)
                cv2.putText(video, 'Yellow', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)"""

    cv2.imshow("window", video)

    cv2.waitKey(1)
    cv2.destroyAllWindows