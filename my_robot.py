import RPi.GPIO as GPIO
import time

print("START")

GPIO.setmode(GPIO.BCM)

class Moove:

    def __init__(self, in1=17, in2=27, in3=22, in4=23):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4

        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)

    def forward(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)

        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)

    def backward(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)

        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)


robot = Moove()

robot.forward()
time.sleep(2)

robot.backward()
time.sleep(2)

robot.stop()

GPIO.cleanup()