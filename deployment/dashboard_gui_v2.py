from oled_display import show_result
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from sensor_reader_v2 import get_all_sensors, get_rssi
from feature_extractor_v2 import extract_features
from ai_engine_v2 import predict_object

# -------------------------
# Auto Refresh
# -------------------------
st_autorefresh(interval=1000, key="refresh")

st.set_page_config(
    page_title="Airport AI Threat Detection",
    page_icon="🛫",
    layout="wide"
)

st.title("🛫 Airport AI Threat Detection System")

# -------------------------
# Read Sensors
# -------------------------

sensors = get_all_sensors()
features = extract_features(sensors, get_rssi())

prediction, confidence = predict_object(features)

# -------------------------
# Threat Level
# -------------------------

prediction = prediction.lower()

if prediction == "unknown":
    risk = "UNKNOWN"

elif prediction in ["knife", "scissors", "screwdriver"]:
    risk = "THREAT"

elif prediction in ["keys", "battery", "usb", "usb_adapter"]:
    risk = "SUSPICIOUS"

elif prediction in ["empty", "fork", "spoon"]:
    risk = "SAFE"

else:
    risk = "UNKNOWN"

# ALWAYS UPDATE OLED
show_result(prediction, risk)
# -------------------------
# Top Cards
# -------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Detected Object", prediction.upper())

with c2:
    st.metric("Threat Level", risk)

with c3:
    st.metric("Confidence", f"{confidence:.1f}%")

st.divider()

# -------------------------
# Sensor Cards
# -------------------------

st.subheader("Live Sensor Readings")

cols = st.columns(4)

for i in range(4):

    mag = sensors[f"sensor{i+1}"]["magnitude"]

    with cols[i]:

        st.metric(
            f"Sensor {i+1}",
            f"{mag:.1f}"
        )

        st.progress(min(mag/4000,1.0))

st.divider()

# -------------------------
# Heat Map
# -------------------------

st.subheader("Magnetic Heat Map")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Sensor 1",
        f"{sensors['sensor1']['magnitude']:.1f}"
    )

    st.progress(min(sensors["sensor1"]["magnitude"]/4000,1.0))

    st.metric(
        "Sensor 3",
        f"{sensors['sensor3']['magnitude']:.1f}"
    )

    st.progress(min(sensors["sensor3"]["magnitude"]/4000,1.0))

with col2:

    st.metric(
        "Sensor 2",
        f"{sensors['sensor2']['magnitude']:.1f}"
    )

    st.progress(min(sensors["sensor2"]["magnitude"]/4000,1.0))

    st.metric(
        "Sensor 4",
        f"{sensors['sensor4']['magnitude']:.1f}"
    )

    st.progress(min(sensors["sensor4"]["magnitude"]/4000,1.0))

st.divider()

st.write("RSSI:", get_rssi())
