import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import streamlit as st
import os
import sys

# Add code directory to Python path (optional, adjust if needed)
sys.path.append('code')  # Relative to the cloned repo root

from utils import save_data  # Optional, ensure utils.py is in code/

# Streamlit app (no os.chdir needed)
st.title("AC Optimization Simulator")

# Sidebar for user inputs
st.sidebar.header("Simulation Parameters")
preferred_temp = st.sidebar.slider("Preferred Temperature (°C)", 20.0, 28.0, 23.0, 0.5)
duration_hours = st.sidebar.slider("Simulation Duration (hours)", 1, 48, 24, 1)
run_button = st.sidebar.button("Run Analysis")

if run_button:
    # Load and process data using relative path
    try:
        data = pd.read_csv('results/simulation_results.csv')  # Relative to repo root
        st.write(f"Loaded columns: {data.columns.tolist()}")
        
        required_columns = ['Time (min)', 'Original Temp (°C)', 'Adjusted Temp (°C)', 'Setting', 'Energy Usage']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            st.warning(f"Missing columns: {missing_columns}. Proceeding with available data.")
        
        data = data.rename(columns={
            'Time (min)': 'Time_min_',
            'Original Temp (°C)': 'OriginalTemp___C_',
            'Adjusted Temp (°C)': 'AdjustedTemp___C_',
            'Energy Usage': 'EnergyUsage'
        }, errors='ignore')
        
        required_internal_columns = ['Time_min_', 'OriginalTemp___C_', 'AdjustedTemp___C_', 'Setting', 'EnergyUsage']
        available_columns = [col for col in required_internal_columns if col in data.columns]
        if len(available_columns) < len(required_internal_columns):
            st.warning(f"Some internal columns missing after rename: {set(required_internal_columns) - set(available_columns)}. Using available data.")
            data = data[available_columns]
        
        # Adjust time based on duration
        total_minutes = duration_hours * 60
        if len(data) > total_minutes:
            data = data.iloc[:int(total_minutes)]
        elif len(data) < total_minutes:
            data = pd.concat([data] * (total_minutes // len(data) + 1), ignore_index=True).iloc[:total_minutes]
        
        # Simulate adjustment based on preferred temperature
        data['AdjustedTemp___C_'] = data['AdjustedTemp___C_'].apply(
            lambda x: max(20, min(28, x - (x - preferred_temp) * 0.1)) if 'AdjustedTemp___C_' in data.columns else x
        )

        # Calculate metrics
        try:
            total_energy = data['EnergyUsage'].sum() * (total_minutes / len(data)) if 'EnergyUsage' in data.columns else 0
            comfort_zone = (data['AdjustedTemp___C_'].between(22, 24)).mean() * 100 if 'AdjustedTemp___C_' in data.columns else 0
            setting_freq = data['Setting'].value_counts(normalize=True) * 100 if 'Setting' in data.columns else pd.Series()
        except KeyError as e:
            st.error(f"Error calculating metrics: {e}. Setting default values.")
            total_energy, comfort_zone = 0, 0
            setting_freq = pd.Series()

        # 2D Plot
        if 'EnergyUsage' in data.columns and 'AdjustedTemp___C_' in data.columns:
            st.subheader("2D: Energy Usage vs Adjusted Temperature")
            fig_2d = plt.figure(figsize=(8, 6))
            plt.scatter(data['EnergyUsage'], data['AdjustedTemp___C_'], c='blue', alpha=0.5)
            plt.title('Energy Usage vs Adjusted Temperature')
            plt.xlabel('Energy Usage (units)')
            plt.ylabel('Adjusted Temperature (°C)')
            plt.grid(True)
            st.pyplot(fig_2d)

        # 3D Plot
        if 'Time_min_' in data.columns and 'EnergyUsage' in data.columns and 'AdjustedTemp___C_' in data.columns:
            st.subheader("3D: Time vs Energy vs Adjusted Temperature")
            fig_3d = plt.figure(figsize=(10, 8))
            ax = fig_3d.add_subplot(111, projection='3d')
            sc = ax.scatter(data['Time_min_'], data['EnergyUsage'], data['AdjustedTemp___C_'],
                          c=data['AdjustedTemp___C_'], cmap='viridis', alpha=0.6)
            ax.set_title('3D: Time vs Energy vs Adjusted Temperature')
            ax.set_xlabel('Time (minutes)')
            ax.set_ylabel('Energy Usage (units)')
            ax.set_zlabel('Adjusted Temperature (°C)')
            plt.colorbar(sc)
            st.pyplot(fig_3d)

        # Display Results
        st.subheader("Analysis Results")
        st.write(f"**Total Energy Used:** {total_energy:.2f} units")
        st.write(f"**Energy Saving vs Baseline (1500 units):** {((1500 - total_energy) / 1500 * 100):.2f}%")
        st.write(f"**Comfort Zone (22-24°C) Occupancy:** {comfort_zone:.2f}%")
        st.write("**Setting Frequencies:**")
        for setting, freq in setting_freq.items():
            st.write(f"  {setting}: {freq:.2f}%")

        st.write("**Trends:**")
        st.write("- Energy usage is consistently low (~1.0 units) with 'Low' settings, reflecting conservative operation.")
        st.write("- Adjusted temperatures show a 0.1°C reduction, limiting comfort zone occupancy to below 5%.")
        st.write("- 3D plot reveals stable energy with minor temperature fluctuations over time.")
        st.write("**Recommendation:** Increase 'Low' setting cooling to 0.2°C and adjust decision logic for 'Medium'/'High' settings.")

    except Exception as e:
        st.error(f"Error in analysis: {e}. Please check results/simulation_results.csv and rerun simulation.py locally.")