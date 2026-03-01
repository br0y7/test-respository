import subprocess
import sys
import os


def run_dashboard():
    """
    Launches the Streamlit dashboard app.
    Uses existing CSV data (Final_Cleaned_Data*.csv, Final_Player_Advanced_Stats*.csv).
    No gamechanger ETL script required.
    """
    dashboard_file = "dashboard_app.py"
    if not os.path.exists(dashboard_file):
        print(f"Error: '{dashboard_file}' not found in the current directory.")
        sys.exit(1)

    print("--- Launching GameChanger Dashboard ---")
    print("Please wait for the browser to open or follow the URL provided by Streamlit.")

    streamlit_command = [sys.executable, "-m", "streamlit", "run", dashboard_file]
    subprocess.run(streamlit_command)


if __name__ == "__main__":
    run_dashboard()
