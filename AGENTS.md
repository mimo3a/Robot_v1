# Robot_v1 Project Context

This project is a Raspberry Pi robot control prototype written in Python.

## Current Hardware

- Raspberry Pi runs the Python control code.
- Two DC motors are controlled through GPIO PWM.
- Each motor has two H-bridge input pins:
  - Left motor: BCM GPIO 17, 27
  - Right motor: BCM GPIO 22, 23
- Wheel encoders are connected to:
  - Left encoder: BCM GPIO 24
  - Right encoder: BCM GPIO 25
- Ultrasonic distance sensors and LED strip code also exist, but current tuning work is focused on straight driving.

## Current Files

- `my_robot.py`
  - Main script for driving forward.
  - Uses `base_pwm = 60`.
  - Uses `steering_trim` to compensate physical drift.
  - Prints encoder counts, error, correction, and final PWM values.
  - Handles `Ctrl+C` cleanly and stops motors in `finally`.
- `motor.py`
  - Defines motor pins, encoder pins, PWM frequency, and motor control.
  - Contains encoder-based correction in `update_encoder_correction()`.
  - Clamps PWM to `0..100`.
  - Uses smoothed correction instead of accumulating correction forever.
- `encoder.py`
  - Counts falling-edge pulses from a GPIO encoder input.
- `hc_sr04.py`
  - Ultrasonic sensor helper.
- `led_band.py`
  - LED strip helper.

## Straight Driving Calibration

The robot originally pulled left. A fixed steering trim was added.

Current recommended value:

```python
steering_trim = 5
```

Meaning:

- Positive `steering_trim` gives more PWM to the left motor and less PWM to the right motor.
- With `base_pwm = 60` and `steering_trim = 5`, initial motor PWM is:
  - Left: `65`
  - Right: `55`

Calibration procedure:

1. Put the robot on a straight 2-3 m floor line.
2. Run forward for about 2 seconds.
3. If it drifts left, increase `steering_trim` by `1..2`.
4. If it drifts right, decrease `steering_trim` by `1..2`.
5. Repeat 3 runs and use the average drift, not a single run.

Important observation:

- Encoder logs can look balanced while the robot still visually drifts.
- Real physical movement should win over encoder logs when tuning `steering_trim`.
- If encoder labels seem suspicious, lift the robot and stop one wheel by hand:
  - stopping the left wheel should reduce the `Left` count
  - stopping the right wheel should reduce the `Right` count

## Encoder Correction Behavior

`update_encoder_correction()` currently:

- measures encoder pulses for a short time window
- computes `error = left_count - right_count`
- ignores small differences with `threshold=2`
- computes a proportional target correction for larger errors
- smooths correction with `smoothing=0.35`
- limits correction with `max_correction=25`

This replaced the older behavior where correction accumulated indefinitely and could drift to values like `-20`, causing unstable PWM differences.

## Future Architecture Plan

The planned architecture is:

- Raspberry Pi:
  - high-level logic
  - camera/navigation/decision making
  - sends commands like forward, turn, stop
- STM32F407 Discovery:
  - low-level motor control
  - PWM generation
  - encoder counting
  - speed PID
  - course/heading PID
  - emergency stop and real-time mechanics

The STM32F407 Discovery board has an onboard MEMS 3-axis accelerometer, but not a full gyroscope suitable for heading control. For better straight driving, add an IMU module with a gyroscope, for example:

- MPU-6050
- MPU-9250
- ICM-20948

For straight driving, the important sensor is the gyroscope Z axis. Encoders measure wheel rotation; the gyroscope measures actual body rotation.

Best future control loop:

- encoders keep wheel speeds stable
- gyroscope keeps robot heading stable
- Raspberry Pi only sends high-level motion commands

## Communication Plan

When STM32 is added, use a simple command protocol between Raspberry Pi and STM32, likely over UART or I2C.

Example high-level commands:

```text
SET_SPEED left right
FORWARD speed
TURN angle speed
STOP
GET_STATUS
```

STM32 should return telemetry such as:

```text
left_encoder
right_encoder
heading
left_pwm
right_pwm
battery_voltage
fault_state
```

## Notes For Future Work

- Do not assume encoder balance means the robot moves straight.
- Keep motor safety behavior: always stop motors on exit.
- Prefer small calibration changes and test on the floor.
- If adding gyro support, calibrate gyro bias at startup while the robot is standing still.
