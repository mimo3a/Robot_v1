from pi5neo import Pi5Neo
import time


# Wiring:
# SPI GPIO10 - MOSI
# GND - GND
# 5V - 5V

# Initialize a 12 LED NeoPixel strip on Raspberry Pi SPI bus 0.
neo = Pi5Neo('/dev/spidev0.0', 12, 800)


def send_spi_data_with_reset():
    """Send LED data followed by a WS2812 reset/latch LOW interval.

    On this Pi 5 SPI setup MOSI remains HIGH between transfers.  Appending
    zero bytes makes the data line LOW for about 78 microseconds, allowing
    WS2812 LEDs to latch the received frame.
    """
    neo.spi.xfer3(neo.raw_data + [0] * 64)


# Override the library's transmitter without modifying site-packages.
neo.send_spi_data = send_spi_data_with_reset

colors = [
    (50, 0, 0),    # red
    (0, 50, 0),    # green
    (0, 0, 50),    # blue
    (50, 50, 50),  # white
]

for i in range(12):
    # Light each LED in sequence, cycling through the color list.
    r, g, b = colors[i % len(colors)]
    neo.set_led_color(i, r, g, b)
    neo.update_strip()
    time.sleep(0.5)

# Turn the strip off after the animation finishes.
neo.clear_strip()
neo.update_strip()
