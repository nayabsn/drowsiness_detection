# VISUAL DROWSINESS DETECTION
This code allows to detect drowsiness using facial features - eye blinking + yawning

## Referenced Code
https://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv

## Hardware Connection
**Hardware Needed:**
- Raspberry Pi 4
- Night-vision Raspberry Pi Camera (any camera would work!)
- Connect the camera https://user-images.githubusercontent.com/60349507/122542709-0f67ad00-d03c-11eb-89c4-3e195f5614dc.jpg

## Using the Code
- After connecting the camera to the Raspberry Pi, clone the visual_detection folder onto the Pi
- From terminal, browse to where the folder is cloned & run the following command:
- *python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav*
