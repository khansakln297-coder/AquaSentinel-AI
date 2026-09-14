import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from engine import generate_telemetry_stream, calculate_aquatic_health_index, detect_anomalies

st.set_page_config(
    page_title="AquaSentinel AI | IEEE OneAquaHealth",
    page_icon="🌊",
    layout="wide"
)

st.title("🌊 AquaSentinel AI: Bio-Telemetry & Anomaly Intelligence")
st.markdown("**Autonomous Freshwater Ecosystem Monitoring & Contamination Early-Warning Engine**")

# Sidebar Controls
st.sidebar.header("⚙️ Telemetry Controls")
sample_count = st.sidebar.slider("Historical Telemetry Horizon (Hours)", min_value=50, max_value=500, value=250, step=25)
contamination = st.sidebar.slider("Anomaly Sensitivity", min_value=0.01, max_value=0.15, value=0.08, step=0.01)

# Generate & Process Telemetry
raw_data = generate_telemetry_stream(n_samples=sample_count)
scored_data = calculate_aquatic_health_index(raw_data)
processed_data, _ = detect_anomalies(scored_data, contamination_rate=contamination)

latest = processed_data.iloc[-1]
anomalies_total = (processed_data["is_anomaly"] == -1).sum()

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Current AHI Score", f"{latest['aquatic_health_index']}/100", latest["ecological_status"])
col2.metric("Dissolved Oxygen", f"{latest['dissolved_oxygen_mg_l']} mg/L")
col3.metric("Water pH", f"{latest['ph']}")
col4.metric("Active Contamination Flags", f"{anomalies_total}", delta_color="inverse")

st.divider()

# Charts Section
tab1, tab2, tab3 = st.tabs(["📊 Bio-Telemetry Multi-Stream", "🚨 AI Anomaly Isolation", "📋 Telemetry Audit Log"])

with tab1:
    fig_telemetry = px.line(
        processed_data, 
        x="timestamp", 
        y=["dissolved_oxygen_mg_l", "ph", "turbidity_ntu"],
        title="Urban Freshwater Bio-Indicators (Circadian Flow & Spikes)",
        labels={"value": "Measured Value", "variable": "Sensor Parameter"}
    )
    st.plotly_chart(fig_telemetry, use_container_width=True)

with tab2:
    fig_anomaly = px.scatter(
        processed_data,
        x="dissolved_oxygen_mg_l",
        y="ph",
        color="anomaly_flag",
        size="turbidity_ntu",
        hover_data=["timestamp", "conductivity_us_cm"],
        color_discrete_map={"Normal": "#00CC96", "CRITICAL ANOMALY": "#EF553B"},
        title="Isolation Forest Multi-Variate Anomaly Boundary"
    )
    st.plotly_chart(fig_anomaly, use_container_width=True)

with tab3:
    st.dataframe(
        processed_data[["timestamp", "aquatic_health_index", "ecological_status", "ph", "dissolved_oxygen_mg_l", "turbidity_ntu", "anomaly_flag"]].tail(50),
        use_container_width=True
    )

st.sidebar.info("Developed for OneAquaHealth IEEE Global Hackathon | Team AquaSentinel")

