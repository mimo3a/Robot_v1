import time
import RPi.GPIO as GPIO

from motor import Motor
from encoder import Encoder


LEFT_ENCODER_PIN = 24
RIGHT_ENCODER_PIN = 25

GPIO.setmode(GPIO.BCM)

base_pwm = 60
correction = 0

motors = Motor()
left_encoder = Encoder(LEFT_ENCODER_PIN)
right_encoder = Encoder(RIGHT_ENCODER_PIN)

try:
    motors.set_speed(base_pwm, base_pwm)

    while True:
        left_encoder.reset()
        right_encoder.reset()

        time.sleep(0.2)

        left_count = left_encoder.read()
        right_count = right_encoder.read()

        error = left_count - right_count

        if error > 1:
            correction -= 1
        elif error < -1:
            correction += 1

        correction = max(-30, min(30, correction))

        left_pwm = base_pwm + correction
        right_pwm = base_pwm - correction

        motors.set_speed(left_pwm, right_pwm)

        print(
            "Left:", left_count,
            "Right:", right_count,
            "Error:", error,
            "Correction:", correction,
            "PWM L:", left_pwm,
            "PWM R:", right_pwm
        )

finally:
    motors.stop()
    motors.cleanup()
    GPIO.cleanup()