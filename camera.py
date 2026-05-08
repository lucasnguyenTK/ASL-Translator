import cv2 as cv
import numpy as np

#default camera index 0
cam = cv.VideoCapture(0)

if not cam.isOpened():
    print("Cannot open camera")
    exit()

while True:
    #capture frame-by-frame
    ret, frame = cam.read()

    #if frame is read correctly, ret = True
    if not ret:
        print("Can't read frame. Exit")
        break
    
    #display captured frame
    cv.imshow('Camera', frame)

    #press 'q' to exit loop = stop displaying camera
    if cv.waitKey(1) == ord('q'):
        break

#release capture 
cam.release()
cv.destroyAllWindows()

    
