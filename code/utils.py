import pandas as pd
import os
import numpy as np

def load_data(file_path):
    """Load CSV data with error handling and validation."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")
    df = pd.read_csv(file_path)
    # Validate against actual CSV headers
    required_columns = ['Time (min)', 'Original Temp (°C)', 'Adjusted Temp (°C)', 'Setting', 'Energy Usage']
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}. Available columns: {df.columns.tolist()}")
    if df.empty or any(df[col].isnull().all() for col in required_columns):
        raise ValueError("Data contains empty or all-null columns")
    return df

def save_data(df, file_path):
    """Save DataFrame to CSV with validation."""
    if df.empty:
        raise ValueError("DataFrame is empty, nothing to save")
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

def validate_numeric(series):
    """Validate that a series contains numeric data."""
    return pd.to_numeric(series, errors='coerce').notna().all()

if __name__ == "__main__":
    try:
        df = load_data('../results/simulation_results.csv')
        if all(validate_numeric(df[col]) for col in ['Time (min)', 'Original Temp (°C)', 'Adjusted Temp (°C)', 'Energy Usage']):
            save_data(df, '../results/test_output.csv')
            print("Validation successful")
        else:
            print("Non-numeric data detected")
    except Exception as e:
        print(f"Error: {e}")