# import the required packages and libraries

from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
from serial import *
from lxml import *
import os
import subprocess

#----------------------------------------------------------------------------------------------------------------

# Initialize serial communication - needed to get analog values from Arduino (FSR)
ser = Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

#----------------------------------------------------------------------------------------------------------------

# Visual Detection - Calculating EAR and MAR values

# EYE ASPECT RATIO
def euclidean_dist(ptA, ptB):
    
    # compute and return the euclidean distance between the two points
    return np.linalg.norm(ptA - ptB)

def eye_aspect_ratio(eye):
    
    # compute the euclidean distances between the two sets of vertical eye landmarks (x, y)-coordinates
    A = euclidean_dist(eye[1], eye[5])
    B = euclidean_dist(eye[2], eye[4])

    # compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
    C = euclidean_dist(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear

# MOUTH ASPECT RATIO
def mouth_aspect_ratio(mouth):
    
    # compute the euclidean distances between the two sets of vertical mouth landmarks (x, y)-coordinates
    A = dist.euclidean(mouth[2], mouth[10]) # 51, 59
    B = dist.euclidean(mouth[4], mouth[8]) # 53, 57

    # compute the euclidean distance between the horizontal mouth landmark (x, y)-coordinates
    C = dist.euclidean(mouth[0], mouth[6]) # 49, 55

    # compute the mouth aspect ratio
    mar = (A + B) / (2.0 * C)

    # return the mouth aspect ratio
    return mar

# FUNCTIONS FOR EXTRACTING VALUES FROM POLAR H10

def launch_subprocess(command):
    global p
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def sh(print_msg=True):
    for line in iter(p.stdout.readline, b''):
        line = line.rstrip()
        line = line.decode('utf8')
        line = str(line)
        line = line[39:41]
        if line != "sf":
            line = "0x"+line
            line = int(line,0)
        else:
            continue
        if print_msg:
            break
    return line

#----------------------------------------------------------------------------------------------------------------

# Construct the argument parse and parse the arguments - using 68-point face shape predictor

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=False, default='shape_predictor_68_face_landmarks.dat',
    help="path to facial landmark predictor")
ap.add_argument("-w", "--webcam", type=int, default=0,
    help="index of webcam on system")
ap.add_argument("-a", "--alarm", type=int, default=0,
    help="boolean used to indicate if TraffHat should be used")
args = vars(ap.parse_args())

# check to see if we are using GPIO/TrafficHat as an alarm
if args["alarm"] > 0:
    from gpiozero import TrafficHat
    th = TrafficHat()
    print("[INFO] using TrafficHat alarm...")

#----------------------------------------------------------------------------------------------------------------

# SET THRESHOLDS

# Define one constant, for mouth aspect ratio to indicate open mouth
MOUTH_AR_THRESH = 0.79

# Define two constants, one for the eye aspect ratio to indicate blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold for to set off the alarm
EYE_AR_THRESH = 0.27
EYE_AR_CONSEC_FRAMES = 5

# **CAN BE CHANGED** Set detection frames - this is to set the number of frames drowsiness will be detected in
DETECTION_FRAMES = 40

# Initialize other variables needed
COUNTER = 0
frame_count = 0
count_yawn = 0
count_eyes = 0
ALARM_ON = False
yawned = 0
counter = 0
constantlyOpen = False

#----------------------------------------------------------------------------------------------------------------

# Visual Detection - initializing HOG based detector

# Initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# Grab the indexes of the facial landmarks for the mouth
(mStart, mEnd) = (49, 68)

# Grab the indexes of the facial landmarks for the left and right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

#----------------------------------------------------------------------------------------------------------------

# Start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

frame_width = 840
frame_height = 560

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
time.sleep(1.0)

#----------------------------------------------------------------------------------------------------------------

# Launch subprocess - used to connect with Polar H10 & read BPM values

launch_subprocess('''gatttool -t random -b F2:BD:B3:70:9E:6A --char-write-req --handle=0x0011 --value=0100 --listen''')

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

# MAIN CODE/LOOP

# Loop over frames from the video
while True:
    
    #------------------------------------------------------------------------------------------------------------

    # GRIP DETECTION
    
    # Get pressure values from Arduino
    if ser.in_waiting > 0:
        b = ser.readline()
        string_n = b.decode()  # decode byte string into Unicode  
        string = string_n.rstrip() # remove \n and \r
        flt = float(string)        # convert string to float - will be used for estimating drowsiness
        print("Pressure: " + str(flt))
        
    #------------------------------------------------------------------------------------------------------------

    # BPM DETECTION
    
    current_bpm = sh()
    print("current bpm: ", current_bpm)
    
    #------------------------------------------------------------------------------------------------------------
      
    # VISUAL DETECTION
    
    # Grab the frame from the threaded video file stream, resize it, and convert it to grayscale channels
    frame = vs.read()
    frame = imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    rects = detector(gray, 0)

    # Loop over the face detections
    for rect in rects:
        
        # Determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Extract the mouth coordinates, then use the coordinates to compute the mouth aspect ratio
        mouth = shape[mStart:mEnd]
        
        mouthMAR = mouth_aspect_ratio(mouth)
        mar = mouthMAR
        
        # Compute the convex hull for the mouth, then visualize the mouth
        mouthHull = cv2.convexHull(mouth)
        
        # Extract the left and right eye coordinates, then use the coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        
        ear = (leftEAR + rightEAR) / 2.0
        
        # Compute the convex hull for the left and right eye, then visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
             
        # Hull for MAR
        cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
        cv2.putText(frame, "MAR: {:.2f}".format(mar), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        #------------------------------------------------------------------------------------------------------------
        
        # Determine drowsiness every 40 frames    
        if frame_count < DETECTION_FRAMES:                              
            frame_count +=1
            # Display the frame counter 0-40
            cv2.putText(frame, "Frame Count: {:.2f}".format(frame_count), (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Display the number of times the driver yawns within the 40-frames
            cv2.putText(frame, "# of times yawned: {:.2f}".format(count_yawn), (30, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
         
        # ---------------------------------------------------------------------------------------------------------------
            # Display "YAWNING" everytime the MAR falls below threshold value
            if mar > MOUTH_AR_THRESH:
                counter += 1
                
            if mar < MOUTH_AR_THRESH:
                    counter = 0
                
            if counter >= 5:
                count_yawn += 1
                cv2.putText(frame, "YAWNING", (250,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
                counter = 0
                
            #------------------------------------------------------------------------------------------------------------
                    
            # Display "EYES CLOSED FOR: XXX" everytime EAR falls below threshold value, and if so, increment the blink frame counter
            if ear < EYE_AR_THRESH:
                COUNTER += 1
                cv2.putText(frame, "Eyes closed for: {:.2f}".format(COUNTER), (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)            
                
                # If the eyes were closed for a sufficient number of frames, then sound the alarm
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    
                    # If the alarm is not on, turn it on
                    if not ALARM_ON:
                        ALARM_ON = True
                        
                        # Check to see if the TrafficHat buzzer should be sounded
                        if args["alarm"] > 0:
                            th.buzzer.blink(0.1, 0.1, 10,
                                background=True)
                            
                    # Draw an alarm on the frame
                    cv2.putText(frame, "EYES CLOSED!", (250, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Otherwise, the eye aspect ratio is not below the blink threshold, so reset the counter and alarm
            else:
                COUNTER = 0
                ALARM_ON = False
                yawned = 0
                
        else:
            frame_count = 0
            count_yawn = 0
            
#------------------------------------------------------------------------------------------------------------
            
    # Write the frame into the file 'output.avi'
    out.write(frame)
    
    # Show the frame
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    
    #------------------------------------------------------------------------------------------------------------

    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    
#------------------------------------------------------------------------------------------------------------

# Cleanup
cv2.destroyAllWindows()
vs.stop()
