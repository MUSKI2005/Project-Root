import pandas as pd
import os

def convert_to_csv(folder_path):
    # Mapping of your current messy names to clean CSV names
    file_map = {
        # "Flow - 30-05-2024.txt": "airflow.csv",
        # "Thorac - 30-05-2024.txt": "thoracic.csv",
        # "SPO2 - 30-05-2024.txt": "spo2.csv",
        "Flow Events - 30-05-2024.txt": "events.csv"
    }

    for old_name, new_name in file_map.items():
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        
        if os.path.exists(old_path):
            # Read the messy text file (skipping headers/metadata as we discussed)
            # For signals, we skip 1 line; for events, we skip 2
            skip = 2 if "Events" in old_name else 1
            df = pd.read_csv(old_path, sep=None, engine='python', skiprows=skip)
            
            # Save as a clean, comma-separated CSV
            df.to_csv(new_path, index=False)
            print(f"Converted: {old_name} -> {new_name}")

if __name__ == "__main__":
    convert_to_csv("Data/AP01")