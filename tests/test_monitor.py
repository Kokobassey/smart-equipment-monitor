
from src.monitor import analyze_reading


def create_reading(temperature, vibration):
    """Create a sample sensor reading for testing."""
    return {
        "timestamp": "2026-10-13T12:00:00",
        "temperature": temperature,
        "vibration": vibration,
    }


def test_normal_reading():
    reading = create_reading(50.0, 2.0)

    result = analyze_reading(reading)

    assert result["status"] == "NORMAL"
    assert result["alerts"] == []


def test_high_temperature_warning():
    reading = create_reading(90.0, 2.0)

    result = analyze_reading(reading)

    assert result["status"] == "WARNING"
    assert any("Temperature" in alert for alert in result["alerts"])


def test_high_vibration_warning():
    reading = create_reading(50.0, 6.0)

    result = analyze_reading(reading)

    assert result["status"] == "WARNING"
    assert any("Vibration" in alert for alert in result["alerts"])


def test_critical_temperature():
    reading = create_reading(105.0, 2.0)

    result = analyze_reading(reading)

    assert result["status"] == "CRITICAL"


def test_critical_vibration():
    reading = create_reading(50.0, 8.5)

    result = analyze_reading(reading)

    assert result["status"] == "CRITICAL"


def test_multiple_warnings():
    reading = create_reading(90.0, 6.0)

    result = analyze_reading(reading)

    assert result["status"] == "WARNING"
    assert len(result["alerts"]) == 2
