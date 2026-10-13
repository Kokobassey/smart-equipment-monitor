import sqlite3

import pandas as pd
import streamlit as st

from src.database import DATABASE_PATH, initialize_database, save_reading
from src.sensor_simulator import generate_sensor_reading
from src.monitor import analyze_reading


st.set_page_config(
    page_title="Smart Equipment Monitor",
    page_icon="⚙️",
    layout="wide",
)

initialize_database()


def load_readings():
    with sqlite3.connect(DATABASE_PATH) as connection:
        return pd.read_sql_query(
            """
            SELECT timestamp, temperature, vibration, status, alerts
            FROM sensor_readings
            ORDER BY id DESC
            LIMIT 200
            """,
            connection,
        )


st.title("⚙️ Smart Equipment Monitoring System")
st.caption("Equipment condition monitoring using simulated sensor data")


st.sidebar.header("Monitoring Controls")

st.sidebar.info(
    "This project uses simulated readings. "
    "It is not connected to physical equipment."
)

auto_monitor = st.sidebar.toggle(
    "Enable Automatic Monitoring",
    value=False,
)

interval = st.sidebar.slider(
    "Reading Interval (seconds)",
    min_value=5,
    max_value=60,
    value=10,
    step=5,
    disabled=not auto_monitor,
)

if st.sidebar.button("Generate New Reading", type="primary"):
    reading = generate_sensor_reading()
    analysis = analyze_reading(reading)
    save_reading(reading, analysis)
    st.sidebar.success("Reading generated and saved!")

if st.sidebar.button("Refresh Dashboard"):
    st.rerun()


@st.fragment(run_every=interval if auto_monitor else None)
def display_dashboard():
    # Generate a new reading on each automatic refresh.
    if auto_monitor:
        reading = generate_sensor_reading()
        analysis = analyze_reading(reading)
        save_reading(reading, analysis)

    df = load_readings()

    if df.empty:
        st.info(
            "No readings yet. Click Generate New Reading "
            "in the sidebar."
        )
        return

    latest = df.iloc[0]

    st.subheader("Current Equipment Status")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Temperature", f"{latest['temperature']:.2f} °C")
    col2.metric("Vibration", f"{latest['vibration']:.2f}")
    col3.metric("Equipment Status", latest["status"])
    col4.metric("Recorded Readings", len(df))

    if latest["status"] == "CRITICAL":
        st.error(
            "CRITICAL: The latest reading exceeds a critical threshold."
        )
    elif latest["status"] == "WARNING":
        st.warning(
            "WARNING: The latest reading exceeds a warning threshold."
        )
    else:
        st.success(
            "NORMAL: The latest reading is within configured limits."
        )

    chart_df = df.copy()
    chart_df["timestamp"] = pd.to_datetime(chart_df["timestamp"])
    chart_df = chart_df.sort_values("timestamp").set_index("timestamp")

    st.subheader("Sensor History")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("#### Temperature (°C)")
        st.line_chart(chart_df[["temperature"]])

    with chart_col2:
        st.markdown("#### Vibration")
        st.line_chart(chart_df[["vibration"]])

    st.subheader("Recent Alerts")

    alerts_df = df[df["status"].isin(["WARNING", "CRITICAL"])]

    if alerts_df.empty:
        st.write(
            "No warning or critical readings in the recorded history."
        )
    else:
        st.dataframe(
            alerts_df[
                [
                    "timestamp",
                    "temperature",
                    "vibration",
                    "status",
                    "alerts",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    st.subheader("Recent Sensor Readings")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="Download Sensor History as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="sensor_readings.csv",
        mime="text/csv",
    )

    st.caption(
        "Thresholds are illustrative settings, not universal "
        "industrial safety limits."
    )


display_dashboard()