import time
import RPi.GPIO as GPIO

from motor import Motor
from encoder import Encoder


LEFT_ENCODER_PIN = 24
RIGHT_ENCODER_PIN = 25

GPIO.setmode(GPIO.BCM)

left_pwm = 70
right_pwm = 30

motors = Motor()
left_encoder = Encoder(LEFT_ENCODER_PIN)
right_encoder = Encoder(RIGHT_ENCODER_PIN)

motors.set_speed(left_pwm, right_pwm)

while True:
    left_encoder.reset()
    right_encoder.reset()

    time.sleep(0.2)

    left_count = left_encoder.read()
    right_count = right_encoder.read()

    print("Left:", left_count, "Right:", right_count)