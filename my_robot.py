import RPi.GPIO as GPIO
import time


class Motor:

    def __init__(self, pin1, pin2, freq=1000):

        self.pin1 = pin1
        self.pin2 = pin2

        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)

        self.pwm1 = GPIO.PWM(pin1, freq)
        self.pwm2 = GPIO.PWM(pin2, freq)

        self.pwm1.start(0)
        self.pwm2.start(0)

    def forward(self, speed):

        self.pwm1.ChangeDutyCycle(speed)
        self.pwm2.ChangeDutyCycle(0)

    def backward(self, speed):

        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(speed)

    def stop(self):

        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(0)


class Robot:

    def __init__(self):

        GPIO.setmode(GPIO.BCM)

        self.left_motor = Motor(17, 27)
        self.right_motor = Motor(22, 23)

    def forward(self, speed=50):

        self.left_motor.forward(speed)
        self.right_motor.forward(speed)

    def backward(self, speed=50):

        self.left_motor.backward(speed)
        self.right_motor.backward(speed)

    def left(self, speed=50):

        self.left_motor.stop()
        self.right_motor.forward(speed)

    def right(self, speed=50):

        self.left_motor.forward(speed)
        self.right_motor.stop()

    def stop(self):

        self.left_motor.stop()
        self.right_motor.stop()

    def cleanup(self):

        self.stop()
        GPIO.cleanup()


robot = Robot()

robot.forward(50)
time.sleep(2)

robot.left(60)
time.sleep(1)

robot.backward(40)
time.sleep(2)

robot.stop()
robot.cleanup()