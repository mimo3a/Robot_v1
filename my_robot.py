from motor import Motor

# Base motor power in percent. The correction value is adjusted at runtime
# to keep both encoder counts close to each other.
base_pwm = 60
correction = 0

# Steering trim calibration:
# 1. Put the robot on a straight 2-3 m floor line.
# 2. Run it forward for about 2 seconds.
# 3. If it drifts left, increase steering_trim by 1-2.
# 4. If it drifts right, decrease steering_trim by 1-2.
# Positive trim gives more PWM to the left motor and less to the right motor.
# Example: base_pwm=60 and steering_trim=5 gives left=65, right=55.
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
