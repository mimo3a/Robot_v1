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

        # PWM
        self.pwm1 = GPIO.PWM(self.in1, 1000)
        self.pwm2 = GPIO.PWM(self.in2, 1000)
        self.pwm3 = GPIO.PWM(self.in3, 1000)
        self.pwm4 = GPIO.PWM(self.in4, 1000)

        self.pwm1.start(0)
        self.pwm2.start(0)
        self.pwm3.start(0)
        self.pwm4.start(0)

    def forward(self, speed=50):

        self.pwm1.ChangeDutyCycle(speed)
        self.pwm2.ChangeDutyCycle(0)

        self.pwm3.ChangeDutyCycle(speed)
        self.pwm4.ChangeDutyCycle(0)

    def backward(self, speed=50):

        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(speed)

        self.pwm3.ChangeDutyCycle(0)
        self.pwm4.ChangeDutyCycle(speed)

    def left(self, speed=50):

        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(0)

        self.pwm3.ChangeDutyCycle(speed)
        self.pwm4.ChangeDutyCycle(0)

    def right(self, speed=50):

        self.pwm1.ChangeDutyCycle(speed)
        self.pwm2.ChangeDutyCycle(0)

        self.pwm3.ChangeDutyCycle(0)
        self.pwm4.ChangeDutyCycle(0)

    def stop(self):

        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(0)
        self.pwm3.ChangeDutyCycle(0)
        self.pwm4.ChangeDutyCycle(0)

    def cleanup(self):
        self.stop()

        self.pwm1.stop()
        self.pwm2.stop()
        self.pwm3.stop()
        self.pwm4.stop()

        self.pwm1 = None
        self.pwm2 = None
        self.pwm3 = None
        self.pwm4 = None

        time.sleep(0.1)

        GPIO.cleanup()


robot = Moove()

# Вперёд медленно
robot.forward(40)
time.sleep(2)

# Вперёд быстро
robot.forward(80)
time.sleep(2)

# Поворот влево
robot.left(60)
time.sleep(1)

# Назад
robot.backward(50)
time.sleep(2)

# Стоп
robot.stop()

robot.cleanup()