import time
import RPi.GPIO as GPIO

from motor import Motor
from encoder import Encoder


LEFT_ENCODER_PIN = 24
RIGHT_ENCODER_PIN = 25

GPIO.setmode(GPIO.BCM)

# Base motor power in percent. The correction value is adjusted at runtime
# to keep both encoder counts close to each other.
base_pwm = 60
correction = 0

motors = Motor()
left_encoder = Encoder(LEFT_ENCODER_PIN)
right_encoder = Encoder(RIGHT_ENCODER_PIN)

try:
    motors.set_speed(base_pwm, base_pwm)

    while True:
        # Measure encoder pulses over a short fixed time window.
        left_encoder.reset()
        right_encoder.reset()

        time.sleep(0.2)

        left_count = left_encoder.read()
        right_count = right_encoder.read()

        error = left_count - right_count

        # If one wheel reports more pulses, slow that side down and speed the
        # other side up by changing the shared correction value.
        if error > 1:
            correction -= 1
        elif error < -1:
            correction += 1

        # Limit correction so the robot cannot command extreme PWM differences.
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
    # Always stop motors and release GPIO pins, even when the loop is interrupted.
    motors.stop()
    motors.cleanup()
    GPIO.cleanup()
