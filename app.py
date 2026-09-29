# app.py
import streamlit as st
import plotly.graph_objects as go
from data_loader import load_replay_telemetry

st.set_page_config(page_title="F1 Interactive Session Replay", page_icon="🏎️", layout="wide")

st.title("🏎️ F1 Interactive Lap Replay & Telemetry Inspector")
st.write("Scrub through the fastest lap to analyze live track positioning and speed differentials side-by-side.")

# --- Sidebar Inputs ---
st.sidebar.header("Session Selector")
year = st.sidebar.selectbox("Select Year", [2024, 2023, 2022], index=0, key="replay_year")
gp = st.sidebar.text_input("Grand Prix", "Bahrain Grand Prix", key="replay_gp")
session_type = st.sidebar.selectbox("Session Type", ["Q", "R", "FP1", "FP2", "FP3"], key="replay_session")

st.sidebar.subheader("Driver Comparison")
col1, col2 = st.sidebar.columns(2)
driver_1 = col1.text_input("Driver 1", "VER", key="replay_d1")
driver_2 = col2.text_input("Driver 2", "LEC", key="replay_d2")

# Load button
load_clicked = st.sidebar.button("Initialize Replay Session", key="init_replay")

if "replay_data" not in st.session_state or load_clicked:
    with st.spinner("Fetching high-frequency telemetry and track geometry..."):
        try:
            df, lap1, lap2, session = load_replay_telemetry(year, gp, session_type, driver_1, driver_2)
            st.session_state["replay_df"] = df
            st.session_state["d1"] = driver_1
            st.session_state["d2"] = driver_2
            st.success("Replay session initialized successfully!")
        except Exception as e:
            st.error(f"Initialization error: {e}")

# If data is loaded, render the interactive replay controls
if "replay_df" in st.session_state:
    df = st.session_state["replay_df"]
    d1 = st.session_state["d1"]
    d2 = st.session_state["d2"]

    max_dist = float(df['Distance'].max())
    
    st.divider()
    st.subheader("📍 Lap Replay Scrubber")
    
    # Interactive Slider acting as the timeline scrubber
    current_distance = st.slider(
        "Drag to scrub through lap distance (meters):", 
        min_value=0.0, 
        max_value=max_dist, 
        value=0.0, 
        step=10.0
    )

    # Find the row closest to the slider position
    current_row = df.iloc[(df['Distance'] - current_distance).abs().argsort()[:1]].iloc[0]

    # Display Live Metrics at current distance point
    m1, m2, m3 = st.columns(3)
    m1.metric("Distance into Lap", f"{current_row['Distance']:.1f} m")
    m2.metric(f"{d1} Speed", f"{current_row[f'{d1}_Speed']:.1f} km/h")
    m3.metric(f"{d2} Speed", f"{current_row[f'{d2}_Speed']:.1f} km/h")

    # --- Layout for Visualizations ---
    col_map, col_chart = st.columns(2)

    with col_map:
        st.markdown("### 🗺️ Live Track Position Replay")
        # Build interactive map with circuit outline + current car dots
        fig_map = go.Figure()

        # Faint background circuit outlines
        fig_map.add_trace(go.Scatter(x=df[f'{d1}_X'], y=df[f'{d1}_Y'], mode='lines', name=f'{d1} Line', line=dict(color='gray', width=2), hoverinfo='skip'))
        
        # Current active marker positions for both drivers
        fig_map.add_trace(go.Scatter(
            x=[current_row[f'{d1}_X']], y=[current_row[f'{d1}_Y']],
            mode='markers', name=f'{d1} Position',
            marker=dict(size=14, color='cyan')
        ))
        fig_map.add_trace(go.Scatter(
            x=[current_row[f'{d2}_X']], y=[current_row[f'{d2}_Y']],
            mode='markers', name=f'{d2} Position',
            marker=dict(size=14, color='orange')
        ))

        fig_map.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            template="plotly_dark",
            height=450,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_chart:
        st.markdown("### 📈 Synchronized Speed Trace")
        # Build Speed Trace with a vertical indicator line showing current scrubber location
        fig_speed = go.Figure()

        fig_speed.add_trace(go.Scatter(x=df['Distance'], y=df[f'{d1}_Speed'], mode='lines', name=f'{d1}', line=dict(color='cyan')))
        fig_speed.add_trace(go.Scatter(x=df['Distance'], y=df[f'{d2}_Speed'], mode='lines', name=f'{d2}', line=dict(color='orange', dash='dash')))

        # Vertical line for current scrubber position
        fig_speed.add_vline(x=current_row['Distance'], line_width=2, line_dash="dash", line_color="white")

        fig_speed.update_layout(
            xaxis_title="Distance (m)",
            yaxis_title="Speed (km/h)",
            template="plotly_dark",
            height=450,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_speed, use_container_width=True)
