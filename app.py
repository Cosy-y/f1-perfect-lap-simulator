
import streamlit as st
from data_loader import load_and_normalize_telemetry
from visualizer import plot_speed_comparison

# Page Configuration
st.set_page_config(page_title="F1 Telemetry Analyzer", page_icon="🏎️", layout="wide")

st.title("🏎️ F1 Telemetry & Analytics Dashboard")
st.write("Compare high-frequency speed traces between any two drivers using official FastF1 data.")
# app.py
import streamlit as st
from data_loader import load_and_normalize_telemetry
from visualizer import plot_speed_comparison
from track_map import plot_track_map

st.set_page_config(page_title="F1 Telemetry & Track Analyzer", page_icon="🏎️", layout="wide")

st.title("🏎️ F1 Telemetry & Circuit Position Dashboard")
st.write("Deep-dive into synchronized telemetry traces and spatial circuit positioning using FastF1.")

# --- Sidebar Inputs ---
st.sidebar.header("Session Selector")
year = st.sidebar.selectbox("Select Year", [2024, 2023, 2022], index=0)
gp = st.sidebar.text_input("Grand Prix", "Bahrain Grand Prix")
session_type = st.sidebar.selectbox("Session Type", ["Q", "R", "FP1", "FP2", "FP3"])

st.sidebar.subheader("Driver Comparison")
col1, col2 = st.sidebar.columns(2)
driver_1 = col1.text_input("Driver 1 Code", "VER")
driver_2 = col2.text_input("Driver 2 Code", "LEC")

if st.sidebar.button("Load Full Telemetry & Map"):
    with st.spinner("Fetching high-frequency telemetry and track geometry from FastF1..."):
        try:
            # 1. Load data and raw laps
            df, lap1, lap2 = load_and_normalize_telemetry(year, gp, session_type, driver_1, driver_2)
            
            # 2. Render Speed Trace Chart
            speed_fig = plot_speed_comparison(df, driver_1, driver_2, gp, year)
            st.plotly_chart(speed_fig, use_container_width=True)
            
            # 3. Render Track Map Spatial Comparison
            track_fig = plot_track_map(lap1, lap2, driver_1, driver_2)
            st.plotly_chart(track_fig, use_container_width=True)
            
            st.success("Telemetry and track maps successfully generated!")
            
        except Exception as e:
            st.error(f"Error loading session data: {e}")
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
