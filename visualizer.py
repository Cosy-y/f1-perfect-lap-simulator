
import plotly.graph_objects as go

def plot_speed_comparison(df, driver_1, driver_2, gp, year):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Distance'], 
        y=df[f'{driver_1}_Speed'], 
        mode='lines', 
        name=f'{driver_1} Speed',
        line=dict(width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Distance'], 
        y=df[f'{driver_2}_Speed'], 
        mode='lines', 
        name=f'{driver_2} Speed',
        line=dict(width=2, dash='dash')
    ))

    fig.update_layout(
        title=f"Speed Trace Comparison: {driver_1} vs {driver_2} ({year} {gp})",
        xaxis_title="Distance into Lap (meters)",
        yaxis_title="Speed (km/h)",
        template="plotly_dark",
        height=500,
        hovermode="x unified"
    )

    return fig
