import RPi.GPIO as GPIO


class Encoder:
    def __init__(self, pin):
        self.pin = pin
        self.count = 0

        # Pull-up keeps the input stable until the encoder pulls it low.
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            self.pin,
            GPIO.FALLING,
            callback=self._pulse
        )

    def _pulse(self, channel):
        # GPIO calls this callback on every falling edge from the encoder.
        self.count += 1

    def read(self):
        return self.count

    def reset(self):
        # Start a new measurement window.
        self.count = 0
