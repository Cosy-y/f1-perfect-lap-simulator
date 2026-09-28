# app.py
import streamlit as st
from data_loader import load_and_normalize_telemetry
from visualizer import plot_speed_comparison

# Page Configuration
st.set_page_config(page_title="F1 Telemetry Analyzer", page_icon="🏎️", layout="wide")

st.title("🏎️ F1 Telemetry & Analytics Dashboard")
st.write("Compare high-frequency speed traces between any two drivers using official FastF1 data.")

# --- Sidebar Configuration for User Inputs ---
st.sidebar.header("Session Selector")

year = st.sidebar.selectbox("Select Year", [2024, 2023, 2022], index=0)
gp = st.sidebar.text_input("Grand Prix", "Monza")
session_type = st.sidebar.selectbox("Session Type", ["Q", "R", "FP1", "FP2", "FP3"])

st.sidebar.subheader("Driver Comparison")
col1, col2 = st.sidebar.columns(2)
driver_1 = col1.text_input("Driver 1 Code", "VER")
driver_2 = col2.text_input("Driver 2 Code", "LEC")

# Trigger button to fetch data and render app
if st.sidebar.button("Load Telemetry"):
    with st.spinner("Fetching data from FastF1 servers... Please wait."):
        try:
            # 1. Call the data loader function
            df, lap1, lap2 = load_and_normalize_telemetry(year, gp, session_type, driver_1, driver_2)
            
            # 2. Call the visualizer function
            fig = plot_speed_comparison(df, driver_1, driver_2, gp, year)
            
            # 3. Render the interactive Plotly chart inside Streamlit
            st.plotly_chart(fig, use_container_width=True)
            st.success("Telemetry trace loaded successfully!")
            
        except Exception as e:
            st.error(f"Failed to load session data. Error: {e}")
