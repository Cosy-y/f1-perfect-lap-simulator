import pandas as pd
import numpy as np
import os
import fastf1

# Create cache directory if it doesn't exist
os.makedirs('f1_cache', exist_ok=True)

# Enable cache to speed up repeated runs
fastf1.Cache.enable_cache('f1_cache')


def load_all_drivers_telemetry(year, gp, session_type):
    print(f"Loading {year} {gp} ({session_type}) for all drivers...")
    session = fastf1.get_session(year, gp, session_type)
    session.load(telemetry=True, laps=True, weather=False, messages=False)

    # Get a list of all unique drivers in the session
    drivers = session.laps['Driver'].unique()
    
    max_distances = []
    driver_teles = {}

    # Collect fastest lap telemetry for each valid driver
    for driver in drivers:
        try:
            lap = session.laps.pick_driver(driver).pick_fastest()
            tel = lap.get_telemetry()
            if not tel.empty:
                max_distances.append(tel['Distance'].max())
                driver_teles[driver] = tel
        except Exception:
            # Skip drivers with missing or incomplete telemetry data
            continue

    if not max_distances:
        raise ValueError("No valid telemetry data found for drivers in this session.")

    # Use the minimum of the maximum distances so every driver's lap covers the range
    common_max_distance = min(max_distances)
    distance_grid = np.arange(0, common_max_distance, 5)  # 5-meter intervals

    # Create a base dataframe with our distance checkpoints
    telemetry_matrix = pd.DataFrame({'Distance': distance_grid})

    # Interpolate each driver's speed profile onto the unified distance grid                                
    for driver, tel in driver_teles.items():
        speed_interp = np.interp(distance_grid, tel['Distance'], tel['Speed'])
        telemetry_matrix[f'{driver}_Speed'] = speed_interp

    print(f"Successfully aligned telemetry for {len(driver_teles)} drivers!")
    return telemetry_matrix, session

