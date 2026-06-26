import time
import RPi.GPIO as GPIO

LEFT_ENCODER = 24
RIGHT_ENCODER = 25

left_count = 0
right_count = 0


def left_pulse(channel):
    global left_count
    left_count += 1


def right_pulse(channel):
    global right_count
    right_count += 1


GPIO.setmode(GPIO.BCM)

GPIO.setup(LEFT_ENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT_ENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(LEFT_ENCODER, GPIO.FALLING, callback=left_pulse)
GPIO.add_event_detect(RIGHT_ENCODER, GPIO.FALLING, callback=right_pulse)

try:
    while True:
        left_count = 0
        right_count = 0

        time.sleep(1)

        print("Left:", left_count, "Right:", right_count)

finally:
    GPIO.cleanup()