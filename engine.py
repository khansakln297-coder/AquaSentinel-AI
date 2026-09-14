import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

def generate_telemetry_stream(n_samples=250):
    """
    Simulates real-world urban freshwater telemetry data
    incorporating circadian cycles and intermittent contamination events.
    """
    np.random.seed(42)
    timestamps = pd.date_range(start="2026-09-01", periods=n_samples, freq="h")
    
    # Baseline ecological metrics for fresh water
    base_temp = 18.0 + 4.0 * np.sin(np.linspace(0, 8 * np.pi, n_samples)) + np.random.normal(0, 0.4, n_samples)
    base_ph = 7.3 + 0.3 * np.sin(np.linspace(0, 4 * np.pi, n_samples)) + np.random.normal(0, 0.15, n_samples)
    base_do = 8.5 - 0.15 * (base_temp - 18.0) + np.random.normal(0, 0.2, n_samples)
    base_turbidity = 4.0 + np.random.exponential(1.2, n_samples)
    base_conductivity = 320.0 + np.random.normal(0, 15.0, n_samples)

    # Inject realistic contamination/run-off incidents
    # Incident 1: Industrial acid/effluent discharge at step 80 to 92
    base_ph[80:92] -= 2.2
    base_conductivity[80:92] += 280.0
    base_do[80:92] -= 3.5

    # Incident 2: Urban sediment runoff / turbidity spike at step 170 to 182
    base_turbidity[170:182] += 28.0
    base_do[170:182] -= 2.1

    df = pd.DataFrame({
        "timestamp": timestamps,
        "temperature_c": np.round(base_temp, 2),
        "ph": np.round(base_ph, 2),
        "dissolved_oxygen_mg_l": np.round(np.clip(base_do, 0.5, 14.0), 2),
        "turbidity_ntu": np.round(base_turbidity, 2),
        "conductivity_us_cm": np.round(base_conductivity, 2)
    })
    return df

def calculate_aquatic_health_index(df):
    """
    Calculates the normalized Aquatic Health Index (AHI: 0 to 100).
    Higher index indicates pristine aquatic ecosystem balance.
    """
    ph_score = np.where((df["ph"] >= 6.5) & (df["ph"] <= 8.5), 100, 
                        np.maximum(0, 100 - np.abs(df["ph"] - 7.5) * 40))
    do_score = np.clip((df["dissolved_oxygen_mg_l"] / 8.0) * 100, 0, 100)
    turbidity_score = np.clip(100 - (df["turbidity_ntu"] * 3.0), 0, 100)
    
    ahi = (0.35 * do_score) + (0.35 * ph_score) + (0.30 * turbidity_score)
    df["aquatic_health_index"] = np.round(ahi, 1)
    
    conditions = [
        (df["aquatic_health_index"] >= 80),
        (df["aquatic_health_index"] >= 55) & (df["aquatic_health_index"] < 80),
        (df["aquatic_health_index"] < 55)
    ]
    choices = ["Healthy / Stable", "Ecosystem Stress", "Severe Contamination Alert"]
    df["ecological_status"] = np.select(conditions, choices, default="Unknown")
    return df

def detect_anomalies(df, contamination_rate=0.08):
    """
    Trains an Isolation Forest to identify multi-variate bio-telemetry anomalies.
    """
    features = ["temperature_c", "ph", "dissolved_oxygen_mg_l", "turbidity_ntu", "conductivity_us_cm"]
    model = IsolationForest(contamination=contamination_rate, random_state=42)
    df["is_anomaly"] = model.fit_predict(df[features])
    df["anomaly_flag"] = df["is_anomaly"].apply(lambda x: "CRITICAL ANOMALY" if x == -1 else "Normal")
    return df, model
  
