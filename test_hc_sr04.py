"""Continuous test for the two HC-SR04 ultrasonic sensors."""

import time

from hc_sr04 import HCSR04


sensor = HCSR04()

try:
    while True:
        sensor.messen()
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    sensor.cleanup()
