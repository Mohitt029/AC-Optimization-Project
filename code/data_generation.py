import numpy as np
import pandas as pd

# Generate 1440 minutes (24 hours) of data
minutes = 1440
time = np.arange(minutes)
temp = 20 + 15 * np.sin(np.linspace(0, 2 * np.pi, minutes)) + np.random.normal(0, 2, minutes)  # 20-35°C with noise
occupancy = np.random.randint(0, 10, minutes)  # 0 to 10 people
air_quality = 400 + 1600 * np.random.random(minutes)  # 400-2000 ppm CO2

# Create DataFrame and save
data = pd.DataFrame({'Time (min)': time, 'Temperature (°C)': temp, 'Occupancy': occupancy, 'Air Quality (ppm)': air_quality})
data.to_csv('../data/raw_data.csv', index=False)
print("Data generated and saved as raw_data.csv")