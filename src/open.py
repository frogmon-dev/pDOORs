# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

led_pin = 20

GPIO.setmode(GPIO.BCM)

GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, 0)

time.sleep(1)

GPIO.output(led_pin, 1)

GPIO.cleanup(led_pin)