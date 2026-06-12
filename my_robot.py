import time

from motor import Motor


motors = Motor()

try:
    motors.forward(40)
    time.sleep(2)
    motors.stop()
finally:
    motors.cleanup()
