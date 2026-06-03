# streaming/producer.py

import requests
import random
import time
import json
import os
from datetime import datetime

# =====================================================
# API URL
# =====================================================

API_URL = "http://127.0.0.1:8000/predict"

# =====================================================
# CREATE STREAMING FOLDER
# =====================================================

os.makedirs(
    "streaming_logs",
    exist_ok=True
)

# =====================================================
# START SIMULATION
# =====================================================

print("\n🏭 FactoryMind AI Sensor Simulator Started...\n")

while True:

    try:

        # =================================================
        # SENSOR DATA GENERATION
        # =================================================

        data = {

            "Type":
            random.randint(0,2),

            "Air_temperature_K":
            round(random.uniform(295,320),2),

            "Process_temperature_K":
            round(random.uniform(305,350),2),

            "Rotational_speed_rpm":
            round(random.uniform(1200,2800),2),

            "Torque_Nm":
            round(random.uniform(10,90),2),

            "Tool_wear_min":
            round(random.uniform(0,250),2)
        }

        # =================================================
        # FEATURE ENGINEERING
        # =================================================

        data["temp_diff"] = (
            data["Process_temperature_K"] -
            data["Air_temperature_K"]
        )

        data["wear_ratio"] = (
            data["Tool_wear_min"] /
            data["Rotational_speed_rpm"]
        )

        data["torque_stress"] = (
            data["Torque_Nm"] *
            data["Rotational_speed_rpm"]
        )

        data["thermal_stress"] = (
            data["temp_diff"] *
            data["Torque_Nm"]
        )

        data["load_index"] = (
            data["Torque_Nm"] /
            data["Rotational_speed_rpm"]
        )

        # =================================================
        # SEND DATA TO FASTAPI
        # =================================================

        response = requests.post(
            API_URL,
            json=data
        )

        result = response.json()

        # =================================================
        # LIVE STATUS
        # =================================================

        print("\n" + "="*70)

        print(
            f"\n🕒 Time: "
            f"{datetime.now().strftime('%H:%M:%S')}"
        )

        print("\n📡 LIVE SENSOR DATA:\n")

        print(json.dumps(
            data,
            indent=4
        ))

        print("\n🤖 AI PREDICTION:\n")

        print(json.dumps(
            result,
            indent=4
        ))

        # =================================================
        # ALERTS
        # =================================================

        probability = result["Failure_Probability"]

        if probability >= 0.80:

            print(
                "\n🚨 CRITICAL ALERT: "
                "Machine Failure Risk HIGH"
            )

        elif probability >= 0.50:

            print(
                "\n⚠ WARNING: "
                "Machine Health Degrading"
            )

        else:

            print(
                "\n✅ Machine Operating Normally"
            )

        # =================================================
        # SAVE LOGS
        # =================================================

        log_data = {

            "timestamp":
            str(datetime.now()),

            "sensor_data":
            data,

            "prediction":
            result
        }

        with open(
            "streaming_logs/live_logs.json",
            "w"
        ) as f:

            json.dump(
                log_data,
                f,
                indent=4
            )

        # =================================================
        # WAIT
        # =================================================

        time.sleep(3)

    except Exception as e:

        print(
            f"\n❌ ERROR: {e}"
        )

        print(
            "\n⚠ Make sure FastAPI server is running..."
        )

        time.sleep(5)