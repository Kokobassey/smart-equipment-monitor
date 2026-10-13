
def analyze_reading(reading):
    """
    Analyze sensor readings and determine equipment status.
    """

    temperature = reading["temperature"]
    vibration = reading["vibration"]

    alerts = []

    # Check temperature
    if temperature >= 100:
        alerts.append("CRITICAL: Temperature is extremely high.")
    elif temperature >= 85:
        alerts.append("WARNING: Temperature is too high.")

    # Check vibration
    if vibration >= 8:
        alerts.append("CRITICAL: Vibration is extremely high.")
    elif vibration >= 5:
        alerts.append("WARNING: Vibration is too high.")

    # Determine overall equipment status
    if any(alert.startswith("CRITICAL") for alert in alerts):
        status = "CRITICAL"
    elif alerts:
        status = "WARNING"
    else:
        status = "NORMAL"

    return {
        "status": status,
        "alerts": alerts,
        "temperature": temperature,
        "vibration": vibration,
        "timestamp": reading["timestamp"],
    }


if __name__ == "__main__":
    from sensor_simulator import generate_sensor_reading

    reading = generate_sensor_reading()
    result = analyze_reading(reading)

    print("Sensor Reading:", reading)
    print("Analysis Result:", result)
