# Robot v1 — Autonomous Differential-Drive Robot (Raspberry Pi)

A two-wheeled differential-drive robot controlled by a Raspberry Pi 5 in **Python**.

The project is a practical robotics prototype for motor control, encoder feedback, ultrasonic obstacle sensing and addressable LEDs. It is also the first stage of a larger architecture that will later move real-time motor control to an STM32.

> **Project status:** 🚧 Work in progress.
>
> Current work focuses on finishing the Raspberry Pi prototype, validating obstacle detection and motor behaviour, cleaning the wiring, and preparing final photos/demo material.

---

## Highlights

- Two DC motors controlled through GPIO PWM and an H-bridge.
- Interrupt-driven wheel encoder measurement.
- Straight-line correction using encoder feedback.
- Fixed steering trim for compensation of mechanical left/right bias.
- Two HC-SR04 ultrasonic distance sensors.
- 12-pixel WS2812 / NeoPixel LED strip via SPI.
- Safe motor shutdown on program exit.
- Hardware functionality separated into reusable Python classes.

## Hardware

| Component | Details |
|---|---|
| Controller | Raspberry Pi 5 |
| Drive | 2 × DC motors via H-bridge |
| Odometry | 2 × single-channel wheel encoders |
| Distance sensing | 2 × HC-SR04 ultrasonic sensors |
| Lighting | 12 × WS2812 / NeoPixel LEDs |
| Chassis | Differential drive: two driven wheels + rear caster |

### GPIO pin map (BCM)

| Function | Pins |
|---|---|
| Left motor (forward/reverse) | GPIO 17, 27 |
| Right motor (forward/reverse) | GPIO 22, 23 |
| Left encoder | GPIO 24 |
| Right encoder | GPIO 25 |
| Left HC-SR04 (trig/echo) | GPIO 5, 6 |
| Right HC-SR04 (trig/echo) | GPIO 13, 19 |
| LED strip (SPI MOSI) | GPIO 10 |

All GPIO numbering uses **BCM** numbering.

## Project structure

| File | Responsibility |
|---|---|
| `my_robot.py` | Main control program and live telemetry |
| `motor.py` | Dual-motor PWM control and encoder-based correction |
| `encoder.py` | Interrupt-driven encoder pulse counting |
| `hc_sr04.py` | Ultrasonic distance measurement with timeout handling |
| `led_band.py` | WS2812 / NeoPixel LED control |
| `test_hc_sr04.py` | HC-SR04 test program |

## Motor control

The current control loop is:

`my_robot.py → motor.py → encoder.py`

The robot uses a base PWM value together with two independent corrections:

1. **Steering trim** compensates for a constant mechanical bias between the motors.
2. **Encoder correction** dynamically compensates for differences in measured wheel speed.

The resulting PWM commands are:

```text
left_pwm  = base_pwm + steering_trim + correction
right_pwm = base_pwm - steering_trim - correction
```

PWM output is clamped to the safe range `0..100`.

### Straight-line calibration

A typical calibration currently uses:

```python
base_pwm = 60
steering_trim = 5
```

A positive `steering_trim` increases left-motor PWM and decreases right-motor PWM.

Calibration is performed on the floor over repeated straight runs:

1. Run the robot for approximately 2 seconds on a straight 2–3 m path.
2. If it drifts left, increase `steering_trim` by about 1–2.
3. If it drifts right, decrease it by about 1–2.
4. Repeat several runs and evaluate the physical trajectory.

**Important:** similar encoder counts do not necessarily mean that the robot physically travels straight. Mechanical differences, wheel slip and motor condition can still cause drift. Floor behaviour is therefore used together with encoder telemetry.

## Encoder correction

`Motor.update_encoder_correction()` samples both encoders over a short measurement window and calculates:

```text
error = left_count - right_count
```

The current algorithm:

- ignores small errors using a dead-band (`threshold=2`);
- calculates a proportional target correction;
- smooths the transition toward the target (`smoothing=0.35`);
- limits correction to `±25`.

The correction is intentionally **smoothed rather than accumulated indefinitely**. An earlier accumulating approach could grow to large correction values and create unstable PWM differences.

The encoder implementation uses a GPIO falling-edge callback to count pulses.

## Ultrasonic sensors

Two HC-SR04 sensors are used for obstacle detection.

`HCSR04.get_distance()` includes timeout handling and returns `None` if a valid echo is not received, preventing the program from waiting indefinitely.

The current target demo behaviour is:

```text
Power on
   ↓
LED indicates ready
   ↓
Drive forward
   ↓
Measure distance
   ↓
Obstacle detected
   ↓
Stop motors
   ↓
LED indicates stop
```

## LED strip

A 12-pixel WS2812 / NeoPixel strip is controlled through SPI using `pi5neo` on `/dev/spidev0.0`.

It is used both for visual feedback and for simple LED test/animation patterns.

## Safety

Motor safety is kept explicit in the software:

- motor duty cycles are clamped to `0..100`;
- `KeyboardInterrupt` is the normal manual exit path;
- the main program stops the motors and releases GPIO resources in a `finally` block;
- ultrasonic measurement uses timeouts instead of blocking indefinitely.

Any future control code should preserve these behaviours.

## Running on Raspberry Pi

The code targets Raspberry Pi hardware and imports `RPi.GPIO` and `pi5neo`, so the hardware-dependent programs are intended to run directly on the Pi.

```bash
pip install RPi.GPIO pi5neo
python3 my_robot.py
```

Stop with **Ctrl+C**; the program should stop the motors and clean up GPIO.

## Current development

Before Robot v1 is considered finished, the current plan is to:

- complete and test ultrasonic obstacle detection;
- integrate LED status indication;
- verify the complete drive → detect obstacle → stop sequence;
- tidy the internal wiring and enclosure;
- make final project photos and a short demonstration video.

Robot v1 is intentionally kept as a Raspberry Pi/Python prototype.

## Future architecture — Robot v2

The planned next architecture separates high-level Linux software from real-time control.

### Raspberry Pi

Responsible for:

- high-level robot logic;
- camera processing;
- navigation and decision making;
- communication with the low-level controller.

### STM32F407 + FreeRTOS

Responsible for:

- PWM generation;
- encoder counting;
- motor speed control / PID;
- heading control;
- emergency-stop and other time-critical functions.

An external IMU with a gyroscope can later provide body-rotation feedback. Encoders measure wheel rotation, while the gyroscope can measure actual robot rotation around the Z axis.

The intended control concept is:

```text
Raspberry Pi
high-level commands
        ↓
STM32F407 + FreeRTOS
        ↓
speed / heading control
        ↓
motors + encoders + IMU
```

Possible communication between Raspberry Pi and STM32 is UART or I²C, using commands such as:

```text
SET_SPEED left right
FORWARD speed
TURN angle speed
STOP
GET_STATUS
```

Possible telemetry from STM32:

```text
left_encoder
right_encoder
heading
left_pwm
right_pwm
battery_voltage
fault_state
```

This split allows Linux to handle complex high-level tasks while the microcontroller handles deterministic real-time motor control.

---

*Robot v1 is an active Raspberry Pi/Python robotics prototype and portfolio project.*
