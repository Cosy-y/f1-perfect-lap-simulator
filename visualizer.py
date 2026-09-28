
from data_loader import load_and_normalize_telemetry
import plotly.express as px

def plot_speed_comparison(comparison_df, driver_1_code, driver_2_code, gp, year):
    df_melted = comparison_df.melt(
        id_vars=['Distance'], 
        value_vars=[f'{driver_1_code}_Speed', f'{driver_2_code}_Speed'],
        var_name='Driver', 
        value_name='Speed (km/h)'
    )
    df_melted['Driver'] = df_melted['Driver'].str.replace('_Speed', '')
    
    fig = px.line(
        df_melted, 
        x='Distance', 
        y='Speed (km/h)', 
        color='Driver',
        title=f"Speed Trace Comparison: {driver_1_code} vs {driver_2_code} ({gp} {year})"
    )
    fig.update_layout(xaxis_title="Track Distance (meters)", yaxis_title="Speed (km/h)", hovermode="x unified")
    return fig

if __name__ == "__main__":
    # 1. Fetch data using your data_loader function
    df, lap1, lap2 = load_and_normalize_telemetry(2024, 'Monza', 'Q', 'VER', 'LEC')
    
    # 2. Generate the plot
    fig = plot_speed_comparison(df, 'VER', 'LEC', 'Monza', 2024)
    
    # 3. Show the plot
    fig.show()
