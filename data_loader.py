import os
import pandas as pd
import numpy as np
import fastf1

# Create cache directory if it doesn't exist
os.makedirs('f1_cache', exist_ok=True)

# Enable cache to speed up repeated runs
fastf1.Cache.enable_cache('f1_cache')

def load_and_normalize_telemetry(year, gp, session_type, driver_1_code, driver_2_code):
    print(f"Loading {year} {gp} ({session_type})...")
    session = fastf1.get_session(year, gp, session_type)
    session.load(telemetry=True, laps=True, weather=False, messages=False)

    # Get fastest laps for both drivers
    d1_lap = session.laps.pick_driver(driver_1_code).pick_fastest()
    d2_lap = session.laps.pick_driver(driver_2_code).pick_fastest()

    # Extract telemetry arrays
    d1_tel = d1_lap.get_telemetry()
    d2_tel = d2_lap.get_telemetry()

    max_distance = min(d1_tel['Distance'].max(), d2_tel['Distance'].max())
    distance_grid = np.arange(0, max_distance, 5) # 5-meter intervals

    # Interpolate data across the uniform distance grid
    d1_speed_interp = np.interp(distance_grid, d1_tel['Distance'], d1_tel['Speed'])
    d2_speed_interp = np.interp(distance_grid, d2_tel['Distance'], d2_tel['Speed'])

    # Bundle into a clean DataFrame
    comparison_df = pd.DataFrame({
        'Distance': distance_grid,
        f'{driver_1_code}_Speed': d1_speed_interp,
        f'{driver_2_code}_Speed': d2_speed_interp
    })

    return comparison_df, d1_lap, d2_lap


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
