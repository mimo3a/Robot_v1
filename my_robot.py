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
try:
    while True:
        left_encoder.reset()
        right_encoder.reset()

        time.sleep(0.2)

        left_count = left_encoder.read()
        right_count = right_encoder.read()

        error = right_count - left_count

        if error > 1:
            left_pwm += 1
            right_pwm -= 1
        elif error < -1:
            left_pwm -= 1
            right_pwm += 1

    left_pwm = max(20, min(100, left_pwm))
    right_pwm = max(20, min(100, right_pwm))

    motors.set_speed(left_pwm, right_pwm)

    print(
            "Left:", left_count,
            "Right:", right_count,
            "PWM L:", left_pwm,
            "PWM R:", right_pwm
        )
finally:
    motors.stop()
    motors.cleanup()
    GPIO.cleanup()