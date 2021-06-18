# DRIVER ALERTING SYSTEM USING RASPBERRY PI
This code alerts the driver using a buzzer and vibration discs connected to the Raspberry Pi

## Hardware Connection
**Hardware Needed:**
- Raspberry Pi 4
- Breadboard
- 2 Vibration Disks
- 1 Active Buzzer
- Connections:
  - Buzzer: +ve side to GPIO17, -ve to GND
  - Vibration disc 1: +ve side to GPIO14, -ve to GND
  - Vibration disc 2: +ve side to GRIO15, -ve to GND

![image](https://user-images.githubusercontent.com/60349507/122548786-d4b54300-d042-11eb-9dc5-bddaa149c30c.png)

## Using the Code
- Clone the folder onto the Pi
- Launch terminal and browse to the folder
- Run the command *python final_output_test.py*

## Results
- Once the code is run, the buzzer and vibration discs will turn on and off in 1 second intervals - this can be changed as needed
