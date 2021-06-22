# VISUAL DROWSINESS DETECTION USING RASPBERRY PI
This code allows to detect drowsiness using facial features - eye blinking + yawning using Raspberry Pi

## Referenced Code
- https://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv
- https://www.pyimagesearch.com/2017/10/23/raspberry-pi-facial-landmarks-drowsiness-detection-with-opencv-and-dlib/

## Hardware Connection
**Hardware Needed:**
- Raspberry Pi 4
- Night-vision Raspberry Pi Camera (any camera would work!)
- Connect the camera to the Pi:

![Odseven-Raspberry-Pi-Night-Vision-Camera-Module-5MP-Ov5647-Webcam-Video-1080P-for-Raspberry-Pi-3](https://user-images.githubusercontent.com/60349507/122551645-52c71900-d046-11eb-9682-2013f44aa210.jpg)

## Using the Code
- After connecting the camera to the Raspberry Pi, clone the visual_detection folder onto the Pi
- From terminal, browse to where the folder is cloned & run the following command:
- *python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav*
- ***Other .py files in this folder include***
  - *ear_detection*: This code will only detect, measure and display the eye-aspect ratio
  - *mar_detection*: This code will only detect, measure and display the mouth-aspect ratio

## Results
- The result of this code will open a video stream and display:
  - EAR value (Eye-Aspect Ratio) - display an alert if eyes have been closed (under a threshold value - set to 0.28 in this code, can be changed)
  - MAR value (Mouth-Aspect Ratio) - display an alert if mouth has been opened for yawning (a threshold value of 0.78, can be changed)
  - How long eyes have been closed for
  - How many times you have yawned within a certain time frame (set to 40 in this code - can be changed)
- Results:

![image](https://user-images.githubusercontent.com/60349507/122551531-27dcc500-d046-11eb-8726-da1ee40972fe.png)
