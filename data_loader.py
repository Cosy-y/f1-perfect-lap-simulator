# data_loader.py
import os
import pandas as pd
import numpy as np
import fastf1

# Create cache directory if it doesn't exist
os.makedirs('f1_cache', exist_ok=True)

# Enable cache to speed up repeated runs
fastf1.Cache.enable_cache('f1_cache')

def load_replay_telemetry(year, gp, session_type, driver_1_code, driver_2_code):
    print(f"Loading replay data for {year} {gp} ({session_type})...")
    session = fastf1.get_session(year, gp, session_type)
    session.load(telemetry=True, laps=True, weather=False, messages=False)

    d1_lap = session.laps.pick_driver(driver_1_code).pick_fastest()
    d2_lap = session.laps.pick_driver(driver_2_code).pick_fastest()

    d1_tel = d1_lap.get_telemetry()
    d2_tel = d2_lap.get_telemetry()

    max_distance = min(d1_tel['Distance'].max(), d2_tel['Distance'].max())
    distance_grid = np.arange(0, max_distance, 10)  # 10-meter intervals for smooth scrubbing

    # Interpolate Speed and Spatial X, Y coordinates
    d1_speed = np.interp(distance_grid, d1_tel['Distance'], d1_tel['Speed'])
    d1_x = np.interp(distance_grid, d1_tel['Distance'], d1_tel['X'])
    d1_y = np.interp(distance_grid, d1_tel['Distance'], d1_tel['Y'])

    d2_speed = np.interp(distance_grid, d2_tel['Distance'], d2_tel['Speed'])
    d2_x = np.interp(distance_grid, d2_tel['Distance'], d2_x_arr := d2_tel['X']) # standard interpolation mapping
    d2_y = np.interp(distance_grid, d2_tel['Distance'], d2_tel['Y'])

    replay_df = pd.DataFrame({
        'Distance': distance_grid,
        f'{driver_1_code}_Speed': d1_speed,
        f'{driver_1_code}_X': d1_x,
        f'{driver_1_code}_Y': d1_y,
        f'{driver_2_code}_Speed': d2_speed,
        f'{driver_2_code}_X': d2_x,
        f'{driver_2_code}_Y': d2_y,
    })

    return replay_df, d1_lap, d2_lap, session
