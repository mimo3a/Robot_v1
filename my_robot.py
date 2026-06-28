from motor import Motor

# Base motor power in percent. The correction value is adjusted at runtime
# to keep both encoder counts close to each other.
base_pwm = 60
correction = 0

motors = Motor()

try:
    motors.set_speed_forward(base_pwm, base_pwm)

    while True:
        encoder_data = motors.update_encoder_correction(base_pwm, correction)
        correction = encoder_data["correction"]

        print(
            "Left:", encoder_data["left_count"],
            "Right:", encoder_data["right_count"],
            "Error:", encoder_data["error"],
            "Correction:", correction,
            "PWM L:", encoder_data["left_pwm"],
            "PWM R:", encoder_data["right_pwm"]
        )

finally:
    # Always stop motors and release GPIO pins, even when the loop is interrupted.
    motors.stop()
    motors.cleanup()
