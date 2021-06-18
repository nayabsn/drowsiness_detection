#!/usr/python/python3

from gpiozero import Buzzer
from time import sleep

buzzer=Buzzer(17)

while True:
    buzzer.on()
    print("Buzz")
    sleep(1)
    buzzer.off()
    print("------")
    sleep(1)
