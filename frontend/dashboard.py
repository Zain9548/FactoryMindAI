
# frontend/dashboard.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="FactoryMind AI",

    page_icon="🏭",

    layout="wide"
)
st_autorefresh(
    interval=15000,
    key="factorymind_refresh"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1,h2,h3,h4 {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.title("🏭 FactoryMind AI")

st.markdown("""
### 🚀 Real-Time Industrial Predictive Maintenance Platform
""")

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# =====================================================
# API URL
# =====================================================

API_URL = "http://127.0.0.1:8000/live"

# =====================================================
# FETCH LIVE DATA
# =====================================================

try:

    response = requests.get(API_URL)

    result = response.json()

    sensor = result["sensor_data"]

    probability = result["Failure_Probability"]

    anomaly = result["Anomaly_Result"]

    status = result["Machine_Status"]

    timestamp = result["timestamp"]

    # =================================================
    # SIDEBAR
    # =================================================

    st.sidebar.title("🏭 FactoryMind AI")

    st.sidebar.success(
        "✔ AI Monitoring Active"
    )

    st.sidebar.info(
        f"🕒 {timestamp}"
    )

    st.sidebar.markdown("---")

    st.sidebar.subheader(
        "📡 Live Sensors"
    )

    st.sidebar.write(
        f"🌡 Air Temp: {sensor['Air_temperature_K']} K"
    )

    st.sidebar.write(
        f"🔥 Process Temp: {sensor['Process_temperature_K']} K"
    )

    st.sidebar.write(
        f"⚙ RPM: {sensor['Rotational_speed_rpm']}"
    )

    st.sidebar.write(
        f"🔩 Torque: {sensor['Torque_Nm']} Nm"
    )

    st.sidebar.write(
        f"🛠 Tool Wear: {sensor['Tool_wear_min']} min"
    )

    # =================================================
    # KPI METRICS
    # =================================================

    st.subheader("📊 Industrial KPIs")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Failure Probability",
        f"{probability*100:.2f}%"
    )

    col2.metric(
        "RPM",
        f"{sensor['Rotational_speed_rpm']}"
    )

    col3.metric(
        "Torque",
        f"{sensor['Torque_Nm']} Nm"
    )

    col4.metric(
        "Tool Wear",
        f"{sensor['Tool_wear_min']} min"
    )

    # =================================================
    # MACHINE STATUS
    # =================================================

    st.subheader("🏭 Machine Health Status")

    if status == "CRITICAL":

        st.error(
            "🚨 CRITICAL FAILURE RISK DETECTED"
        )

    elif status == "WARNING":

        st.warning(
            "⚠ MACHINE HEALTH DEGRADING"
        )

    else:

        st.success(
            "✅ MACHINE OPERATING NORMALLY"
        )

    # =================================================
    # ANOMALY STATUS
    # =================================================

    if anomaly == -1:

        st.error(
            "🚨 ANOMALY DETECTED"
        )

    else:

        st.info(
            "✔ NO ANOMALY DETECTED"
        )

    # =================================================
    # FAILURE RISK GAUGE
    # =================================================

    st.subheader("📈 Failure Risk Gauge")

    gauge = go.Figure(go.Indicator(

        mode="gauge+number",

        value=probability * 100,

        title={
            'text': "Failure Risk %"
        },

        gauge={

            'axis': {
                'range': [0, 100]
            },

            'bar': {
                'color': "red"
            },

            'steps': [

                {
                    'range': [0, 50],
                    'color': "green"
                },

                {
                    'range': [50, 80],
                    'color': "yellow"
                },

                {
                    'range': [80, 100],
                    'color': "red"
                }
            ]
        }
    ))

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    # =================================================
    # SENSOR ANALYTICS
    # =================================================

    st.subheader("📡 Sensor Analytics")

    sensor_df = pd.DataFrame({

        "Sensor": [

            "Air Temp",
            "Process Temp",
            "Torque",
            "RPM",
            "Tool Wear"
        ],

        "Value": [

            sensor["Air_temperature_K"],

            sensor["Process_temperature_K"],

            sensor["Torque_Nm"],

            sensor["Rotational_speed_rpm"],

            sensor["Tool_wear_min"]
        ]
    })

    fig = px.bar(

        sensor_df,

        x="Sensor",

        y="Value",

        text="Value",

        title="Industrial Sensor Monitoring"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =================================================
    # LIVE TABLE
    # =================================================

    st.subheader("📋 Live Sensor Data")

    st.dataframe(
        sensor_df,
        use_container_width=True
    )

    # =================================================
    # AI COPILOT CHAT
    # =================================================

    st.subheader("🤖 FactoryMind AI Copilot")

    # =============================================
    # SHOW CHAT HISTORY
    # =============================================

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # =============================================
    # CHAT INPUT
    # =============================================

    prompt = st.chat_input(
        "Ask industrial maintenance question..."
    )

    # =============================================
    # NEW QUESTION
    # =============================================

    if prompt:

        # =========================================
        # SAVE USER MESSAGE
        # =========================================

        st.session_state.messages.append({

            "role": "user",

            "content": prompt
        })

        # =========================================
        # SHOW USER MESSAGE
        # =========================================

        with st.chat_message("user"):

            st.markdown(prompt)

        # =========================================
        # CALL ask.py API
        # =========================================

        try:

            with st.spinner(
                "FactoryMind AI Thinking..."
            ):

                rag_response = requests.post(

                    "http://127.0.0.1:9000/ask",

                    json={
                        "question": prompt
                    },

                    timeout=120
                )

                rag_result = rag_response.json()

                print(rag_result)

                answer = rag_result["answer"]

        except Exception as e:

            answer = f"❌ Error: {e}"

        # =========================================
        # SAVE ASSISTANT MESSAGE
        # =========================================

        st.session_state.messages.append({

            "role": "assistant",

            "content": answer
        })

        # =========================================
        # SHOW ASSISTANT MESSAGE
        # =========================================

        with st.chat_message("assistant"):

            st.markdown(answer)

    # =================================================
    # RAW AI OUTPUT
    # =================================================

    st.subheader("🤖 AI Prediction Output")

    st.json(result)

    # =================================================
    # FOOTER
    # =================================================

    st.markdown("---")

    st.markdown(
        "### ⚡ FactoryMind AI — Industry 4.0 Predictive Maintenance Platform"
    )

except Exception as e:

    st.error(
        f"❌ Error: {e}"
    )

    st.warning(
        "⚠ Make sure backend and ask.py API are running."
    )

