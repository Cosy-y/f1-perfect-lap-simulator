# track_map.py
import plotly.graph_objects as go
import numpy as np

def plot_track_map(d1_lap, d2_lap, driver_1, driver_2):
    # Extract position telemetry data (X, Y coordinates on track)
    d1_pos = d1_lap.get_pos_data()
    d2_pos = d2_lap.get_pos_data()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=d1_pos['X'], y=d1_pos['Y'],
        mode='lines',
        name=f'{driver_1} Line',
        line=dict(width=4)
    ))

    
    fig.add_trace(go.Scatter(
        x=d2_pos['X'], y=d2_pos['Y'],
        mode='lines',
        name=f'{driver_2} Line',
        line=dict(width=2, dash='dot')
    ))

    fig.update_layout(
        title="Circuit Spatial Comparison (Track Layout Map)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        template="plotly_dark",
        height=600,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig
