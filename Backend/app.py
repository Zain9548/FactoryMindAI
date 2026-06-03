# backend/app.py

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import json
import os
from datetime import datetime

# =====================================================
# LOAD MODELS
# =====================================================

failure_model = joblib.load(
    "../Backend/models/failure_model1.pkl"
)

anomaly_model = joblib.load(
    "../Backend/models/anomaly_model.pkl"
)

# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="FactoryMind AI API",
    description="Industrial Predictive Maintenance Platform",
    version="2.0"
)

# =====================================================
# INPUT SCHEMA
# =====================================================

class MachineData(BaseModel):

    Type: int

    Air_temperature_K: float

    Process_temperature_K: float

    Rotational_speed_rpm: float

    Torque_Nm: float

    Tool_wear_min: float

    temp_diff: float

    wear_ratio: float

    torque_stress: float

    thermal_stress: float

    load_index: float

# =====================================================
# HOME ROUTE
# =====================================================

@app.get("/")
def home():

    return {
        "message": "FactoryMind AI Running Successfully"
    }

# =====================================================
# HEALTH ROUTE
# =====================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": True,
        "anomaly_model_loaded": True
    }

# =====================================================
# FAILURE PREDICTION
# =====================================================

@app.post("/predict")
def predict(data: MachineData):

    values = [[
        data.Type,
        data.Air_temperature_K,
        data.Process_temperature_K,
        data.Rotational_speed_rpm,
        data.Torque_Nm,
        data.Tool_wear_min,
        data.temp_diff,
        data.wear_ratio,
        data.torque_stress,
        data.thermal_stress,
        data.load_index
    ]]

    # =========================================
    # FAILURE PREDICTION
    # =========================================

    prediction = failure_model.predict(values)[0]

    probability = failure_model.predict_proba(
        values
    )[0][1]

    # =========================================
    # ANOMALY DETECTION
    # =========================================

    anomaly = anomaly_model.predict(values)[0]

    # =========================================
    # MACHINE STATUS
    # =========================================

    if probability >= 0.80:

        machine_status = "CRITICAL"

    elif probability >= 0.50:

        machine_status = "WARNING"

    else:

        machine_status = "HEALTHY"

    # =========================================
    # RESULT JSON
    # =========================================

    result = {

        "timestamp":
        str(datetime.now()),

        "Machine_Failure":
        int(prediction),

        "Failure_Probability":
        round(float(probability), 4),

        "Anomaly_Result":
        int(anomaly),

        "Machine_Status":
        machine_status,

        "sensor_data": {

            "Type":
            data.Type,

            "Air_temperature_K":
            data.Air_temperature_K,

            "Process_temperature_K":
            data.Process_temperature_K,

            "Rotational_speed_rpm":
            data.Rotational_speed_rpm,

            "Torque_Nm":
            data.Torque_Nm,

            "Tool_wear_min":
            data.Tool_wear_min
        }
    }

    # =========================================
    # SAVE LIVE DATA
    # =========================================

    os.makedirs(
        "../streaming",
        exist_ok=True
    )

    with open(
        "../streaming/latest_data.json",
        "w"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )

    return result

# =====================================================
# ANOMALY API
# =====================================================

@app.post("/anomaly")
def anomaly(data: MachineData):

    values = [[
        data.Type,
        data.Air_temperature_K,
        data.Process_temperature_K,
        data.Rotational_speed_rpm,
        data.Torque_Nm,
        data.Tool_wear_min,
        data.temp_diff,
        data.wear_ratio,
        data.torque_stress,
        data.thermal_stress,
        data.load_index
    ]]

    result = anomaly_model.predict(values)[0]

    return {
        "Anomaly_Result": int(result)
    }

# =====================================================
# LIVE DATA API
# =====================================================

@app.get("/live")
def live_data():

    file_path = "../streaming/latest_data.json"

    if os.path.exists(file_path):

        with open(file_path, "r") as f:

            data = json.load(f)

        return data

    return {
        "message": "No live data available"
    }