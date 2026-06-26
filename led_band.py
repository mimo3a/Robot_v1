from pi5neo import Pi5Neo
import time


# Wiring:
# SPI GPIO10 - MOSI
# GND - GND
# 5V - 5V

# Initialize a 12 LED NeoPixel strip on Raspberry Pi SPI bus 0.
neo = Pi5Neo('/dev/spidev0.0', 12, 800)

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
