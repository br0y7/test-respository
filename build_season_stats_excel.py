"""
Build Season_Stats.xlsx with Season 1 Stats and Season 2 Stats sheets.
Season 2 data = Unknown League / S2 (same source).
Run this to create or update the Excel file after CSV data changes.
"""

import os
from data_manager import data_manager

if __name__ == "__main__":
    path = data_manager.build_season_stats_excel()
    print(f"Created/updated: {os.path.abspath(path)}")
    print("Sheets: Season 1 Stats, Season 2 Stats (S2 / Unknown League)")
