import time

import RPi.GPIO as GPIO

from encoder import Encoder


class _SingleMotor:
    def __init__(self, pin1, pin2, freq):
        self.pin1 = pin1
        self.pin2 = pin2

        # Each motor uses two PWM pins: one for forward and one for reverse.
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)

        self.pwm1 = GPIO.PWM(self.pin1, freq)
        self.pwm2 = GPIO.PWM(self.pin2, freq)

        self.pwm1.start(0)
        self.pwm2.start(0)

    def forward(self, speed):
        # Drive forward by powering only the first H-bridge input.
        self.pwm1.ChangeDutyCycle(speed)
        self.pwm2.ChangeDutyCycle(0)

    def backward(self, speed):
        # Drive backward by powering only the second H-bridge input.
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(speed)

    def stop(self):
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm1.stop()
        self.pwm2.stop()
        


class Motor:
    # BCM GPIO pins connected to the left and right motor driver inputs.
    LEFT_PINS = (17, 27)
    RIGHT_PINS = (22, 23)
    LEFT_ENCODER_PIN = 24
    RIGHT_ENCODER_PIN = 25
    PWM_FREQ = 1000

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.left = _SingleMotor(*self.LEFT_PINS, self.PWM_FREQ)
        self.right = _SingleMotor(*self.RIGHT_PINS, self.PWM_FREQ)
        self.left_encoder = Encoder(self.LEFT_ENCODER_PIN)
        self.right_encoder = Encoder(self.RIGHT_ENCODER_PIN)

    def stop(self):
        self.left.stop()
        self.right.stop()

    def cleanup(self):
        self.left.cleanup()
        self.right.cleanup()
        GPIO.cleanup()

    def set_speed_forward(self, left_speed, right_speed):
        # Independent forward speeds make steering correction possible.
        self.left.forward(left_speed)
        self.right.forward(right_speed)

    def update_encoder_correction(
        self,
        base_speed,
        correction,
        measure_time=0.2,
        # threshold=1,
        max_correction=30
    ):
        # Measure encoder pulses over a short fixed time window.
        self.left_encoder.reset()
        self.right_encoder.reset()

        time.sleep(measure_time)

        left_count = self.left_encoder.read()
        right_count = self.right_encoder.read()
        error = left_count - right_count

        # If one wheel reports more pulses, slow that side down and speed the
        # other side up by changing the shared correction value.
        if error > 0:
            correction -= 1
        elif error < 0:
            correction += 1

        # Limit correction so the robot cannot command extreme PWM differences.
        correction = max(-max_correction, min(max_correction, correction))

        left_pwm = base_speed + correction
        right_pwm = base_speed - correction
        self.set_speed_forward(left_pwm, right_pwm)

        return {
            "left_count": left_count,
            "right_count": right_count,
            "error": error,
            "correction": correction,
            "left_pwm": left_pwm,
            "right_pwm": right_pwm,
        }

    def set_speed_left(self, speed):
        self.left.forward(speed)
        self.right.stop()

    def set_speed_right(self, speed):
        self.left.stop()
        self.right.forward(speed)
