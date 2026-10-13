
import random
from datetime import datetime


def generate_sensor_reading():
    """Generate simulated temperature and vibration readings."""

    temperature = round(random.uniform(35.0, 75.0), 2)
    vibration = round(random.uniform(0.5, 4.0), 2)

    # Occasionally simulate abnormal machine behaviour.
    if random.random() < 0.15:
        temperature = round(random.uniform(85.0, 110.0), 2)
        vibration = round(random.uniform(5.0, 9.0), 2)

    reading = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "temperature": temperature,
        "vibration": vibration,
    }

    return reading


if __name__ == "__main__":
    for _ in range(5):
        print(generate_sensor_reading())
