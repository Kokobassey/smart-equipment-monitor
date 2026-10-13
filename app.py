
import time

from src.sensor_simulator import generate_sensor_reading
from src.monitor import analyze_reading
from src.database import initialize_database, save_reading


def run_monitoring_cycle():
    """Generate, analyze, save, and display one sensor reading."""

    reading = generate_sensor_reading()
    analysis = analyze_reading(reading)

    save_reading(reading, analysis)

    print("\n" + "=" * 45)
    print("SMART EQUIPMENT MONITORING SYSTEM")
    print("=" * 45)
    print(f"Timestamp:   {reading['timestamp']}")
    print(f"Temperature: {reading['temperature']} °C")
    print(f"Vibration:   {reading['vibration']}")
    print(f"Status:      {analysis['status']}")

    if analysis["alerts"]:
        for alert in analysis["alerts"]:
            print(f"ALERT: {alert}")
    else:
        print("Alerts:      None")

    print("Reading saved to database.")


def main():
    initialize_database()

    print("Equipment monitoring started.")
    print("Press Ctrl+C to stop monitoring.")

    try:
        while True:
            run_monitoring_cycle()
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
