# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# import argparse
# import numpy as np

# def parse_time_to_seconds(time_str):
#     h, m, s = time_str.split(':')
#     s, ms = s.split(',')
#     return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

# def visualize_participant(folder_path):
#     # 1. Load Signals - Correct column and extract fs
#     def load_clean_signal(file_name):
#         df = pd.read_csv(os.path.join(folder_path, file_name), header=None)
#         fs = float(df.iloc[1, 2])
#         data = pd.to_numeric(df.iloc[5:, 2], errors='coerce').fillna(0)
#         return data, fs

#     airflow, fs_air = load_clean_signal("airflow.csv")
#     thoracic, fs_thor = load_clean_signal("thoracic.csv")
#     spo2, fs_spo2 = load_clean_signal("spo2.csv")

#     # Start time in seconds (20:59:00)
#     start_seconds = 20 * 3600 + 59 * 60

#     fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
    
#     # 2. Plotting with time axis
#     time_air = np.arange(len(airflow)) / fs_air
#     time_thor = np.arange(len(thoracic)) / fs_thor
#     time_spo2 = np.arange(len(spo2)) / fs_spo2
    
#     ax1.plot(time_air, airflow, color='blue', linewidth=0.5, label='Airflow')
#     ax2.plot(time_thor, thoracic, color='green', linewidth=0.5, label='Thoracic')
#     ax3.plot(time_spo2, spo2, color='red', linewidth=1.0, label='SpO2')

#     # 3. Dynamic Scaling
#     ax1.set_ylim(airflow.min() - 0.1, airflow.max() + 0.1)
#     ax2.set_ylim(thoracic.min() - 0.1, thoracic.max() + 0.1)
#     ax3.set_ylim(max(0, spo2.min() - 5), 105)

#     # 4. Improved Event Overlay
#     try:
#         events_df = pd.read_csv(os.path.join(folder_path, "events.csv"), header=None)
#         for line in events_df[0]:
#             parts = line.split(';')
#             if len(parts) >= 2:
#                 full_time = parts[0]  # e.g., "30.05.2024 23:52:13,626-23:52:27,268"
#                 date_str, time_range = full_time.split(' ', 1)
#                 start_str, _ = time_range.split('-')
#                 event_start_sec = parse_time_to_seconds(start_str)
#                 if date_str == "31.05.2024":
#                     event_start_sec += 24 * 3600  # Add a day
#                 start_sec = event_start_sec - start_seconds
#                 duration = float(parts[1])
                
#                 for ax in [ax1, ax2, ax3]:
#                     ax.axvspan(start_sec, start_sec + duration, color='yellow', alpha=0.5)
#     except Exception as e:
#         print(f"Notice: Event overlay skipped: {e}")

#     # Add labels and legend
#     ax1.set_ylabel('Nasal Airflow')
#     ax2.set_ylabel('Thoracic Effort')
#     ax3.set_ylabel('SpO2 (%)')
#     ax3.set_xlabel('Time (seconds)')
    
#     ax1.legend()
#     ax2.legend()
#     ax3.legend()
#     os.makedirs("Visualizations", exist_ok=True)
#     name = os.path.basename(folder_path)
#     plt.savefig(f"Visualizations/{name}_visualization.pdf")
#     print(f"Success! Check Visualizations/{name}_visualization.pdf")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-name", type=str, required=True) 
#     args = parser.parse_args()
#     visualize_participant(args.name)

import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse
import numpy as np

def visualize_participant(folder_path):
    # 1. Load Signals
    def load_clean_signal(file_name):
        df = pd.read_csv(os.path.join(folder_path, file_name), header=None)
        # Extract fs from row 1, col 2 as per your specific file structure
        fs = float(df.iloc[1, 2])
        # Data starts from row 5 as per your code
        data = pd.to_numeric(df.iloc[5:, 2], errors='coerce').fillna(0)
        return data.values, fs

    airflow, fs_air = load_clean_signal("airflow.csv")
    thoracic, fs_thor = load_clean_signal("thoracic.csv")
    spo2, fs_spo2 = load_clean_signal("spo2.csv")

    # Create the figure
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
    
    # 2. Plotting with EXPLICIT colors and time axis
    time_air = np.arange(len(airflow)) / fs_air
    time_thor = np.arange(len(thoracic)) / fs_thor
    time_spo2 = np.arange(len(spo2)) / fs_spo2
    
    ax1.plot(time_air, airflow, color='blue', linewidth=0.7, label='Nasal Airflow')
    ax2.plot(time_thor, thoracic, color='green', linewidth=0.7, label='Thoracic Effort')
    ax3.plot(time_spo2, spo2, color='red', linewidth=1.2, label='SpO2 (%)')

    # 3. Dynamic Scaling to ensure waves are visible [cite: 16-22]
    ax1.set_ylim(np.min(airflow) - 10, np.max(airflow) + 10)
    ax2.set_ylim(np.min(thoracic) - 10, np.max(thoracic) + 10)
    ax3.set_ylim(max(0, np.min(spo2) - 5), 105)

    # 4. Event Overlay (Yellow Bars)
    try:
        events_df = pd.read_csv(os.path.join(folder_path, "events.csv"), header=None)
        for index, row in events_df.iterrows():
            line = str(row[0])
            if ';' in line:
                parts = line.split(';')
                # Extract the relative start second (e.g., the 408)
                time_info = parts[0]
                start_sec = float(time_info.split(',')[-1])
                duration = float(parts[1])
                
                # zorder=0 keeps yellow bars BEHIND the colored lines
                for ax in [ax1, ax2, ax3]:
                    ax.axvspan(start_sec, start_sec + duration, color='yellow', alpha=0.3, zorder=0)
    except Exception as e:
        print(f"Notice: Event overlay skipped: {e}")

    # Final Formatting [cite: 1, 3, 17, 29]
    ax1.set_ylabel('Airflow')
    ax2.set_ylabel('Thoracic')
    ax3.set_ylabel('SpO2 (%)')
    ax3.set_xlabel('Time (seconds)')
    
    ax1.legend(loc='upper right')
    ax2.legend(loc='upper right')
    ax3.legend(loc='upper right')

    plt.tight_layout()
    os.makedirs("Visualizations", exist_ok=True)
    name = os.path.basename(folder_path)
    plt.savefig(f"Visualizations/{name}_visualization.pdf")
    print(f"Success! Corrected colors and labels saved for {name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-name", type=str, required=True) 
    args = parser.parse_args()
    visualize_participant(args.name)