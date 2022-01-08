# BPM DETECTION USING POLAR H10 + RASPBERRY PI
This code allows to detect the driver's BPM using the Polar H10 wireless sensor connected to Raspberry Pi

## Referenced Code 
- https://nob.ro/post/polar_h10_ubuntu/
- https://www.linuxquestions.org/questions/programming-9/python-os-system-function-howto-use-python-variables-572485/![image](https://user-images.githubusercontent.com/60349507/122549579-b4d24f00-d043-11eb-91b9-51c051afe09c.png)
- https://medium.com/swlh/creating-an-accelerometer-data-stream-with-polar-device-450a223f5789![image](https://user-images.githubusercontent.com/60349507/122549621-bef44d80-d043-11eb-870c-0448cd811e22.png)
- https://github.com/peplin/pygatt
- https://github.com/danielfppps/hbpimon

## Hardware Connection
**Hardware Needed:**
- Raspberry Pi 4
- Polar H10 Sensor (will be connected via Bluetooth)

<img width="686" alt="Screen Shot 2021-06-18 at 2 46 17 PM" src="https://user-images.githubusercontent.com/60349507/122549978-290cf280-d044-11eb-97db-919460cc26fe.png">

## Using the Code
- Clone the folder onto the Pi
- Find your polar H10's Bluetooth MAC Address (Reference: https://nob.ro/post/polar_h10_ubuntu/)

![image](https://user-images.githubusercontent.com/60349507/122550691-062f0e00-d045-11eb-94de-e04e1417a754.png)

- Open the *polarh10.py* using a Python IDE (Thonny IDE) and update line #24 with your Polar H10 MAC Address
- Run the the code to detect BPM values

## Results
- You can display the plotter to visualize the results - this will return BPM values:
- Results:

![Screen Shot 2021-06-18 at 2 56 01 PM](https://user-images.githubusercontent.com/60349507/122551131-a422d880-d045-11eb-8378-95aa66440b48.png)
