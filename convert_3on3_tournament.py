"""
Convert '3 on 3 basketball tournament.xlsx' to Final_Cleaned_Data_3on3.csv
and Final_Player_Advanced_Stats_3on3.csv for use as a season in the dashboard.
Layout: team name row, then header row (Player No., PTS, FGM, ...), then player rows until TOTALS.
"""
import os
import pandas as pd


# Stat column names as they appear in the xlsx header row (used to map by name)
STAT_NAMES = ["Player No.", "PTS", "FGM", "FGA", "FG_PCT", "3PTM", "3PA", "3P%", "FTM", "FTA", "FT%", "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV", "PF"]


def _find_xlsx(data_dir: str):
    for name in ["3 on 3  basketball tournament .xlsx", "3 on 3 basketball tournament.xlsx"]:
        path = os.path.join(data_dir, name)
        if os.path.exists(path):
            return path
    return None


def _get_col_map(header_row: pd.Series) -> dict:
    """Build map from stat name to column index from the header row."""
    col_map = {}
    for c in range(len(header_row)):
        v = header_row.iloc[c]
        if pd.isna(v):
            continue
        s = str(v).strip()
        if s in STAT_NAMES:
            col_map[s] = c
    return col_map


def _read_player_row(df: pd.DataFrame, r: int, col_map: dict, team_name: str, game_name: str) -> dict:
    """Read one player row into a dict with standard keys; add MIN=0 and Efficiency."""
    row_dict = {"Team": team_name, "Game": game_name}
    for name in STAT_NAMES:
        if name in col_map:
            c = col_map[name]
            v = df.iloc[r, c]
            if pd.isna(v) and name in ("FG_PCT", "3P%", "FT%"):
                row_dict[name] = 0.0
            else:
                try:
                    row_dict[name] = int(float(v)) if name == "Player No." else float(v)
                except (ValueError, TypeError):
                    row_dict[name] = 0 if name != "Player No." else 0
        else:
            row_dict[name] = 0 if name != "Player No." else 0
    row_dict["MIN"] = 0
    PTS = row_dict.get("PTS", 0)
    REB = row_dict.get("REB", 0)
    AST = row_dict.get("AST", 0)
    STL = row_dict.get("STL", 0)
    BLK = row_dict.get("BLK", 0)
    TOV = row_dict.get("TOV", 0)
    FGA = row_dict.get("FGA", 0)
    FGM = row_dict.get("FGM", 0)
    FTA = row_dict.get("FTA", 0)
    FTM = row_dict.get("FTM", 0)
    row_dict["Efficiency"] = PTS + REB + AST + STL + BLK - TOV - (FGA - FGM) - 0.5 * max(0, FTA - FTM)
    return row_dict


def _game_type_from_sheet_name(game_name: str) -> str:
    """Infer Round Robin vs Playoffs from sheet name."""
    lower = game_name.lower()
    playoff_keywords = (
        "playoff", "playoffs",
        "final", "finals",
        "semifinal", "semi-final", "semi final", "semis",
        "championship", "quarter",
        "winners bracket", "losers bracket", "loser's bracket", "bracket",
        "third place",
    )
    if any(x in lower for x in playoff_keywords):
        return "Playoffs"
    return "Round Robin"


def _parse_sheet(df: pd.DataFrame, game_name: str) -> list:
    """Parse one sheet (one game, two teams). Return list of dicts for game-level rows."""
    rows_out = []
    game_type = _game_type_from_sheet_name(game_name)
    # Team 1: row 3 (0-based) = team name, row 4 = header, row 5+ = players until TOTALS
    team1_name = df.iloc[3, 0]
    if pd.isna(team1_name) or str(team1_name).strip().upper() == "TOTALS":
        return rows_out
    team1_name = str(team1_name).strip()
    header_row = df.iloc[4]
    col_map = _get_col_map(header_row)
    if "Player No." not in col_map:
        return rows_out
    r = 5
    while r < len(df):
        val = df.iloc[r, col_map["Player No."]]
        if pd.isna(val):
            r += 1
            continue
        s = str(val).strip().upper()
        if s == "TOTALS":
            break
        row = _read_player_row(df, r, col_map, team1_name, game_name)
        row["Game_Type"] = game_type
        rows_out.append(row)
        r += 1

    # Skip TOTALS row and blank; next row = team 2 name, then header, then players
    r += 1
    while r < len(df) and (pd.isna(df.iloc[r, 0]) or str(df.iloc[r, 0]).strip() == ""):
        r += 1
    if r >= len(df):
        return rows_out
    team2_name = df.iloc[r, 0]
    if pd.isna(team2_name) or str(team2_name).strip().upper() == "TOTALS":
        return rows_out
    team2_name = str(team2_name).strip()
    r += 1
    if r >= len(df):
        return rows_out
    header_row2 = df.iloc[r]
    col_map2 = _get_col_map(header_row2)
    if "Player No." not in col_map2:
        col_map2 = col_map
    r += 1
    while r < len(df):
        val = df.iloc[r, col_map2.get("Player No.", 0)]
        if pd.isna(val):
            r += 1
            continue
        s = str(val).strip().upper()
        if s == "TOTALS":
            break
        row = _read_player_row(df, r, col_map2, team2_name, game_name)
        row["Game_Type"] = game_type
        rows_out.append(row)
        r += 1

    return rows_out


def convert_to_csv(data_dir: str = ".") -> tuple:
    """
    Read the 3on3 tournament xlsx and write Final_Cleaned_Data_3on3.csv and
    Final_Player_Advanced_Stats_3on3.csv. Returns (cleaned_path, advanced_path).
    """
    xlsx_path = _find_xlsx(data_dir)
    if not xlsx_path:
        raise FileNotFoundError("3 on 3 basketball tournament.xlsx not found")

    xl = pd.ExcelFile(xlsx_path)
    all_rows = []
    for sheet_name in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        game_name = str(sheet_name).strip()
        all_rows.extend(_parse_sheet(df, game_name))

    if not all_rows:
        raise ValueError("No game data found in the workbook")

    cleaned = pd.DataFrame(all_rows)
    # Column order expected by app (include Game_Type for Round Robin vs Playoffs)
    out_cols = ["Player No.", "Team", "Game", "Game_Type", "FGM", "FGA", "3PTM", "3PA", "FTM", "FTA", "MIN", "PTS", "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV", "PF", "FG_PCT", "3P%", "FT%", "Efficiency"]
    cleaned = cleaned[[c for c in out_cols if c in cleaned.columns]]
    cleaned_path = os.path.join(data_dir, "Final_Cleaned_Data_3on3.csv")
    cleaned.to_csv(cleaned_path, index=False)

    # Advanced stats: one row per player
    agg = cleaned.groupby(["Player No.", "Team"], as_index=False).agg(
        PTS=("PTS", "sum"),
        REB=("REB", "sum"),
        AST=("AST", "sum"),
        FGM=("FGM", "sum"),
        FGA=("FGA", "sum"),
        FTM=("FTM", "sum"),
        FTA=("FTA", "sum"),
        TOV=("TOV", "sum"),
        STL=("STL", "sum"),
        BLK=("BLK", "sum"),
        games=("Game", "nunique"),
    )
    agg["Total_Games_Played"] = agg["games"]
    agg["Total_MIN_Played"] = 0
    agg["Player_Team_Label"] = "Player " + agg["Player No."].astype(str) + " (" + agg["Team"].astype(str) + ")"
    # Simple ratios
    agg["Avg_AST_TOV_Ratio"] = (agg["AST"] / agg["TOV"].replace(0, pd.NA)).fillna(0).astype(float)
    ts_denom = 2 * (agg["FGA"] + 0.44 * agg["FTA"].replace(0, pd.NA))
    agg["Avg_TS_Percentage"] = (100 * agg["PTS"] / ts_denom.replace(0, pd.NA)).fillna(0).astype(float)
    agg["Avg_REB_Percentage"] = 10.0
    agg["Avg_Efficiency"] = (agg["PTS"] + agg["REB"] + agg["AST"] + agg["STL"] + agg["BLK"] - agg["TOV"]) / agg["games"]
    agg["Avg_WS_Simplified"] = agg["Avg_Efficiency"] / 10.0
    agg["Avg_VORP_Simplified"] = agg["Avg_WS_Simplified"] / 5.0
    agg["Avg_PTS_Per_Min"] = 0.0
    agg["Avg_REB_Per_Min"] = 0.0
    agg["Avg_AST_Per_Min"] = 0.0
    agg["Avg_STL_Per_Min"] = 0.0
    agg["Avg_BLK_Per_Min"] = 0.0

    adv_cols = ["Player No.", "Team", "Player_Team_Label", "Total_Games_Played", "Total_MIN_Played",
                "Avg_PTS_Per_Min", "Avg_REB_Per_Min", "Avg_AST_Per_Min", "Avg_STL_Per_Min", "Avg_BLK_Per_Min",
                "Avg_AST_TOV_Ratio", "Avg_TS_Percentage", "Avg_REB_Percentage", "Avg_Efficiency",
                "Avg_WS_Simplified", "Avg_VORP_Simplified"]
    advanced = agg[[c for c in adv_cols if c in agg.columns]]
    advanced_path = os.path.join(data_dir, "Final_Player_Advanced_Stats_3on3.csv")
    advanced.to_csv(advanced_path, index=False)

    return cleaned_path, advanced_path


if __name__ == "__main__":
    convert_to_csv()
    print("Created Final_Cleaned_Data_3on3.csv and Final_Player_Advanced_Stats_3on3.csv")
