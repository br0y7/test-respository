"""
Rule-Based Coaching Assistant (Free Alternative)
Provides personalized basketball coaching advice without AI API calls
Uses smart rules and templates based on player statistics
"""

from typing import Dict, List, Optional, Any
from data_manager import data_manager
from drill_library import drill_library
import pandas as pd

class RuleBasedAssistant:
    """
    Free rule-based coaching assistant
    Provides personalized feedback using statistical analysis and templates
    """
    
    def __init__(self):
        self.enabled = True  # Always enabled - no API key needed

    def _find_team_in_question(self, question_lower: str) -> Optional[str]:
        """Try to match a team name from the dataset inside the user's question."""
        try:
            game_data = data_manager.load_player_data()
            teams = sorted({str(t) for t in game_data["Team"].dropna().unique()})
        except Exception:
            teams = []

        # Prefer longest matches first to avoid partial collisions
        for team in sorted(teams, key=len, reverse=True):
            if team.lower() in question_lower:
                return team
        return None

    def _team_scout_report(self, team: str) -> str:
        """Generate a simple strengths/weaknesses report for a team vs league averages."""
        try:
            game_data = data_manager.load_player_data()
        except Exception:
            return f"Couldn't load data to scout {team}."

        df = game_data.copy()
        df["FG%"] = df["FGM"] / df["FGA"].replace(0, pd.NA)
        df["3P%"] = df["3PTM"] / df["3PA"].replace(0, pd.NA)
        df["FT%"] = df["FTM"] / df["FTA"].replace(0, pd.NA)

        league = df.agg(
            PTS=("PTS", "mean"),
            REB=("REB", "mean"),
            AST=("AST", "mean"),
            TOV=("TOV", "mean"),
            Efficiency=("Efficiency", "mean"),
            FG_pct=("FG%", "mean"),
            Three_pct=("3P%", "mean"),
        )

        team_df = df[df["Team"] == team]
        if team_df.empty:
            return f"No games found for team {team}."

        team_stats = team_df.agg(
            PTS=("PTS", "mean"),
            REB=("REB", "mean"),
            AST=("AST", "mean"),
            TOV=("TOV", "mean"),
            Efficiency=("Efficiency", "mean"),
            FG_pct=("FG%", "mean"),
            Three_pct=("3P%", "mean"),
        )

        def _scalar(v) -> float:
            """Ensure agg results are scalars (pandas can sometimes return 1-element Series)."""
            try:
                # pandas scalar types
                if hasattr(v, "item") and not isinstance(v, (float, int, str)):
                    return float(v.item())
            except Exception:
                pass
            try:
                # 1-element Series
                if hasattr(v, "iloc"):
                    return float(v.iloc[0])
            except Exception:
                pass
            return float(v)

        league = {k: _scalar(league[k]) for k in league.index}
        team_stats = {k: _scalar(team_stats[k]) for k in team_stats.index}

        # Identify strengths/weaknesses with simple thresholds
        strengths = []
        weaknesses = []

        def pct_diff(a, b):
            if pd.isna(a) or pd.isna(b) or b == 0:
                return 0.0
            return float((a - b) / b)

        # Offense
        if team_stats["PTS"] > league["PTS"] * 1.05:
            strengths.append(f"Scoring (+{pct_diff(team_stats['PTS'], league['PTS'])*100:.0f}% vs league)")
        if team_stats["FG_pct"] > league["FG_pct"] * 1.05:
            strengths.append(f"Efficient shooting (FG% {team_stats['FG_pct']:.1%})")
        if team_stats["Three_pct"] > league["Three_pct"] * 1.05:
            strengths.append(f"Three-point shooting (3P% {team_stats['Three_pct']:.1%})")

        # Playmaking
        if team_stats["AST"] > league["AST"] * 1.05:
            strengths.append(f"Ball movement (AST +{pct_diff(team_stats['AST'], league['AST'])*100:.0f}% vs league)")
        if team_stats["TOV"] > league["TOV"] * 1.10:
            weaknesses.append(f"Turnovers (TOV +{pct_diff(team_stats['TOV'], league['TOV'])*100:.0f}% vs league)")

        # Rebounding / efficiency
        if team_stats["REB"] > league["REB"] * 1.05:
            strengths.append(f"Rebounding (REB +{pct_diff(team_stats['REB'], league['REB'])*100:.0f}% vs league)")
        if team_stats["Efficiency"] > league["Efficiency"] * 1.05:
            strengths.append(f"Overall efficiency (+{pct_diff(team_stats['Efficiency'], league['Efficiency'])*100:.0f}% vs league)")
        if team_stats["Efficiency"] < league["Efficiency"] * 0.95:
            weaknesses.append(f"Overall efficiency (-{abs(pct_diff(team_stats['Efficiency'], league['Efficiency'])*100):.0f}% vs league)")

        # If no strengths/weaknesses found, fall back
        if not strengths:
            strengths = ["Balanced team profile (no single stat far above league)"]
        if not weaknesses:
            weaknesses = ["No major weaknesses flagged by team averages"]

        lines = []
        lines.append(f"### 🧠 Scout report: {team}")
        lines.append("")
        lines.append("**Team averages (per game):**")
        lines.append(f"- PTS: {team_stats['PTS']:.1f} | REB: {team_stats['REB']:.1f} | AST: {team_stats['AST']:.1f} | TOV: {team_stats['TOV']:.1f} | EFF: {team_stats['Efficiency']:.1f}")
        lines.append(f"- FG%: {team_stats['FG_pct']:.1%} | 3P%: {team_stats['Three_pct']:.1%}")
        lines.append("")
        lines.append("**Strengths:**")
        for s in strengths[:5]:
            lines.append(f"- {s}")
        lines.append("")
        lines.append("**Weaknesses:**")
        for w in weaknesses[:5]:
            lines.append(f"- {w}")
        return "\n".join(lines)

    def _get_team_leaders(self, team: str, stat_category: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """Get top performers within a team for a stat category."""
        try:
            game_data = data_manager.load_player_data()
        except Exception:
            return []

        team_players = [p for p in data_manager.get_all_players() if p.get("team") == team]
        rows: List[Dict[str, Any]] = []

        for p in team_players:
            prof = data_manager.get_player_profile(p["player_no"], p["team"])
            if "error" in prof:
                continue
            stats = prof.get("stats", {})

            if stat_category == "points":
                val = float(stats.get("points", {}).get("average", 0.0))
                rows.append({"name": p["label"], "team": team, "stat_name": "PPG", "stat_display": f"{val:.1f}", "stat_value": val})
            elif stat_category == "rebounds":
                val = float(stats.get("rebounds", {}).get("average", 0.0))
                rows.append({"name": p["label"], "team": team, "stat_name": "RPG", "stat_display": f"{val:.1f}", "stat_value": val})
            elif stat_category == "assists":
                val = float(stats.get("assists", {}).get("average", 0.0))
                rows.append({"name": p["label"], "team": team, "stat_name": "APG", "stat_display": f"{val:.1f}", "stat_value": val})
            elif stat_category == "fg_pct":
                val = float(stats.get("shooting", {}).get("fg_pct", 0.0))
                rows.append({"name": p["label"], "team": team, "stat_name": "FG%", "stat_display": f"{val:.1%}", "stat_value": val})
            elif stat_category == "three_pct":
                val = float(stats.get("shooting", {}).get("three_pct", 0.0))
                rows.append({"name": p["label"], "team": team, "stat_name": "3P%", "stat_display": f"{val:.1%}", "stat_value": val})
            elif stat_category == "three_point":
                pg = game_data[(game_data["Player No."] == p["player_no"]) & (game_data["Team"] == team)]
                val = float(int(pg["3PTM"].sum()) if not pg.empty else 0)
                rows.append({"name": p["label"], "team": team, "stat_name": "3PTM", "stat_display": f"{int(val)}", "stat_value": val})
            elif stat_category == "efficiency":
                val = float(stats.get("efficiency", {}).get("average", 0.0))
                rows.append({"name": p["label"], "team": team, "stat_name": "EFF", "stat_display": f"{val:.1f}", "stat_value": val})

        rows.sort(key=lambda x: x.get("stat_value", 0), reverse=True)
        return rows[:top_n]

    def _best_player_on_team(self, team: str) -> Optional[Dict[str, Any]]:
        """Pick the best player on a team using efficiency per game as primary signal."""
        players = [p for p in data_manager.get_all_players() if p.get("team") == team]
        best = None
        for p in players:
            profile = data_manager.get_player_profile(p["player_no"], p["team"])
            if "error" in profile:
                continue
            eff = profile.get("stats", {}).get("efficiency", {}).get("average", 0.0)
            ppg = profile.get("stats", {}).get("points", {}).get("average", 0.0)
            score = float(eff) * 10 + float(ppg)  # weighted
            if best is None or score > best["score"]:
                best = {
                    "label": p["label"],
                    "team": team,
                    "ppg": float(ppg),
                    "eff": float(eff),
                    "strengths": profile.get("strengths", []),
                    "weaknesses": profile.get("weaknesses", []),
                    "score": score,
                }
        return best

    def _format_leaderboard(self, title: str, rows: List[Dict[str, Any]]) -> str:
        # Optional: include a definition for the stat being displayed
        stat_definitions = {
            "PPG": "Points Per Game (PPG) = total points ÷ games played.",
            "RPG": "Rebounds Per Game (RPG) = total rebounds ÷ games played.",
            "APG": "Assists Per Game (APG) = total assists ÷ games played.",
            "FG%": "Field Goal % (FG%) = field goals made ÷ field goals attempted.",
            "3P%": "Three-Point % (3P%) = three-pointers made ÷ three-pointers attempted.",
            "3PTM": "3PT Made (3PTM) = total three-pointers made.",
            "EFF": "Efficiency = a summary stat that rewards points/rebounds/assists/steals/blocks and penalizes missed shots and turnovers (per game here).",
        }

        lines = [f"### 🏆 {title}", ""]
        if rows:
            stat_key = rows[0].get("stat_name")
            if stat_key and stat_key in stat_definitions:
                lines.append(f"**Definition:** {stat_definitions[stat_key]}")
                lines.append("")
        for i, r in enumerate(rows, 1):
            lines.append(f"**{i}. {r['name']}** ({r['team']})")
            if "stat_name" in r and "stat_display" in r:
                lines.append(f"   {r['stat_name']}: {r['stat_display']}")
            elif "stat_display" in r:
                lines.append(f"   {r['stat_display']}")
            lines.append("")
        return "\n".join(lines).rstrip()

    def _top5_all_categories(self, team: Optional[str] = None) -> str:
        """Return top 5 leaderboards across common categories (league-wide or within team)."""
        categories = [
            ("Top Scorers (PPG)", "points"),
            ("Top Field Goal %", "fg_pct"),
            ("Top 3PT Made", "three_point"),
            ("Top Rebounders (RPG)", "rebounds"),
            ("Top Playmakers (APG)", "assists"),
            ("Top Efficiency", "efficiency"),
        ]

        parts = []
        scope_label = f"{team} team" if team else "League"
        parts.append(f"## Top 5 Leaders — {scope_label}")
        parts.append("")

        if team:
            # Build within-team leaderboards using player profiles + game totals
            game_data = data_manager.load_player_data()
            team_players = [p for p in data_manager.get_all_players() if p.get("team") == team]

            def team_rows(stat_cat: str) -> List[Dict[str, Any]]:
                rows = []
                for p in team_players:
                    prof = data_manager.get_player_profile(p["player_no"], p["team"])
                    if "error" in prof:
                        continue
                    stats = prof.get("stats", {})
                    if stat_cat == "points":
                        val = stats.get("points", {}).get("average", 0.0)
                        rows.append({"name": p["label"], "team": team, "stat_name": "PPG", "stat_display": f"{float(val):.1f}" , "stat_value": float(val)})
                    elif stat_cat == "rebounds":
                        val = stats.get("rebounds", {}).get("average", 0.0)
                        rows.append({"name": p["label"], "team": team, "stat_name": "RPG", "stat_display": f"{float(val):.1f}", "stat_value": float(val)})
                    elif stat_cat == "assists":
                        val = stats.get("assists", {}).get("average", 0.0)
                        rows.append({"name": p["label"], "team": team, "stat_name": "APG", "stat_display": f"{float(val):.1f}", "stat_value": float(val)})
                    elif stat_cat == "fg_pct":
                        val = stats.get("shooting", {}).get("fg_pct", 0.0)
                        rows.append({"name": p["label"], "team": team, "stat_name": "FG%", "stat_display": f"{float(val):.1%}", "stat_value": float(val)})
                    elif stat_cat == "three_point":
                        pg = game_data[(game_data["Player No."] == p["player_no"]) & (game_data["Team"] == team)]
                        val = int(pg["3PTM"].sum()) if not pg.empty else 0
                        rows.append({"name": p["label"], "team": team, "stat_name": "3PTM", "stat_display": f"{val}", "stat_value": float(val)})
                    elif stat_cat == "efficiency":
                        val = stats.get("efficiency", {}).get("average", 0.0)
                        rows.append({"name": p["label"], "team": team, "stat_name": "EFF", "stat_display": f"{float(val):.1f}", "stat_value": float(val)})
                rows.sort(key=lambda x: x.get("stat_value", 0), reverse=True)
                return rows[:5]

            for title, cat in categories:
                parts.append(self._format_leaderboard(title, team_rows(cat)))
                parts.append("")
        else:
            for title, cat in categories:
                parts.append(self._format_leaderboard(title, self._get_league_leaders(cat, 5)))
                parts.append("")

        return "\n".join(parts).rstrip()
    
    def get_personalized_feedback(self, player_profile: Dict[str, Any]) -> str:
        """
        Generate personalized coaching feedback using rules
        """
        if "error" in player_profile:
            return "Player data not available."
        
        stats = player_profile.get("stats", {})
        strengths = player_profile.get("strengths", [])
        weaknesses = player_profile.get("weaknesses", [])
        advanced_stats = player_profile.get("advanced_stats", {})
        
        feedback_parts = []
        
        # Header
        feedback_parts.append(f"## Coaching Analysis for Player {player_profile.get('player_no')} ({player_profile.get('team')})")
        feedback_parts.append("")
        feedback_parts.append(f"Based on {player_profile.get('total_games')} games played, here's your personalized coaching analysis:")
        feedback_parts.append("")
        
        # Strengths section
        if strengths:
            feedback_parts.append("### ✅ Your Strengths")
            feedback_parts.append("")
            for strength in strengths:
                feedback_parts.append(f"- **{strength}**")
                
                # Add specific feedback for each strength
                if "Scoring" in strength or "scoring" in strength:
                    avg_pts = stats.get('points', {}).get('average', 0)
                    if avg_pts >= 15:
                        feedback_parts.append(f"  - You're averaging {avg_pts:.1f} points per game - excellent offensive production!")
                        feedback_parts.append(f"  - Use your scoring ability to draw defenders and create opportunities for teammates")
                elif "Rebounding" in strength or "rebounding" in strength:
                    avg_reb = stats.get('rebounds', {}).get('average', 0)
                    feedback_parts.append(f"  - Your {avg_reb:.1f} rebounds per game show strong court positioning")
                    feedback_parts.append(f"  - Continue boxing out and tracking the ball off the rim")
                elif "Passing" in strength or "playmaking" in strength:
                    avg_ast = stats.get('assists', {}).get('average', 0)
                    feedback_parts.append(f"  - With {avg_ast:.1f} assists per game, you're an effective playmaker")
                    feedback_parts.append(f"  - Keep looking for cutters and open shooters")
            feedback_parts.append("")
        
        # Weaknesses section with actionable advice
        if weaknesses:
            feedback_parts.append("### 🎯 Areas for Improvement")
            feedback_parts.append("")
            for weakness in weaknesses:
                feedback_parts.append(f"- **{weakness}**")
                
                # Provide specific drills and advice using drill library
                if "Turnover" in weakness or "Ball control" in weakness:
                    avg_tov = stats.get('turnovers', {}).get('average', 0)
                    feedback_parts.append(f"  - Currently averaging {avg_tov:.1f} turnovers per game")
                    
                    # Get specific drills from library
                    dribbling_drills = drill_library.get_drills_for_category("dribbling")
                    for i, drill in enumerate(dribbling_drills[:3], 1):  # Top 3 dribbling drills
                        feedback_parts.append(f"  - **Drill {i}**: {drill['name']} - {drill['description']}")
                        feedback_parts.append(f"    Duration: {drill['duration']}")
                    
                    feedback_parts.append(f"  - **Game tip**: Slow down when making decisions, especially in traffic")
                    
                elif "Shooting" in weakness or "percentage" in weakness:
                    fg_pct = stats.get('shooting', {}).get('fg_pct', 0)
                    three_pct = stats.get('shooting', {}).get('three_pct', 0)
                    feedback_parts.append(f"  - Current shooting: FG {fg_pct:.1%}, 3PT {three_pct:.1%}")
                    
                    # Get specific shooting drills from library
                    shooting_drills = drill_library.get_drills_for_category("shooting")
                    for i, drill in enumerate(shooting_drills[:3], 1):  # Top 3 shooting drills
                        feedback_parts.append(f"  - **Drill {i}**: {drill['name']} - {drill['description']}")
                        feedback_parts.append(f"    Duration: {drill['duration']}")
                    
                elif "Rebounding" in weakness:
                    avg_reb = stats.get('rebounds', {}).get('average', 0)
                    feedback_parts.append(f"  - Current average: {avg_reb:.1f} rebounds per game")
                    
                    # Get specific rebounding drills from library
                    rebounding_drills = drill_library.get_drills_for_category("rebounding")
                    for i, drill in enumerate(rebounding_drills[:2], 1):  # Top 2 rebounding drills
                        feedback_parts.append(f"  - **Drill {i}**: {drill['name']} - {drill['description']}")
                        feedback_parts.append(f"    Duration: {drill['duration']}")
                    
                    feedback_parts.append(f"  - **Game tip**: Position yourself between opponent and basket before shot goes up")
                    
                elif "Playmaking" in weakness or "assists" in weakness:
                    avg_ast = stats.get('assists', {}).get('average', 0)
                    feedback_parts.append(f"  - Current average: {avg_ast:.1f} assists per game")
                    
                    # Get specific passing drills from library
                    passing_drills = drill_library.get_drills_for_category("passing")
                    for i, drill in enumerate(passing_drills[:2], 1):  # Top 2 passing drills
                        feedback_parts.append(f"  - **Drill {i}**: {drill['name']} - {drill['description']}")
                        feedback_parts.append(f"    Duration: {drill['duration']}")
                    
                    feedback_parts.append(f"  - **Game tip**: Keep your head up and scan the court for open teammates")
                
                feedback_parts.append("")
        
        # Overall recommendations
        feedback_parts.append("### 💡 Overall Recommendations")
        feedback_parts.append("")
        
        # Shooting recommendations
        fg_pct = stats.get('shooting', {}).get('fg_pct', 0)
        if fg_pct < 0.40:
            feedback_parts.append("1. **Focus on shot selection**: Work on taking higher-percentage shots. Practice finishing at the rim and taking open shots within your range.")
        elif fg_pct >= 0.45:
            feedback_parts.append("1. **Maintain efficient shooting**: Your field goal percentage is strong. Continue taking quality shots and keep practicing.")
        else:
            feedback_parts.append("1. **Balance shot quality and quantity**: Look for opportunities to improve your field goal percentage through better shot selection.")
        
        # Efficiency recommendations
        efficiency = stats.get('efficiency', {}).get('average', 0)
        if efficiency < 10:
            feedback_parts.append("2. **Improve overall efficiency**: Focus on reducing turnovers and improving shot selection. Every possession matters.")
        elif efficiency >= 15:
            feedback_parts.append("2. **Maintain high efficiency**: You're playing efficient basketball. Keep making smart decisions on both ends of the court.")
        else:
            feedback_parts.append("2. **Continue building efficiency**: You're on the right track. Look for small improvements in decision-making.")
        
        # Balance recommendations
        if strengths and weaknesses:
            feedback_parts.append("3. **Build on strengths while addressing weaknesses**: Use your strengths to create advantages while actively working on your areas for improvement during practice.")
        
        feedback_parts.append("")
        feedback_parts.append("### 📊 Advanced Metrics")
        if advanced_stats:
            ast_tov = advanced_stats.get('ast_tov_ratio', 0)
            ts_pct = advanced_stats.get('ts_percentage', 0)
            reb_pct = advanced_stats.get('reb_percentage', 0)
            
            feedback_parts.append(f"- **Assist/Turnover Ratio**: {ast_tov:.2f} - {'Excellent playmaking!' if ast_tov >= 2.0 else 'Room for improvement in ball control'}")
            feedback_parts.append(f"- **True Shooting %**: {ts_pct:.1f}% - {'Efficient scorer!' if ts_pct >= 50 else 'Focus on shot quality'}")
            feedback_parts.append(f"- **Rebound %**: {reb_pct:.1f}% - {'Strong rebounder!' if reb_pct >= 10 else 'Work on positioning and timing'}")
        
        return "\n".join(feedback_parts)
    
    def _get_league_leaders(self, stat_category: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """Get top performers in a specific category across all players"""
        try:
            game_data = data_manager.load_player_data()
            advanced_stats = data_manager.load_advanced_stats()
            players = data_manager.get_all_players()
            
            leader_data = []
            
            for player in players:
                profile = data_manager.get_player_profile(player['player_no'], player['team'])
                if "error" in profile:
                    continue
                
                stats = profile.get("stats", {})
                player_info = {
                    "name": player['label'],
                    "player_no": player['player_no'],
                    "team": player['team']
                }
                
                # Map stat categories to actual stats
                if stat_category == "fg_pct" or stat_category == "field goal":
                    player_info["stat_value"] = stats.get('shooting', {}).get('fg_pct', 0)
                    player_info["stat_display"] = f"{player_info['stat_value']:.1%}"
                    player_info["stat_name"] = "Field Goal %"
                elif stat_category == "three_point" or stat_category == "3pt" or stat_category == "3ptm":
                    # Calculate total 3PTM from game data
                    player_games = game_data[(game_data['Player No.'] == player['player_no']) & (game_data['Team'] == player['team'])]
                    total_3ptm = int(player_games['3PTM'].sum()) if not player_games.empty else 0
                    player_info["stat_value"] = total_3ptm
                    player_info["stat_display"] = f"{total_3ptm}"
                    player_info["stat_name"] = "Total 3PT Made"
                elif stat_category == "three_pct" or stat_category == "3pt_pct":
                    player_info["stat_value"] = stats.get('shooting', {}).get('three_pct', 0)
                    player_info["stat_display"] = f"{player_info['stat_value']:.1%}"
                    player_info["stat_name"] = "Three-Point %"
                elif stat_category == "points" or stat_category == "scoring":
                    player_info["stat_value"] = stats.get('points', {}).get('average', 0)
                    player_info["stat_display"] = f"{player_info['stat_value']:.1f} PPG"
                    player_info["stat_name"] = "Points Per Game"
                elif stat_category == "rebounds" or stat_category == "rebounding":
                    player_info["stat_value"] = stats.get('rebounds', {}).get('average', 0)
                    player_info["stat_display"] = f"{player_info['stat_value']:.1f} RPG"
                    player_info["stat_name"] = "Rebounds Per Game"
                elif stat_category == "assists":
                    player_info["stat_value"] = stats.get('assists', {}).get('average', 0)
                    player_info["stat_display"] = f"{player_info['stat_value']:.1f} APG"
                    player_info["stat_name"] = "Assists Per Game"
                elif stat_category == "efficiency":
                    player_info["stat_value"] = stats.get('efficiency', {}).get('average', 0)
                    player_info["stat_display"] = f"{player_info['stat_value']:.1f}"
                    player_info["stat_name"] = "Efficiency"
                else:
                    continue
                
                leader_data.append(player_info)
            
            # Sort by stat_value (descending)
            leader_data.sort(key=lambda x: x['stat_value'], reverse=True)
            
            return leader_data[:top_n]
        except Exception as e:
            return []
    
    def get_ai_response(self, user_question: str, player_profile: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate response to user question using rules and templates
        """
        question_lower = user_question.lower()
        
        # Initialize response
        response_parts = []
        
        # League-wide statistics questions (when no player profile is selected)
        if player_profile is None:
            team = self._find_team_in_question(question_lower)

            # Coach/scout: team report
            if team and any(k in question_lower for k in ["strength", "weakness", "scout", "report", "breakdown"]):
                return self._team_scout_report(team)

            # Coach/scout: best player on a team
            if team and any(k in question_lower for k in ["best player", "best on", "top player", "mvp"]):
                best = self._best_player_on_team(team)
                if not best:
                    return f"I couldn't determine the best player on {team} from the data."
                lines = []
                lines.append(f"### 🏀 Best player on {team}")
                lines.append("")
                lines.append(f"**{best['label']}**")
                lines.append(f"- PPG: {best['ppg']:.1f}")
                lines.append(f"- Efficiency: {best['eff']:.1f}")
                lines.append("")
                lines.append("**Strengths:**")
                for s in (best.get("strengths") or [])[:5]:
                    lines.append(f"- {s}")
                lines.append("")
                lines.append("**Weaknesses:**")
                for w in (best.get("weaknesses") or [])[:5]:
                    lines.append(f"- {w}")
                return "\n".join(lines)

            # "Top 5 in each category" (league or team)
            if any(k in question_lower for k in ["top 5 in each", "top five in each", "top 5 each", "top 5 all", "leaders in each"]):
                return self._top5_all_categories(team=team)

            # Check for "who is best", "most", "top" type questions
            # Also simpler queries like "best FG shooter" or "most 3pt made"
            is_league_question = (any(word in question_lower for word in ["who", "which player"]) and 
                                any(word in question_lower for word in ["best", "most", "top", "leader"])) or \
                                (any(word in question_lower for word in ["best", "most", "top"]) and
                                any(word in question_lower for word in ["fg", "field goal", "3pt", "three-point", "points", "rebound", "assist", "efficiency"]))
            
            if is_league_question:
                # If a team is mentioned, answer within that team (top 5) for the asked category
                if team:
                    if any(word in question_lower for word in ["fg", "field goal", "fg%", "field goal percentage", "shooting percentage"]):
                        return self._format_leaderboard(f"Top Field Goal Shooters — {team}", self._get_team_leaders(team, "fg_pct", 5))
                    if any(word in question_lower for word in ["3pt", "three-point", "3-point", "3pt made", "threes made"]):
                        if "percentage" in question_lower or "%" in question_lower or "pct" in question_lower:
                            return self._format_leaderboard(f"Top Three-Point % — {team}", self._get_team_leaders(team, "three_pct", 5))
                        return self._format_leaderboard(f"Most 3PT Made — {team}", self._get_team_leaders(team, "three_point", 5))
                    if any(word in question_lower for word in ["points", "scoring", "scorer", "ppg"]):
                        return self._format_leaderboard(f"Top Scorers — {team}", self._get_team_leaders(team, "points", 5))
                    if any(word in question_lower for word in ["rebound", "rebounds", "rpg"]):
                        return self._format_leaderboard(f"Top Rebounders — {team}", self._get_team_leaders(team, "rebounds", 5))
                    if any(word in question_lower for word in ["assists", "passing", "playmaking", "apg"]):
                        return self._format_leaderboard(f"Top Playmakers — {team}", self._get_team_leaders(team, "assists", 5))
                    if any(word in question_lower for word in ["efficiency", "efficient"]):
                        return self._format_leaderboard(f"Most Efficient — {team}", self._get_team_leaders(team, "efficiency", 5))
                    # If we can't tell which category, give a scout report
                    return self._team_scout_report(team)

                # Field goal shooting questions
                if any(word in question_lower for word in ["fg", "field goal", "fg%", "field goal percentage", "shooting percentage"]):
                    leaders = self._get_league_leaders("fg_pct", 5)
                    if leaders:
                        return self._format_leaderboard("Top Field Goal Shooters", leaders)
                
                # Three-point made questions
                elif any(word in question_lower for word in ["3pt", "three-point", "3-point", "3pt made", "threes made"]):
                    if "percentage" in question_lower or "%" in question_lower or "pct" in question_lower:
                        leaders = self._get_league_leaders("three_pct", 5)
                        stat_label = "Three-Point %"
                    else:
                        leaders = self._get_league_leaders("three_point", 5)
                        stat_label = "Total 3-Pointers Made"
                    
                    if leaders:
                        return self._format_leaderboard(f"Top {stat_label} Leaders", leaders)
                
                # Points/scoring questions
                elif any(word in question_lower for word in ["points", "scoring", "scorer", "ppg"]):
                    leaders = self._get_league_leaders("points", 5)
                    if leaders:
                        return self._format_leaderboard("Top Scorers", leaders)
                
                # Rebounding questions
                elif any(word in question_lower for word in ["rebound", "rebounds", "rpg"]):
                    leaders = self._get_league_leaders("rebounds", 5)
                    if leaders:
                        return self._format_leaderboard("Top Rebounders", leaders)
                
                # Assists questions
                elif any(word in question_lower for word in ["assists", "passing", "playmaking", "apg"]):
                    leaders = self._get_league_leaders("assists", 5)
                    if leaders:
                        return self._format_leaderboard("Top Playmakers", leaders)
                
                # Efficiency questions
                elif any(word in question_lower for word in ["efficiency", "efficient"]):
                    leaders = self._get_league_leaders("efficiency", 5)
                    if leaders:
                        return self._format_leaderboard("Most Efficient Players", leaders)
        
        # Shooting-related questions
        if any(word in question_lower for word in ["shoot", "shooting", "three-point", "3-point", "field goal", "form shooting", "catch and shoot"]):
            if player_profile:
                stats = player_profile.get("stats", {})
                fg_pct = stats.get('shooting', {}).get('fg_pct', 0)
                three_pct = stats.get('shooting', {}).get('three_pct', 0)
                
                response_parts.append("### Shooting Improvement Drills")
                response_parts.append("")
                
                # Check for specific drill requests
                if "form shooting" in question_lower:
                    drill = drill_library.get_drill_by_name("Form Shooting")
                    if drill:
                        response_parts.append(drill_library.format_drill(drill))
                elif "catch and shoot" in question_lower or "catch-and-shoot" in question_lower:
                    drill = drill_library.get_drill_by_name("Catch and Shoot")
                    if drill:
                        response_parts.append(drill_library.format_drill(drill))
                elif "three-point" in question_lower or "3-point" in question_lower:
                    drill = drill_library.get_drill_by_name("Three-Point Shooting")
                    if drill:
                        response_parts.append(drill_library.format_drill(drill))
                else:
                    shooting_drills = drill_library.get_drills_for_category("shooting")
                    for i, drill in enumerate(shooting_drills[:4], 1):
                        response_parts.append(f"**{i}. {drill['name']}** ({drill['difficulty']})")
                        response_parts.append(f"   {drill['description']}")
                        response_parts.append(f"   Duration: {drill['duration']}")
                        response_parts.append("")
                    
                    if fg_pct < 0.40:
                        response_parts.append("**Quick Tip:** Focus on shot selection - take open shots within your range")
            else:
                shooting_drills = drill_library.get_drills_for_category("shooting")
                response_parts.append("**Recommended Shooting Drills:**")
                for i, drill in enumerate(shooting_drills[:3], 1):
                    response_parts.append(f"{i}. **{drill['name']}** - {drill['description']}")
                response_parts.append("")
                response_parts.append("Ask for a specific drill to see detailed instructions!")
        
        # Rebounding questions
        elif any(word in question_lower for word in ["rebound", "rebounding", "board"]):
            if player_profile:
                avg_reb = player_profile.get('stats', {}).get('rebounds', {}).get('average', 0)
                strengths = player_profile.get('strengths', [])
                
                # Add strengths if rebounding is a strength
                if any("rebounding" in s.lower() for s in strengths):
                    response_parts.append("**✅ Rebounding is one of your strengths!**")
                    response_parts.append("")
                
                response_parts.append(f"You're averaging {avg_reb:.1f} rebounds per game.")
                response_parts.append("")
                if avg_reb < 5:
                    response_parts.append("**To improve rebounding, try these drills:**")
                else:
                    response_parts.append("**To maintain strong rebounding, practice these drills:**")
            else:
                response_parts.append("**Rebounding Improvement Drills:**")
            
            response_parts.append("")
            rebounding_drills = drill_library.get_drills_for_category("rebounding")
            for i, drill in enumerate(rebounding_drills[:3], 1):
                response_parts.append(f"**{i}. {drill['name']}** ({drill['difficulty']}, {drill['duration']})")
                response_parts.append(f"   {drill['description']}")
                response_parts.append("")
            
            response_parts.append("💡 **Key Tips:** Box out positioning, watch the ball's trajectory, pursue aggressively!")
            response_parts.append("Ask for a specific drill name to see detailed instructions!")
        
        # Turnover/ball control questions
        elif any(word in question_lower for word in ["turnover", "ball control", "handle", "dribble", "right hand", "left hand"]):
            if player_profile:
                avg_tov = player_profile.get('stats', {}).get('turnovers', {}).get('average', 0)
                strengths = player_profile.get('strengths', [])
                
                # Check if player has playmaking as a strength despite turnovers
                if any("passing" in s.lower() or "playmaking" in s.lower() for s in strengths):
                    response_parts.append("**✅ Playmaking is one of your strengths!** Focus on reducing turnovers to maximize this.")
                    response_parts.append("")
                
                response_parts.append(f"You're averaging {avg_tov:.1f} turnovers per game.")
                response_parts.append("")
            
            # Check for specific drill requests
            if "right hand" in question_lower:
                drill = drill_library.get_drill_by_name("Right Hand Dribbling")
                if drill:
                    response_parts.append(drill_library.format_drill(drill))
            elif "left hand" in question_lower:
                drill = drill_library.get_drill_by_name("Left Hand Dribbling")
                if drill:
                    response_parts.append(drill_library.format_drill(drill))
            elif "crossover" in question_lower:
                drill = drill_library.get_drill_by_name("Crossover Dribble Drill")
                if drill:
                    response_parts.append(drill_library.format_drill(drill))
            else:
                response_parts.append("**Recommended Dribbling Drills:**")
                response_parts.append("")
                dribbling_drills = drill_library.get_drills_for_category("dribbling")
                for i, drill in enumerate(dribbling_drills[:4], 1):
                    response_parts.append(f"**{i}. {drill['name']}** ({drill['difficulty']}, {drill['duration']})")
                    response_parts.append(f"   {drill['description']}")
                    response_parts.append("")
                response_parts.append("💡 **Tip:** Ask for a specific drill name to see detailed step-by-step instructions!")
        
        # General improvement or questions about strengths
        elif any(word in question_lower for word in ["improve", "better", "help", "advice", "drills", "practice", "what should i", "strength", "strong", "good at"]):
            # If asking specifically about strengths
            if any(word in question_lower for word in ["strength", "strong", "good at", "best at", "what am i good"]):
                if player_profile:
                    strengths = player_profile.get('strengths', [])
                    if strengths:
                        response_parts.append("### ✅ Your Strengths")
                        response_parts.append("")
                        stats = player_profile.get("stats", {})
                        for strength in strengths:
                            response_parts.append(f"- **{strength}**")
                            
                            # Add context for each strength
                            if "Scoring" in strength or "scoring" in strength:
                                avg_pts = stats.get('points', {}).get('average', 0)
                                response_parts.append(f"  • Averaging {avg_pts:.1f} points per game")
                                response_parts.append(f"  • Use this to draw defenders and create opportunities for teammates")
                            elif "Rebounding" in strength or "rebounding" in strength:
                                avg_reb = stats.get('rebounds', {}).get('average', 0)
                                response_parts.append(f"  • {avg_reb:.1f} rebounds per game - strong court positioning")
                            elif "Passing" in strength or "playmaking" in strength:
                                avg_ast = stats.get('assists', {}).get('average', 0)
                                response_parts.append(f"  • {avg_ast:.1f} assists per game - effective playmaking")
                            elif "Three-point" in strength or "three-point" in strength:
                                three_pct = stats.get('shooting', {}).get('three_pct', 0)
                                response_parts.append(f"  • {three_pct:.1%} three-point shooting - keep it up!")
                            elif "Shooting" in strength or "shooting" in strength:
                                fg_pct = stats.get('shooting', {}).get('fg_pct', 0)
                                response_parts.append(f"  • {fg_pct:.1%} field goal percentage - efficient scorer")
                            response_parts.append("")
                        
                        response_parts.append("💡 **Tip:** Build on these strengths while working on areas for improvement!")
                    else:
                        response_parts.append("Keep working hard! Focus on fundamental skills like shooting, ball handling, and defense.")
                    
                    if response_parts:
                        return "\n".join(response_parts)
            
            # General improvement questions
            response_parts.append("Here are personalized improvement recommendations:")
            response_parts.append("")
            
            if player_profile:
                strengths = player_profile.get('strengths', [])
                weaknesses = player_profile.get('weaknesses', [])
                
                # Add strengths section to general improvement responses
                if strengths:
                    response_parts.append("**✅ Your Strengths:**")
                    for strength in strengths[:3]:  # Top 3 strengths
                        response_parts.append(f"- {strength}")
                    response_parts.append("")
                
                if weaknesses:
                    response_parts.append("**Based on your stats, focus on these areas:**")
                    for weakness in weaknesses[:3]:  # Top 3 weaknesses
                        response_parts.append(f"- {weakness}")
                    
                    # Get recommended drills for weaknesses
                    response_parts.append("")
                    response_parts.append("**Recommended Drills:**")
                    response_parts.append("")
                    
                    for weakness in weaknesses[:2]:  # Top 2 weaknesses
                        drills = drill_library.get_drills_for_weakness(weakness)
                        if drills:
                            response_parts.append(f"**For {weakness}:**")
                            for drill in drills[:2]:  # Top 2 drills per weakness
                                response_parts.append(f"- **{drill['name']}** ({drill['difficulty']}, {drill['duration']})")
                                response_parts.append(f"  {drill['description']}")
                            response_parts.append("")
                    
                    response_parts.append("💡 **Tip:** Ask for a specific drill name like 'Right Hand Dribbling' to see detailed instructions!")
                else:
                    response_parts.append("**Key areas to work on:**")
                    response_parts.append("1. **Practice fundamentals daily** - Shooting, dribbling, passing")
                    response_parts.append("2. **Study game film** - Watch your games and identify patterns")
                    response_parts.append("3. **Conditioning** - Basketball requires endurance and agility")
                    response_parts.append("")
                    response_parts.append("**Popular Drills to Try:**")
                    dribbling_drills = drill_library.get_drills_for_category("dribbling")[:2]
                    shooting_drills = drill_library.get_drills_for_category("shooting")[:2]
                    for drill in dribbling_drills + shooting_drills:
                        response_parts.append(f"- **{drill['name']}** ({drill['difficulty']})")
            else:
                response_parts.append("**Key areas to work on:**")
                response_parts.append("1. **Practice fundamentals daily** - Shooting, dribbling, passing")
                response_parts.append("2. **Study game film** - Watch your games and identify patterns")
                response_parts.append("3. **Conditioning** - Basketball requires endurance and agility")
                response_parts.append("")
                response_parts.append("**Popular Drills to Try:**")
                popular_drills = [
                    drill_library.get_drill_by_name("Right Hand Dribbling"),
                    drill_library.get_drill_by_name("Form Shooting"),
                    drill_library.get_drill_by_name("Chest Pass Drill")
                ]
                for drill in popular_drills:
                    if drill:
                        response_parts.append(f"- **{drill['name']}** ({drill['difficulty']}, {drill['duration']})")
                        response_parts.append(f"  {drill['description']}")
                response_parts.append("")
                response_parts.append("💡 **Tip:** Ask for a specific drill name to see detailed instructions!")
        
        # Drill-specific requests (catch all drill name queries)
        elif any(drill_name.lower() in question_lower for drill_name in [
            "right hand dribbling", "left hand dribbling", "two-ball dribbling",
            "crossover", "between the legs", "behind the back",
            "form shooting", "catch and shoot", "pull-up", "three-point", "free throw",
            "chest pass", "bounce pass", "outlet pass", "skip pass",
            "box out", "tip drill", "reaction rebound",
            "defensive slide", "close-out", "one-on-one defense",
            "pivot", "triple threat", "suicide runs"
        ]):
            # Try to find matching drill
            found_drill = None
            for category_drills in drill_library.drills.values():
                for drill in category_drills:
                    if drill["name"].lower() in question_lower:
                        found_drill = drill
                        break
                if found_drill:
                    break
            
            if found_drill:
                response_parts.append(drill_library.format_drill(found_drill))
            else:
                response_parts.append("I can help you find specific drills! Try asking:")
                response_parts.append("- 'Right Hand Dribbling'")
                response_parts.append("- 'Form Shooting'")
                response_parts.append("- 'Crossover Dribble Drill'")
                response_parts.append("- Or any drill name from our library")
        
        # Default response
        else:
            response_parts.append("I can help you with:")
            response_parts.append("- **Shooting improvement** - Try asking 'shooting drills'")
            response_parts.append("- **Rebounding tips** - Ask 'rebounding drills'")
            response_parts.append("- **Ball control and turnovers** - Ask 'dribbling drills'")
            response_parts.append("- **Specific drills** - Ask for drill names like 'Right Hand Dribbling'")
            response_parts.append("- **Coach / scout questions (All Players)** - Ask things like 'best player on Black team' or 'Black team strengths and weaknesses'")
            response_parts.append("- **Leaderboards (All Players)** - Ask 'best FG shooter', 'most 3PTs made', or 'top 5 in each category'")
            response_parts.append("")
            response_parts.append("**Try asking:**")
            response_parts.append("- 'How can I improve my shooting?'")
            response_parts.append("- 'What drills should I do?'")
            response_parts.append("- 'Show me the Right Hand Dribbling drill'")
            response_parts.append("- 'I need dribbling drills'")
            response_parts.append("- 'Who's the best player on Black team?'")
            response_parts.append("- 'Black team strengths and weaknesses'")
            response_parts.append("- 'Top 5 in each category'")
        
        return "\n".join(response_parts) if response_parts else "I'm here to help with your basketball training. What would you like to know?"

# Global instance
rule_based_assistant = RuleBasedAssistant()
