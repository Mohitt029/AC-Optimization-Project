import pandas as pd
import numpy as np
from ai_models import AIModels
import os

def simulate_ac(data_path: str = "../data/raw_data.csv", output_path: str = "../results/simulation_results.csv"):
    """Simulate AC operation over 24 hours."""
    # Load data and AI models
    ai = AIModels(data_path)
    ai.train_decision_tree()
    data = pd.read_csv(data_path)

    # Initialize simulation variables
    energy = 0
    adjusted_temps = []
    settings = []

    for index, row in data.iterrows():
        temp = row['Temperature (°C)']
        occupancy = row['Occupancy']
        air_quality = row['Air Quality (ppm)']

        # Get decision tree setting
        setting = ai.get_decision_tree_prediction(temp, occupancy, air_quality)
        settings.append(setting)

        # Apply cooling (simplified)
        if setting == 'High':
            energy += 3
            new_temp = temp - 0.5
        elif setting == 'Medium':
            energy += 2
            new_temp = temp - 0.3
        else:  # Low
            energy += 1
            new_temp = temp - 0.1
        adjusted_temps.append(new_temp)

    # Save results
    results = pd.DataFrame({
        'Time (min)': data['Time (min)'],
        'Original Temp (°C)': data['Temperature (°C)'],
        'Adjusted Temp (°C)': adjusted_temps,
        'Setting': settings,
        'Energy Usage': [energy/len(data)] * len(data)  # Average energy per minute
    })
    os.makedirs('../results', exist_ok=True)
    results.to_csv(output_path, index=False)
    print(f"Simulation complete. Energy used: {energy:.1f} units. Results saved to {output_path}")

if __name__ == "__main__":
    simulate_ac()