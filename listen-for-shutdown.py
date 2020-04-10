#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
import subprocess

TRUST_THRESHOLD2 = 50
RESET_PIN = 3
GHOST_CHECK_INTERVAL = 0.01

detected_rising = False

def on_gpio_rising(channel):
    global detected_rising
    if channel == RESET_PIN:
        detected_rising = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(RESET_PIN, GPIO.IN)  # according to Pi document, GPIO 3 has a hardware pull-up so specifying a pull up here will only result a warning
GPIO.add_event_detect(RESET_PIN, GPIO.RISING, callback=on_gpio_rising, bouncetime=200)

while True:
    while GPIO.input(RESET_PIN) == GPIO.LOW or not detected_rising:
        time.sleep(1.0)

    # check if ghost rising
    time.sleep(GHOST_CHECK_INTERVAL)
    trust_count = 0
    while GPIO.input(RESET_PIN) == GPIO.HIGH:
        trust_count += 1
        time.sleep(GHOST_CHECK_INTERVAL) 
        if trust_count >= TRUST_THRESHOLD2:
            break
    if trust_count < TRUST_THRESHOLD2:
        continue
    else:
        subprocess.call(['shutdown', '-h', 'now'], shell=False)
        break

GPIO.cleanup()

