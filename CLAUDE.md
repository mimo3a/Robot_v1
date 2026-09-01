# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Raspberry Pi robot control prototype in Python. Two DC motors via H-bridge PWM, two wheel encoders, two HC-SR04 ultrasonic sensors, and a NeoPixel strip. Current tuning work targets straight-line driving.

Read `AGENTS.md` for the full project context, calibration history, and the planned migration to an STM32F407 + IMU low-level controller. It contains rationale not derivable from code (e.g., why `update_encoder_correction` is smoothed rather than accumulating).

## Running

Code targets the Raspberry Pi and imports `RPi.GPIO` (and `pi5neo` for the LED strip). It cannot be executed on the Windows dev machine — only syntax-check or lint locally. To run on the Pi:

```
python my_robot.py
```

There is no build system, no test suite, and no linter configured. There are no dependencies beyond the system `RPi.GPIO` and `pi5neo`.

## Architecture

All GPIO uses BCM numbering. Pin assignments live as class constants and are the single source of truth:

- `Motor.LEFT_PINS = (17, 27)`, `RIGHT_PINS = (22, 23)`, encoders 24 / 25 — `motor.py:45-48`
- `HCSR04.LEFT_PINS = (5, 6)`, `RIGHT_PINS = (13, 19)` — `hc_sr04.py:50-51`
- LED strip on SPI `/dev/spidev0.0`, 12 LEDs — `led_band.py:11`

Control loop layering (`my_robot.py` → `motor.py` → `encoder.py`):

1. `my_robot.py` sets a `base_pwm` and a fixed `steering_trim`, then calls `Motor.update_encoder_correction()` in a loop.
2. `update_encoder_correction()` resets both encoders, sleeps `measure_time` (default 0.2 s), reads pulse counts, and computes `error = left_count - right_count`.
3. Correction is **smoothed proportional**, not integrated: `target = -error * gain` when `|error| > threshold`, then `correction += (target - correction) * smoothing`, clamped to `±max_correction`. This shape is deliberate — an earlier accumulating version drifted to extreme values; do not reintroduce integration without the same kind of clamp.
4. Final PWM: `left = base + trim + correction`, `right = base - trim - correction`, clamped to `0..100`.

`steering_trim` and the encoder correction are two separate compensations:
- `steering_trim` is a **fixed mechanical bias** calibrated by floor testing (positive value = more left PWM, compensates a left-pulling robot).
- Encoder correction is a **dynamic per-loop adjustment** based on wheel pulse balance.
Tune them independently. Encoder balance ≠ visually straight driving — trust floor behavior over encoder logs when adjusting `steering_trim`.

`Encoder` uses `GPIO.add_event_detect` with a falling-edge callback that increments `self.count`. `reset()` + `read()` after a fixed sleep is the only sampling pattern used.

## Safety conventions

- The main script must always call `motors.stop()` and `motors.cleanup()` in a `finally` block. `KeyboardInterrupt` is the expected exit path. Preserve this when editing `my_robot.py`.
- `Motor._clamp_speed` enforces `0..100`. Any new code that writes a duty cycle should go through it.
- `hc_sr04.get_distance()` returns `None` on timeout rather than blocking — callers must handle `None`.

## Future direction (context only, not yet implemented)

`AGENTS.md` describes a planned split where an STM32F407 takes over PWM, encoder counting, speed PID, and heading PID (with an added IMU gyro), and the Pi sends high-level commands like `FORWARD speed` / `TURN angle speed` over UART or I2C. Current files do not yet contain any of this — keep changes consistent with the existing Pi-only structure unless explicitly asked to start the split.
