"""
Data Manager Module for Basketball Analytics Dashboard
Handles data storage, retrieval, and management
Supports CSV files (local) with structure ready for cloud migration (Google Sheets, SQL, etc.)
"""

import os
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class DataManager:
    """
    Manages player data storage and retrieval
    Currently uses CSV files, but structured for easy migration to cloud storage
    """
    
    def __init__(self, data_dir: str = "."):
        self.data_dir = data_dir
        # Season 1 (main league)
        self.cleaned_data_file = os.path.join(data_dir, "Final_Cleaned_Data.csv")
        self.advanced_stats_file = os.path.join(data_dir, "Final_Player_Advanced_Stats.csv")
        # Season 2 (Unknown League / S2 - same data, different label)
        self.cleaned_data_s2_file = os.path.join(data_dir, "Final_Cleaned_Data_Unknown_League.csv")
        self.advanced_stats_s2_file = os.path.join(data_dir, "Final_Player_Advanced_Stats_Unknown_League.csv")
        
    def load_player_data(self, season: Optional[int] = None) -> pd.DataFrame:
        """
        Load cleaned player game data. If season is 1 use Final_Cleaned_Data.csv;
        if season is 2 use Final_Cleaned_Data_Unknown_League.csv (S2 / Unknown League).
        Default season=1 if None.
        """
        s = 1 if season is None else season
        if s == 1:
            if not os.path.exists(self.cleaned_data_file):
                raise FileNotFoundError(f"Player data file not found: {self.cleaned_data_file}")
            return pd.read_csv(self.cleaned_data_file)
        else:
            if not os.path.exists(self.cleaned_data_s2_file):
                raise FileNotFoundError(f"Season 2 player data file not found: {self.cleaned_data_s2_file}")
            return pd.read_csv(self.cleaned_data_s2_file)
    
    def load_advanced_stats(self, season: Optional[int] = None) -> pd.DataFrame:
        """
        Load player advanced statistics. If season is 1 use Final_Player_Advanced_Stats.csv;
        if season is 2 use Final_Player_Advanced_Stats_Unknown_League.csv (S2 / Unknown League).
        Default season=1 if None.
        """
        s = 1 if season is None else season
        if s == 1:
            if not os.path.exists(self.advanced_stats_file):
                raise FileNotFoundError(f"Advanced stats file not found: {self.advanced_stats_file}")
            return pd.read_csv(self.advanced_stats_file)
        else:
            if not os.path.exists(self.advanced_stats_s2_file):
                raise FileNotFoundError(f"Season 2 advanced stats file not found: {self.advanced_stats_s2_file}")
            return pd.read_csv(self.advanced_stats_s2_file)
    
    def get_player_profile(self, player_no: int, team: str, season: Optional[int] = None) -> Dict[str, Any]:
        """
        Get comprehensive player profile with all stats for the given season.
        Returns structured data ready for AI prompt generation.
        """
        try:
            s = 1 if season is None else season
            game_data = self.load_player_data(season=s)
            advanced_stats = self.load_advanced_stats(season=s)
            
            # Filter for specific player
            player_games = game_data[
                (game_data['Player No.'] == player_no) & 
                (game_data['Team'] == team)
            ]
            
            player_advanced = advanced_stats[
                (advanced_stats['Player No.'] == player_no) & 
                (advanced_stats['Team'] == team)
            ]
            
            if player_games.empty:
                return {"error": "Player not found"}
            
            # Calculate averages and totals
            profile = {
                "player_no": int(player_no),
                "team": team,
                "total_games": len(player_games),
                "stats": {
                    "points": {
                        "total": int(player_games['PTS'].sum()),
                        "average": float(player_games['PTS'].mean()),
                        "max": int(player_games['PTS'].max()),
                        "min": int(player_games['PTS'].min())
                    },
                    "rebounds": {
                        "total": int(player_games['REB'].sum()),
                        "average": float(player_games['REB'].mean()),
                        "max": int(player_games['REB'].max())
                    },
                    "assists": {
                        "total": int(player_games['AST'].sum()),
                        "average": float(player_games['AST'].mean()),
                        "max": int(player_games['AST'].max())
                    },
                    "turnovers": {
                        "total": int(player_games['TOV'].sum()),
                        "average": float(player_games['TOV'].mean())
                    },
                    "steals": {
                        "total": int(player_games['STL'].sum()),
                        "average": float(player_games['STL'].mean())
                    },
                    "blocks": {
                        "total": int(player_games['BLK'].sum()),
                        "average": float(player_games['BLK'].mean())
                    },
                    "shooting": {
                        "fg_pct": float(player_games['FG_PCT'].mean()),
                        "three_pct": float(player_games['3P%'].mean()),
                        "ft_pct": float(player_games['FT%'].mean())
                    },
                    "efficiency": {
                        "average": float(player_games['Efficiency'].mean()),
                        "max": int(player_games['Efficiency'].max())
                    }
                }
            }
            
            # Add advanced stats if available
            if not player_advanced.empty:
                profile["advanced_stats"] = {
                    "ast_tov_ratio": float(player_advanced['Avg_AST_TOV_Ratio'].iloc[0]),
                    "ts_percentage": float(player_advanced['Avg_TS_Percentage'].iloc[0]),
                    "reb_percentage": float(player_advanced['Avg_REB_Percentage'].iloc[0]),
                    "ws": float(player_advanced['Avg_WS_Simplified'].iloc[0]),
                    "vorp": float(player_advanced['Avg_VORP_Simplified'].iloc[0])
                }
            
            # Identify strengths and weaknesses
            profile["strengths"] = self._identify_strengths(profile)
            profile["weaknesses"] = self._identify_weaknesses(profile)
            
            return profile
            
        except Exception as e:
            return {"error": str(e)}
    
    def _identify_strengths(self, profile: Dict[str, Any]) -> List[str]:
        """Identify player strengths based on stats"""
        strengths = []
        stats = profile["stats"]
        
        # Points strength
        if stats["points"]["average"] >= 15:
            strengths.append("Scoring ability")
        elif stats["points"]["average"] >= 10:
            strengths.append("Solid scoring")
        
        # Rebounding strength
        if stats["rebounds"]["average"] >= 8:
            strengths.append("Strong rebounding")
        elif stats["rebounds"]["average"] >= 5:
            strengths.append("Good rebounding")
        
        # Assists strength
        if stats["assists"]["average"] >= 5:
            strengths.append("Playmaking and ball distribution")
        elif stats["assists"]["average"] >= 3:
            strengths.append("Good passing")
        
        # Shooting strength
        if stats["shooting"]["fg_pct"] >= 0.45:
            strengths.append("Efficient field goal shooting")
        if stats["shooting"]["three_pct"] >= 0.35:
            strengths.append("Three-point shooting")
        if stats["shooting"]["ft_pct"] >= 0.75:
            strengths.append("Free throw shooting")
        
        # Defense
        if stats["steals"]["average"] >= 2:
            strengths.append("Defensive playmaking (steals)")
        if stats["blocks"]["average"] >= 1:
            strengths.append("Shot blocking")
        
        return strengths if strengths else ["Versatile player"]
    
    def _identify_weaknesses(self, profile: Dict[str, Any]) -> List[str]:
        """Identify player weaknesses based on stats"""
        weaknesses = []
        stats = profile["stats"]
        
        # Turnover issues
        if stats["turnovers"]["average"] >= 4:
            weaknesses.append("High turnover rate")
        elif stats["turnovers"]["average"] >= 2.5:
            weaknesses.append("Ball control needs improvement")
        
        # Shooting weaknesses
        if stats["shooting"]["fg_pct"] < 0.35:
            weaknesses.append("Field goal percentage needs improvement")
        if stats["shooting"]["three_pct"] < 0.25 and stats["shooting"]["three_pct"] > 0:
            weaknesses.append("Three-point shooting accuracy")
        if stats["shooting"]["ft_pct"] < 0.60 and stats["shooting"]["ft_pct"] > 0:
            weaknesses.append("Free throw shooting")
        
        # Low production areas
        if stats["rebounds"]["average"] < 3:
            weaknesses.append("Rebounding")
        if stats["assists"]["average"] < 2:
            weaknesses.append("Playmaking and assists")
        
        return weaknesses
    
    def get_all_players(self, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get list of all players for the given season (1 or 2). Default season=1."""
        try:
            s = 1 if season is None else season
            advanced_stats = self.load_advanced_stats(season=s)
            players = []
            for _, row in advanced_stats.iterrows():
                players.append({
                    "player_no": int(row['Player No.']),
                    "team": row['Team'],
                    "label": row['Player_Team_Label']
                })
            return players
        except Exception as e:
            return []
    
    def save_player_data(self, data: pd.DataFrame, filename: Optional[str] = None):
        """Save player data to CSV (for future cloud sync)"""
        if filename is None:
            filename = self.cleaned_data_file
        data.to_csv(filename, index=False)

    def build_season_stats_excel(self, filepath: Optional[str] = None) -> str:
        """
        Create an Excel workbook with Season 1 Stats and Season 2 Stats sheets.
        Season 2 uses the same data as Unknown League / S2.
        Returns the path to the written file.
        """
        if filepath is None:
            filepath = os.path.join(self.data_dir, "Season_Stats.xlsx")
        with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
            if os.path.exists(self.advanced_stats_file):
                df_s1 = pd.read_csv(self.advanced_stats_file)
                df_s1.to_excel(writer, sheet_name="Season 1 Stats", index=False)
            if os.path.exists(self.advanced_stats_s2_file):
                df_s2 = pd.read_csv(self.advanced_stats_s2_file)
                df_s2.to_excel(writer, sheet_name="Season 2 Stats", index=False)
        return filepath

    # Future methods for cloud integration:
    # def sync_to_google_sheets(self): ...
    # def sync_to_sql(self): ...
    # def sync_to_cloud_storage(self): ...

# Global instance
data_manager = DataManager()

