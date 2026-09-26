import time

from motor import Motor
from hc_sr04 import HCSR04
from led_band import LedBand

# Drive calibration.
base_pwm = 60
correction = 0
steering_trim = 5

# Stop when either ultrasonic sensor sees an obstacle at or below this distance.
STOP_DISTANCE_CM = 30

motors = Motor()
sensors = HCSR04()
leds = LedBand()


def obstacle_detected(distances):
    """Return True if either valid sensor reading is inside the stop distance."""
    return any(
        distance is not None and distance <= STOP_DISTANCE_CM
        for distance in distances.values()
    )


try:
    # Green means the robot is ready and moving normally.
    leds.green()
    motors.set_speed_forward(
        base_pwm + steering_trim,
        base_pwm - steering_trim
    )

    while True:
        distances = sensors.get_distances()

        print(
            "Distance L:", distances["left"],
            "Distance R:", distances["right"]
        )

        if obstacle_detected(distances):
            motors.stop()
            leds.red()
            print("Obstacle detected - motors stopped.")

            # Keep the stop state visible until the user ends the program.
            # The motors remain stopped and the status LED stays red.
            while True:
                time.sleep(0.1)

        encoder_data = motors.update_encoder_correction(
            base_pwm,
            correction,
            trim=steering_trim
        )
        correction = encoder_data["correction"]

        print(
            "Encoder L:", encoder_data["left_count"],
            "Encoder R:", encoder_data["right_count"],
            "Error:", encoder_data["error"],
            "Correction:", round(correction, 1),
            "PWM L:", encoder_data["left_pwm"],
            "PWM R:", encoder_data["right_pwm"]
        )

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    motors.stop()
    leds.off()
    motors.cleanup()
