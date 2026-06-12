import RPi.GPIO as GPIO


class _SingleMotor:
    def __init__(self, pin1, pin2, freq):
        self.pin1 = pin1
        self.pin2 = pin2

        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)

        self.pwm1 = GPIO.PWM(self.pin1, freq)
        self.pwm2 = GPIO.PWM(self.pin2, freq)

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

    def cleanup(self):
        self.pwm1.stop()
        self.pwm2.stop()


class Motor:
    LEFT_PINS = (17, 27)
    RIGHT_PINS = (22, 23)
    PWM_FREQ = 1000

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.left = _SingleMotor(*self.LEFT_PINS, self.PWM_FREQ)
        self.right = _SingleMotor(*self.RIGHT_PINS, self.PWM_FREQ)

    def forward(self, speed):
        self.left.forward(speed)
        self.right.forward(speed)

    def backward(self, speed):
        self.left.backward(speed)
        self.right.backward(speed)

    def stop(self):
        self.left.stop()
        self.right.stop()

    def cleanup(self):
        self.left.cleanup()
        self.right.cleanup()
        GPIO.cleanup()
