import cv2 as cv
import numpy as np
import mediapipe as mp
import time 


#build and configure tasks
class landmarker_and_result():
    def __init__(self):
        self.result = None #change this when want to display results
        self.landmarker = mp.tasks.vision.HandLandmarker
        self.createLandmarker()
#create landmarker instance with the live stream mode
    def createLandmarker(self):
        #callback function
        def update_result(result: mp.tasks.vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
            self.result = result
    
        options = mp.tasks.vision.HandLandmarkerOptions( 
            base_options = mp.tasks.BaseOptions(model_asset_path="hand_landmarker.task"), # path to model
            running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM, # running on a live stream
            num_hands = 2, # track both hands
            min_hand_detection_confidence = 0.3, # lower than value to get predictions more often
            min_hand_presence_confidence = 0.3, # lower than value to get predictions more often
            min_tracking_confidence = 0.3, # lower than value to get predictions more often
            result_callback = update_result)
    
    #init landmarker
        self.landmarker = self.landmarker.create_from_options(options)

    #convert image frame into image datatype that MediaPipe expects
    def detect_async(self, frame):
        #convert np to mp image
        mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame)
        #detects landmarks
        self.landmarker.detect_async(image = mp_image, timestamp_ms = int(time.time() * 1000))
    #function to close landmarker
    def close(self):
        #close landmarker
        self.landmarker.close() 
  

def main():
    #access video
    cam = cv.VideoCapture(0)

    if not cam.isOpened():
        print("Can't access camera")
        exit()

    #intialize capture loop
    hand_landmarker = landmarker_and_result()
    #if able to open camera
    while True:
        #read frame by frame
        success, frame = cam.read()
        #if not success, then can't capture
        if not success:
            print("Can't read frame")
            break
        #mirror the displayed video
        frame = cv.flip(frame, 1)

        hand_landmarker.detect_async(frame)
        print(hand_landmarker.result)

        #display video output
        cv.imshow('Video', frame)
        #press q to exit
        if cv.waitKey(1) == ord('q'):
            break
    #release frame and destroy all windows
    cam.release()
    cv.destroyAllWindows()
    hand_landmarker.close()

if __name__ == "__main__":
    main()