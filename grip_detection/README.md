# GRIP DETECTION USING ARDUINO + RASPBERRY PI
This code allows to detect the grip force using Arduino serial port with values transffered to Raspberry Pi

## Referenced Code/Circuit
https://user-images.githubusercontent.com/60349507/122545532-fe6c6b00-d03e-11eb-93bb-f9e7e85f7036.png
https://www.youtube.com/watch?v=LREOsIXPoLY

## Hardware Connection
**Hardware Needed:**
- Arduino Uno
- Raspberry Pi 4
- Force Sensitive Resistor - Long SEN-09674
- Breadboard
- 3.3K Ohm Resistor
- Connection:
  - The sensor connects to a 3.3k resistor on one side, and to 5V on the Arduino on the other
  - The 3.3k resistor connects to the sensor on one side, and to GND on the Arduino on the other
  - The sensor also connects to pin A0 before the resistor

![image](https://user-images.githubusercontent.com/60349507/122548295-375a0f00-d042-11eb-83b3-bf99561bd5b6.png)

<img width="463" alt="Screen Shot 2021-06-18 at 2 20 58 PM" src="https://user-images.githubusercontent.com/60349507/122547035-a9315900-d040-11eb-941c-bf5d9f12bc8f.png">

## Using the Code
- Install Arduino on the Raspberry Pi 
- Clone the folder onto the Pi, upload the .ino code to your board
  - This will display the output from the sensor in Arduino Serial Monitor. Note that you will need to **CLOSE** the Arduino Serial Monitor to transfer and display values to the Pi
- Once the .ino code has been uploaded to the Arduino board, browse to where the .py file has been cloned
- Open your Python IDE (Thonny IDE) and run the .py code 

## Results
- You can display the plotter to visualize the results - this will return the amount of force applied to your resistor
- Results:
-
![image](https://user-images.githubusercontent.com/60349507/122546810-63749080-d040-11eb-86d2-52e82e558a97.png)

