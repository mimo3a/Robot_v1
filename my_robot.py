from motor import Motor

# Base motor power in percent. The correction value is adjusted at runtime
# to keep both encoder counts close to each other.
base_pwm = 60
correction = 0

# Positive trim steers the robot right. Increase this if it still pulls left;
# reduce it if the robot starts pulling right.
steering_trim = 5

motors = Motor()

try:
    motors.set_speed_forward(base_pwm + steering_trim, base_pwm - steering_trim)

    while True:
        encoder_data = motors.update_encoder_correction(
            base_pwm,
            correction,
            trim=steering_trim
        )
        correction = encoder_data["correction"]

        print(
            "Left:", encoder_data["left_count"],
            "Right:", encoder_data["right_count"],
            "Error:", encoder_data["error"],
            "Correction:", round(correction, 1),
            "PWM L:", encoder_data["left_pwm"],
            "PWM R:", encoder_data["right_pwm"]
        )

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    # Always stop motors and release GPIO pins, even when the loop is interrupted.
    motors.stop()
    motors.cleanup()
