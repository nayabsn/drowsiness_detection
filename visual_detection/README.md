# VISUAL DROWSINESS DETECTION
This code allows to detect drowsiness using facial features - eye blinking + yawning

## Referenced Code
https://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv

## Hardware Connection
**Hardware Needed:**
- Raspberry Pi 4
- Night-vision Raspberry Pi Camera (any camera would work!)
- Connect the camera to the Pi --> https://user-images.githubusercontent.com/60349507/122542709-0f67ad00-d03c-11eb-89c4-3e195f5614dc.jpg

## Using the Code
- After connecting the camera to the Raspberry Pi, clone the visual_detection folder onto the Pi
- From terminal, browse to where the folder is cloned & run the following command:
- *python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav*

## Results
- The result of this code will open a video stream and display:
  - EAR value (Eye-Aspect Ratio) - display an alert if eyes have been closed (under a threshold value - set to 0.28 in this code, can be changed)
  - MAR value (Mouth-Aspect Ratio) - display an alert if mouth has been opened for yawning (a threshold value of 0.78, can be changed)
  - How long eyes have been closed for
  - How many times you have yawned within a certain time frame (set to 40 in this code - can be changed)
- RESULTING IMAGE --> https://user-images.githubusercontent.com/60349507/122543615-03301f80-d03d-11eb-8110-650c764bf610.png
