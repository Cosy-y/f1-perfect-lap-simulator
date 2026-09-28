import pandas as pd

def generate_ghost_lap(telemetry_matrix):
    # Select only the speed columns (drop the 'Distance' column)
    speed_columns = [col for col in telemetry_matrix.columns if col.endswith('_Speed')]
    
    ghost_lap_df = pd.DataFrame()
    ghost_lap_df['Distance'] = telemetry_matrix['Distance']
    
    # 1. Find the maximum speed across all drivers at each 5-meter mark
    ghost_lap_df['Optimal_Speed'] = telemetry_matrix[speed_columns].max(axis=1)
    
    # 2. Track WHICH driver achieved that peak speed (useful for seeing who owns each corner)
    best_driver_col = telemetry_matrix[speed_columns].idxmax(axis=1)
    ghost_lap_df['Fastest_Driver'] = best_driver_col.str.replace('_Speed', '')
    
    return ghost_lap_df


