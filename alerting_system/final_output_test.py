from gpiozero import PWMOutputDevice
from time import sleep, time
from gpiozero import Buzzer

motor1 = PWMOutputDevice(14)
motor2 = PWMOutputDevice(15)
buzzer=Buzzer(17)

sleep (2)

while True:
    buzzer.on()
    motor1.value = 1
    motor2.value = 1
    print("ALERT!")

    sleep(1)
    
    buzzer.off()
    motor1.value = 0
    motor2.value = 0
    print("-------")
    sleep(1)
