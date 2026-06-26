import time
import RPi.GPIO as GPIO

from motor import Motor
from encoder import Encoder


LEFT_ENCODER_PIN = 24
RIGHT_ENCODER_PIN = 25

GPIO.setmode(GPIO.BCM)

motors = Motor()
left_encoder = Encoder(LEFT_ENCODER_PIN)
right_encoder = Encoder(RIGHT_ENCODER_PIN)

try:
    motors.forward(40)

    while True:
        left_encoder.reset()
        right_encoder.reset()

        time.sleep(0.2)

        left_speed = left_encoder.read()
        right_speed = right_encoder.read()

        print("Left:", left_speed, "Right:", right_speed)

finally:
    motors.stop()
    motors.cleanup()
    GPIO.cleanup()