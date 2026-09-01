# Robot v1 — Autonomous Differential-Drive Robot (Raspberry Pi)

A two-wheeled differential-drive robot controlled by a Raspberry Pi in **Python**.
This is **version 1** of the project: closed-loop motor control with wheel-encoder
feedback for straight-line driving, ultrasonic obstacle sensing, and an addressable
LED strip — all written as clean, reusable hardware-abstraction classes.

> **Project status:** ✅ Version 1 complete — tagged [`v1.0`](../../releases/tag/v1.0).
> Development continues in **[Robot v2](https://github.com/mimo3a/Robot_v2)** — a full
> redesign on an **STM32F407 (FreeRTOS)** for real-time low-level control plus a
> **Raspberry Pi (ROS)** for high-level logic.

---

## Highlights

- **Closed-loop straight-line driving.** Both wheels are kept in sync using
  interrupt-driven encoder feedback, with a smoothed proportional correction,
  a dead-band to ignore sensor jitter, and clamping to keep PWM commands safe.
- **Manual steering trim.** A simple, documented calibration constant compensates
  for mechanical drift on a straight run.
- **Clean hardware abstraction.** Each peripheral (motors, encoders, ultrasonic
  sensors, LED strip) is its own self-contained class with a small, obvious API.
- **Safe shutdown.** Motors always stop and GPIO is always released, even when the
  program is interrupted.
- **Continuous integration.** Every push is syntax-checked automatically via
  GitHub Actions.

## Hardware

| Component            | Details                                              |
|---------------------|------------------------------------------------------|
| Controller          | Raspberry Pi (Pi 5 — uses SPI + `pi5neo`)            |
| Drive               | 2 × DC motors via H-bridge driver (2 PWM pins each)  |
| Odometry            | 2 × wheel encoders (single-channel, falling edge)    |
| Distance sensing    | 2 × HC-SR04 ultrasonic sensors (left / right)        |
| Lighting            | 12 × WS2812 / NeoPixel LED strip (SPI)               |

### GPIO pin map (BCM)

| Function               | Pins            |
|------------------------|-----------------|
| Left motor (fwd/rev)   | GPIO 17, 27     |
| Right motor (fwd/rev)  | GPIO 22, 23     |
| Left encoder           | GPIO 24         |
| Right encoder          | GPIO 25         |
| Left HC-SR04 (trig/echo)  | GPIO 5, 6    |
| Right HC-SR04 (trig/echo) | GPIO 13, 19  |
| LED strip (SPI MOSI)   | GPIO 10         |

## Project structure

| File           | Responsibility                                                      |
|----------------|--------------------------------------------------------------------|
| `my_robot.py`  | Entry point: drives forward, runs the encoder-correction loop, prints live telemetry |
| `motor.py`     | `Motor` class — dual-motor control, PWM, and the encoder-based straight-line correction |
| `encoder.py`   | `Encoder` class — interrupt-driven pulse counting                  |
| `hc_sr04.py`   | `HCSR04` class — dual ultrasonic distance measurement with echo timeouts |
| `led_band.py`  | NeoPixel LED-strip demo animation                                  |

## How the straight-line control works

Both drive wheels rarely turn at exactly the same rate, so the robot drifts.
On every cycle the controller:

1. resets both encoders and counts pulses over a short fixed time window;
2. computes the error between left and right counts;
3. ignores errors inside a small dead-band (encoder noise);
4. converts the remaining error into a **smoothed** correction (a proportional
   step toward the target, not an ever-growing accumulator);
5. clamps the correction and applies it as opposite PWM offsets to the two motors,
   on top of a manual `steering_trim`.

```
left_pwm  = base + trim + correction
right_pwm = base - trim - correction
```

This keeps the robot tracking straight while never commanding an extreme
speed difference between the wheels.

## Getting started

Requires a Raspberry Pi with the wiring above. The GPIO libraries only run on
the Pi itself.

```bash
# On the Raspberry Pi
pip install RPi.GPIO pi5neo

# Drive forward with live encoder correction
python3 my_robot.py

# Stop with Ctrl-C — motors stop and GPIO is released automatically
```

## Roadmap → v2

Version 1 proved the mechanics and control on a single board. **Version 2** splits
the system into the right tool for each job:

- **STM32F407 + FreeRTOS** — hard real-time low-level control (motors, PWM, encoders).
- **Raspberry Pi + ROS** — high-level logic, navigation, and communication.

See **[Robot v2](https://github.com/mimo3a/Robot_v2)**.

---

*Written in Python for Raspberry Pi. Version 1 — archived and tagged `v1.0`.*
