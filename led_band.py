from pi5neo import Pi5Neo
import time

from pi5neo import Pi5Neo
import time
# SPI GPIO10 - MOSI
# GND - GND
# 5V - 5V
# Инициализация ленты NeoPixel на Raspberry Pi


neo = Pi5Neo('/dev/spidev0.0', 12, 800)

colors = [
    (50, 0, 0),   # красный
    (0, 50, 0),   # зелёный
    (0, 0, 50),   # синий
    (50, 50, 50), # белый
]

for i in range(12):
    r, g, b = colors[i % len(colors)]
    neo.set_led_color(i, r, g, b)
    neo.update_strip()
    time.sleep(0.5)

neo.clear_strip()
neo.update_strip()
