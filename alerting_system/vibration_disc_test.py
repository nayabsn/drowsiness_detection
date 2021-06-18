from gpiozero import PWMOutputDevice
from time import sleep, time

motor1 = PWMOutputDevice(14)
motor2 = PWMOutputDevice(15)

sleep (2)

while True:
    motor1.value = 1
    motor2.value = 1

    print("Vibrate")
    sleep(1)
    
    motor1.value = 0
    motor2.value = 0
    
    print("-------")
    sleep(1)
