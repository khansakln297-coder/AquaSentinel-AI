# 🌊 AquaSentinel AI
> Autonomous Freshwater Bio-telemetry & Predictive Anomaly Engine for Urban Aquatic Ecosystems  
> *Developed for the OneAquaHealth IEEE Global Virtual Hackathon*

---

## 📌 Executive Summary
Urban freshwater bodies suffer from delayed contamination response due to discrete, manual sampling. **AquaSentinel AI** bridges this gap by providing an autonomous, continuous telemetry intelligence engine. It combines real-time hydrological bio-indicators (Dissolved Oxygen, pH, Turbidity, Conductivity) with unsupervised anomaly detection and a standardized Aquatic Health Index (AHI).

## 🚀 Key Architectural Capabilities
- **Multi-Variate Bio-Telemetry Pipeline:** Real-time continuous processing of primary freshwater metrics incorporating diurnal and circadian cycles.
- **Unsupervised Anomaly Isolation:** Uses an Isolation Forest machine learning engine to pinpoint contamination runoff, toxic shocks, and industrial discharges without requiring pre-labeled training data.
- **Aquatic Health Index (AHI):** Composite mathematical scoring (0–100) weighting Dissolved Oxygen, pH equilibrium, and Turbidity into actionable ecological alerts.
- **Actionable Decision Support:** Direct classification of ecosystem status into *Healthy/Stable*, *Ecosystem Stress*, and *Severe Contamination Alert*.

## 🛠️ Tech Stack
- **Core Engine:** Python 3.10+, NumPy, Pandas
- **Machine Learning:** Scikit-learn (Isolation Forest Anomaly Model)
- **Interactive Telemetry Interface:** Streamlit Framework
- **Dynamic Visualization:** Plotly Graph Objects & Express

## ⚙️ Local Setup & Execution
```bash
# Clone the repository
git clone [https://github.com/khansakln297-coder/AquaSentinel-AI.git](https://github.com/khansakln297-coder/AquaSentinel-AI.git)
cd AquaSentinel-AI

# Install dependencies
pip install -r requirements.txt

# Run the telemetry dashboard
streamlit run app.py

## 👥 Hackathon Submission
Built solo for the **OneAquaHealth IEEE Global Virtual Hackathon**.
