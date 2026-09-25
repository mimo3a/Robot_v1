from pi5neo import Pi5Neo
import time


class LedBand:
    """Control the 12-pixel WS2812 status strip on Raspberry Pi 5."""

    LED_COUNT = 12
    SPI_DEVICE = "/dev/spidev0.0"
    SPI_SPEED = 800

    def __init__(self):
        self.neo = Pi5Neo(self.SPI_DEVICE, self.LED_COUNT, self.SPI_SPEED)

        # On this Pi 5 SPI setup MOSI can remain HIGH between transfers.
        # Append zero bytes to create the LOW reset/latch interval required
        # by WS2812 LEDs.
        def send_spi_data_with_reset():
            self.neo.spi.xfer3(self.neo.raw_data + [0] * 64)

        self.neo.send_spi_data = send_spi_data_with_reset

    def set_color(self, red, green, blue):
        """Set all LEDs to one RGB color."""
        for i in range(self.LED_COUNT):
            self.neo.set_led_color(i, red, green, blue)
        self.neo.update_strip()

    def green(self):
        """Ready / normal operation."""
        self.set_color(0, 50, 0)

    def red(self):
        """Stopped / obstacle detected."""
        self.set_color(50, 0, 0)

    def blue(self):
        """Optional status color."""
        self.set_color(0, 0, 50)

    def off(self):
        """Turn all LEDs off."""
        self.neo.clear_strip()
        self.neo.update_strip()

    def test_animation(self, delay=0.5):
        """Light LEDs one by one, cycling through test colors."""
        colors = [
            (50, 0, 0),
            (0, 50, 0),
            (0, 0, 50),
            (50, 50, 50),
        ]

        for i in range(self.LED_COUNT):
            red, green, blue = colors[i % len(colors)]
            self.neo.set_led_color(i, red, green, blue)
            self.neo.update_strip()
            time.sleep(delay)

        self.off()


if __name__ == "__main__":
    leds = LedBand()

    try:
        leds.test_animation()
    except KeyboardInterrupt:
        pass
    finally:
        leds.off()
