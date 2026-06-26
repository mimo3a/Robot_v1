import time

import RPi.GPIO as GPIO


class _SingleHCSR04:
    def __init__(self, trig_pin, echo_pin):
        self.trig = trig_pin
        self.echo = echo_pin

        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        GPIO.output(self.trig, False)
        time.sleep(0.1)

    def get_distance(self):
        # Send the 10 microsecond trigger pulse required by the HC-SR04 sensor.
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        start_time = time.time()
        timeout = start_time + 0.05

        # Wait for the echo pulse to start, but avoid blocking forever.
        while GPIO.input(self.echo) == 0:
            start_time = time.time()
            if start_time > timeout:
                return None

        stop_time = time.time()

        # Wait for the echo pulse to end so its duration can be measured.
        while GPIO.input(self.echo) == 1:
            stop_time = time.time()
            if stop_time > timeout:
                return None

        elapsed = stop_time - start_time
        # Distance in centimeters: speed of sound is about 34300 cm/s, and the
        # pulse travels to the object and back.
        distance = (elapsed * 34300) / 2

        return round(distance, 1)


class HCSR04:
    LEFT_PINS = (5, 6)
    RIGHT_PINS = (13, 19)

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.left = _SingleHCSR04(*self.LEFT_PINS)
        self.right = _SingleHCSR04(*self.RIGHT_PINS)

    def get_left_distance(self):
        return self.left.get_distance()

    def get_right_distance(self):
        return self.right.get_distance()

    def get_distances(self):
        return {
            "left": self.get_left_distance(),
            "right": self.get_right_distance(),
        }

    def messen(self):
        distances = self.get_distances()

        if distances["left"] is not None:
            print(f"Left Distance: {distances['left']} cm")
        else:
            print("Left No echo")

        if distances["right"] is not None:
            print(f"Right Distance: {distances['right']} cm")
        else:
            print("Right No echo")

    def cleanup(self):
        GPIO.cleanup()
