"""
GameChanger - AI-Powered Basketball Analytics for Youth Athletes
Main Streamlit application with homepage-first navigation
"""

import streamlit as st

# Page configuration MUST be first
st.set_page_config(
    page_title="GameChanger - Basketball Analytics",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import os
import pandas as pd
from data_manager import data_manager
from site_logger import logger
from ai_dashboard_integration import render_ai_chat_interface, render_3on3_ai_chat_interface
from drill_library import drill_library

# Custom CSS
st.markdown("""
    <style>
    /* Larger button text */
    .stButton > button {
        font-size: 1.35rem !important;
    }
    .hero-headline {
        font-size: 3.5rem;
        font-weight: 800;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .hero-subtext {
        font-size: 1.5rem;
        color: #4a4a6a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .mission-block {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 12px;
        margin: 2rem 0;
        font-size: 1.05rem;
        line-height: 1.7;
    }
    .footer-brand {
        text-align: center;
        color: #6c757d;
        font-size: 0.95rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #dee2e6;
    }
    /* Larger page headers and subtitles */
    h1, .stMarkdown h1 { font-size: 2.5rem !important; }
    h2, .stMarkdown h2 { font-size: 1.9rem !important; }
    h3, .stMarkdown h3 { font-size: 1.5rem !important; }
    .stCaptionContainer { font-size: 1.1rem !important; }
    /* Larger data (tables, metrics) */
    .stDataFrame td, .stDataFrame th, [data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th { font-size: 1.25rem !important; }
    /* 3on3 Player Dashboard - dark theme like NBA stats */
    .player-dash-3on3 { background: #1e1e1e !important; color: #e0e0e0 !important; padding: 1rem; border-radius: 8px; }
    .player-dash-3on3 table { width: 100%; border-collapse: collapse; background: #2d2d2d; }
    .player-dash-3on3 th { color: #b0b0b0; font-weight: 600; padding: 0.75rem; text-align: left; border-bottom: 1px solid #444; }
    .player-dash-3on3 td { padding: 0.75rem; border-bottom: 1px solid #3a3a3a; color: #e0e0e0; }
    .player-dash-3on3 .player-name { color: #5dade2 !important; font-weight: 500; }
    [data-testid="stMetricValue"] { font-size: 1.75rem !important; }
    [data-testid="stMetricLabel"] { font-size: 1.15rem !important; }
    .stSelectbox label { font-size: 1.15rem !important; }
    .stSelectbox [data-baseweb="select"] { font-size: 1.1rem !important; }
    </style>
""", unsafe_allow_html=True)


def _get_page():
    """Get current page from session state."""
    return st.session_state.get("current_page", "home")


def _set_page(page: str):
    st.session_state.current_page = page
    st.rerun()


def _get_season_num():
    """Get current season (1 or 2) from session state. 3on3 has its own page."""
    sel = st.session_state.get("season_rising_stars", "Season 1 Rising Stars")
    if sel == "Season 1 Rising Stars":
        return 1
    if sel == "Season 2 Rising Stars":
        return 2
    return 1


def _render_nav_buttons():
    """Render navigation at top, season switcher in right corner (only on Team Dashboard and Player Performance Report)."""
    page = _get_page()
    show_season = page in ("dashboard", "sample_report")
    left_cols, right_col = st.columns([4, 1])
    with left_cols:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🏠 Home", use_container_width=True) and page != "home":
                _set_page("home")
        with c2:
            if st.button("📊 Team Dashboard", use_container_width=True) and page != "dashboard":
                _set_page("dashboard")
        with c3:
            if st.button("📋 Player Performance Report", use_container_width=True) and page != "sample_report":
                _set_page("sample_report")
        with c4:
            if st.button("🏀 3 on 3 Tournament Dashboard", use_container_width=True) and page != "dashboard_3on3":
                _set_page("dashboard_3on3")
    with right_col:
        if show_season:
            st.selectbox(
                "Season",
                ["Season 1 Rising Stars", "Season 2 Rising Stars"],                         
                key="season_rising_stars",
                label_visibility="collapsed"
            )
    st.markdown("---")


def _render_footer():
    st.markdown(
        '<p class="footer-brand">GameChanger — AI-Powered Basketball Analytics for Youth Players</p>',
        unsafe_allow_html=True
    )


def show_homepage():
    """1️⃣ Homepage - Hook in 5 Seconds"""
    # Larger subtitle/paragraph text for main page (50% increase)
    st.markdown("""
        <style>
        .main p, .main .stMarkdown, .main [data-testid="stMarkdown"], .main ul, .main li { font-size: 1.5rem !important; line-height: 1.6 !important; }
        .main h2, .main .stMarkdown h2 { font-size: 2.2rem !important; }
        .main .stMetric [data-testid="stMetricValue"], .main .stMetric [data-testid="stMetricLabel"] { font-size: 1.5rem !important; }
        .main .stCaptionContainer { font-size: 1.3rem !important; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<h1 class="hero-headline">GameChanger</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-subtext">AI-Powered Basketball Analytics for Youth Athletes</p>',
        unsafe_allow_html=True
    )
    st.markdown('<p class="hero-subtext">Making performance data accessible to community leagues.</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏀 3 on 3 Basketball Tournament Dashboard", use_container_width=True, type="primary"):
            _set_page("dashboard_3on3")
    with col2:
        if st.button("📊 View Dashboard", use_container_width=True, type="primary"):
            _set_page("dashboard")
    with col3:
        if st.button("📋 See Player Performance Report", use_container_width=True, type="primary"):
            _set_page("sample_report")
    st.markdown("---")
    st.subheader("🏀 What Is GameChanger?")
    st.markdown(
        "GameChanger is a youth basketball analytics platform that tracks real game statistics and "
        "converts them into clear performance insights for players and coaches."
    )
    st.markdown(
        "By measuring points, rebounds, assists, shooting efficiency, and turnovers, GameChanger provides "
        "structured, data-driven feedback that helps athletes understand their strengths and areas for improvement."
    )

    st.markdown("---")
    st.subheader("📊 What We Track")
    st.markdown("- **Points**")
    st.markdown("- **Rebounds** (Offensive & Defensive)")
    st.markdown("- **Assists**")
    st.markdown("- **Three-Pointers Made**")
    st.markdown("- **Field Goals Made**")
    st.markdown("- **Blocks**")
    st.markdown("- **Turnovers**")
    st.markdown("- **Personal Fouls**")
    st.markdown("- **Shooting Percentages** (FT%, 3PT%, FG%)")
    st.markdown(
        "*GCIR (GameChanger Impact Rating) combines scoring efficiency (PPS), stats, and negative plays to measure overall game performance.*"
    )

    st.markdown("---")
    st.subheader("🧠 How It Works")
    st.markdown("1️⃣ Game stats are recorded live")
    st.markdown("2️⃣ Performance metrics are calculated")
    st.markdown("3️⃣ A GCIR (GameChanger Impact Rating) is generated")
    st.markdown("4️⃣ A player development report is created")
    st.markdown("*GameChanger turns raw statistics into meaningful insights.*")

    st.markdown("---")
    st.subheader("🏆 Live at the Met Schools 3x3 Tournament")
    st.markdown("GameChanger is being implemented at the Met Schools 3x3 Basketball Tournament.")
    st.markdown("- Players wear numbered pinnies")
    st.markdown("- Stats are tracked in real time")
    st.markdown("- Performance reports are generated after games")
    st.markdown("- Data is used to support youth development")

    img_path = "assets/tournament.jpg"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True, caption="Met Schools 3x3 Tournament")
    else:
        st.markdown(
            '<div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); height: 180px; '
            'border-radius: 12px; display: flex; align-items: center; justify-content: center; '
            'color: #1565c0; font-size: 1rem;">📸 Add tournament photo at assets/tournament.jpg</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("📈 Community Impact")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Funding Secured", "$1500")
    with col2:
        st.metric("Organizations", "2")
    with col3:
        st.metric("Youth Athletes Served", "50+")
    with col4:
        st.metric("Honorarium", "$1000")
    st.caption("Recognized with a $1000 Honorarium from North Forge")

    st.markdown("---")
    st.subheader("🚀 Vision")
    st.markdown(
        "The long-term goal of GameChanger is to expand youth access to performance analytics by:"
    )
    st.markdown("- Integrating video-based stat tracking")
    st.markdown("- Expanding to additional community leagues")
    st.markdown("- Building student-led analytics teams")
    _render_footer()


# 3 on 3 tournament: (Team, Player No.) -> display name (overrides "Player 1" etc.)
PLAYER_NAMES_3ON3 = {
    ("Oppahsnee", 1): "Reid",
    ("Oppahsnee", 2): "Tsering",
    ("Oppahsnee", 3): "Niko",
    ("Oppahsnee", 4): "Ethan K.",
    ("Oppahsnee", 5): "Jeesh",
    ("Los Blancos", 1): "Gurfateh",
    ("Los Blancos", 2): "Aashman",
    ("Los Blancos", 3): "Gurshan",
    ("Los Blancos", 4): "Jayelle",
    ("Swaggers", 8): "James",
    ("Swaggers", 10): "Mehtab",
    ("Swaggers", 11): "Archer",
    ("Swaggers", 4): "Mason",
    ("Bau Bau", 1): "Javier",
    ("Bau Bau", 12): "Ethan M.",
    ("Bau Bau", 7): "Kade",
    ("Bau Bau", 4): "Sacha",
    ("Bau Bau", 3): "Yohann",
    ("Basketball Bandits", 2): "Julian",
    ("Basketball Bandits", 4): "Ben",
    ("Basketball Bandits", 5): "Dorian",
    ("Basketball Bandits", 1): "Corban",
    ("DD", 1): "Kyle",
    ("DD", 2): "Dom",
    ("DD", 3): "Kirby",
    ("DD", 67): "Replacement Player",
    ("Uncs", 1): "Nathan",
    ("Uncs", 2): "Stan",
    ("Uncs", 3): "Cohen",
    ("Uncs", 4): "Dom (Replacement Player)",
}


def _get_3on3_display_name(team: str, player_no, fallback: str) -> str:
    """Return mapped name for 3on3 (Team, Player No.) or fallback."""
    try:
        key = (str(team).strip(), int(player_no))
        return PLAYER_NAMES_3ON3.get(key, fallback)
    except (ValueError, TypeError):
        return fallback


# Stat column tooltips for Player Dashboard (shown on hover)
STAT_TOOLTIPS = {
    "Name": "Player name and team",
    "Games": "Number of games played.",
    "Points": "Total points you scored in the game.",
    "Rebounds": "How many times you gained possession after a missed shot.",
    "Assists": "Passes that directly led to a teammate scoring.",
    "3PM": "Shots made from beyond the three-point line.",
    "FG Made": "Total shots made from the floor (2-point and 3-point shots).",
    "Blocks": "Shots you prevented by stopping the ball before it reached the basket.",
    "OREB": "Rebounds your team gets after your own team misses a shot.",
    "DREB": "Rebounds your team gets after the opponent misses a shot.",
    "Personal Fouls": "Illegal contact that can give the opponent free throws or possession.",
    "Turnovers": "Times you lost possession of the ball to the other team.",
    "FG%": "How efficient you are at making your shots overall.",
    "3PT%": "How often you make shots from long range.",
    "FT%": "How often you make uncontested free throw shots.",
    "GCIR": "GameChanger Impact Rating: (PTS×PPS) + 1.3(REB) + 1.5(AST) + 3(STL) + 2.5(BLK) + 0.7(OREB) − 1.5(TOV) − 0.8(PF). PPS = PTS/FGA (points per shot).",
    "GCMVP": "GameChanger MVP (Total games only, per-game avg): (4×PTS×(PTS/(FGA+0.44×FTA))) + 0.7(REB) + 1.2(AST) + 1.8(STL) + 1.5(BLK) − 2(TOV) − 0.7(PF).",
}


def show_live_dashboard():
    """2️⃣ Live Dashboard - Player Stats Table (Team Dashboard)"""
    st.header("📊 Team Dashboard")
    st.caption("Click “View Dashboard” on the homepage to see how it works.")

    season_num = _get_season_num()

    try:
        game_data = data_manager.load_player_data(season=season_num)
        advanced_stats = data_manager.load_advanced_stats(season=season_num)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        _render_footer()
        return

    totals = (
        game_data.groupby(["Player No.", "Team"], as_index=False)
        .agg(
            Games=("Game", "nunique"),
            PTS=("PTS", "sum"),
            REB=("REB", "sum"),
            AST=("AST", "sum"),
            ThreePTM=("3PTM", "sum"),
            FGM=("FGM", "sum"),
            BLK=("BLK", "sum"),
            OREB=("OREB", "sum"),
            DREB=("DREB", "sum"),
            PF=("PF", "sum"),
            TOV=("TOV", "sum"),
            FGA=("FGA", "sum"),
            ThreePA=("3PA", "sum"),
            FTM=("FTM", "sum"),
            FTA=("FTA", "sum"),
            STL=("STL", "sum"),
        )
    )
    # Coerce to numeric in case CSV read as object (e.g. on some hosts)
    for col in ["Games", "PTS", "REB", "AST", "ThreePTM", "FGM", "BLK", "OREB", "DREB", "PF", "TOV", "FGA", "ThreePA", "FTM", "FTA", "STL"]:
        if col in totals.columns:
            totals[col] = pd.to_numeric(totals[col], errors="coerce")
    games = totals["Games"].replace(0, pd.NA)
    totals["Points"] = (totals["PTS"] / games).round(1)
    totals["Rebounds"] = (totals["REB"] / games).round(1)
    totals["Assists"] = (totals["AST"] / games).round(1)
    totals["3PM"] = (totals["ThreePTM"] / games).round(1)
    totals["FG Made"] = (totals["FGM"] / games).round(1)
    totals["Blocks"] = (totals["BLK"] / games).round(1)
    totals["OREB"] = (totals["OREB"] / games).round(1)
    totals["DREB"] = (totals["DREB"] / games).round(1)
    totals["Personal Fouls"] = (totals["PF"] / games).round(1)
    totals["Turnovers"] = (totals["TOV"] / games).round(1)
    totals["FG%"] = pd.to_numeric(totals["FGM"] / totals["FGA"].replace(0, pd.NA) * 100, errors="coerce").round(1)
    totals["3PT%"] = pd.to_numeric(totals["ThreePTM"] / totals["ThreePA"].replace(0, pd.NA) * 100, errors="coerce").round(1)
    totals["FT%"] = pd.to_numeric(totals["FTM"] / totals["FTA"].replace(0, pd.NA) * 100, errors="coerce").round(1)
    # PPS = PTS/FGA (points per shot, when FGA > 0); GCIR = (PTS×PPS) + 1.3(REB) + 1.5(AST) + 3(STL) + 2.5(BLK) + 0.7(OREB) − 1.5(TOV) − 0.8(PF)
    _pps = totals["PTS"] / totals["FGA"].replace(0, pd.NA)
    _pps = _pps.fillna(0).astype(float)
    _gcir_total = (
        totals["PTS"] * _pps
        + 1.3 * totals["REB"] + 1.5 * totals["AST"]
        + 3 * totals["STL"] + 2.5 * totals["BLK"] + 0.7 * totals["OREB"]
        - 1.5 * totals["TOV"] - 0.8 * totals["PF"]
    )
    totals["GCIR"] = (_gcir_total / games).fillna(0).round(1)

    labels = advanced_stats[["Player No.", "Team", "Player_Team_Label"]].drop_duplicates()
    totals = totals.merge(labels, on=["Player No.", "Team"], how="left")
    totals["Name"] = totals["Player_Team_Label"].fillna(
        "Player " + totals["Player No."].astype(str) + " (" + totals["Team"].astype(str) + ")"
    )

    display_df = totals[[
        "Name", "Points", "Rebounds", "Assists", "3PM", "FG Made", "Blocks",
        "OREB", "DREB", "Personal Fouls", "Turnovers",
        "FG%", "3PT%", "FT%", "GCIR"
    ]].copy()
    # Format percentages to 1 decimal
    for pct_col in ["FG%", "3PT%", "FT%"]:
        if pct_col in display_df.columns:
            display_df[pct_col] = display_df[pct_col].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")

    column_config = {col: st.column_config.Column(col, help=STAT_TOOLTIPS.get(col, "")) for col in display_df.columns if STAT_TOOLTIPS.get(col)}
    st.dataframe(display_df, use_container_width=True, hide_index=True, column_config=column_config)

    # Optional bar chart (plotly optional for environments where it fails to import, e.g. some hosts)
    if st.checkbox("Show player comparison chart", value=False):
        try:
            import plotly.express as px
            fig = px.bar(
                display_df.sort_values("GCIR", ascending=True).tail(12),
                x="Name",
                y="GCIR",
                title="GCIR by Player",
                color="GCIR",
                color_continuous_scale="Blues",
            )
            fig.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.info("Chart is unavailable in this environment. The stats table above has the same data.")

    st.markdown("---")
    st.subheader("💡 AI Assistant")
    st.caption("Ask questions about performance, training, or game strategy.")
    render_ai_chat_interface(player_profile=None)

    _render_footer()


def _build_3on3_player_table(game_data: pd.DataFrame, advanced_stats: pd.DataFrame, include_gcmvp: bool = False) -> pd.DataFrame:
    """Build the standard player stats display table from game_data and advanced_stats. If include_gcmvp=True, add GCMVP column (for Total games only)."""
    totals = (
        game_data.groupby(["Player No.", "Team"], as_index=False)
        .agg(
            Games=("Game", "nunique"),
            PTS=("PTS", "sum"),
            REB=("REB", "sum"),
            AST=("AST", "sum"),
            ThreePTM=("3PTM", "sum"),
            FGM=("FGM", "sum"),
            BLK=("BLK", "sum"),
            OREB=("OREB", "sum"),
            DREB=("DREB", "sum"),
            PF=("PF", "sum"),
            TOV=("TOV", "sum"),
            FGA=("FGA", "sum"),
            ThreePA=("3PA", "sum"),
            FTM=("FTM", "sum"),
            FTA=("FTA", "sum"),
            STL=("STL", "sum"),
        )
    )
    for col in ["Games", "PTS", "REB", "AST", "ThreePTM", "FGM", "BLK", "OREB", "DREB", "PF", "TOV", "FGA", "ThreePA", "FTM", "FTA", "STL"]:
        if col in totals.columns:
            totals[col] = pd.to_numeric(totals[col], errors="coerce")
    games = totals["Games"].replace(0, pd.NA)
    totals["Points"] = (totals["PTS"] / games).round(1)
    totals["Rebounds"] = (totals["REB"] / games).round(1)
    totals["Assists"] = (totals["AST"] / games).round(1)
    totals["3PM"] = (totals["ThreePTM"] / games).round(1)
    totals["FG Made"] = (totals["FGM"] / games).round(1)
    totals["Blocks"] = (totals["BLK"] / games).round(1)
    totals["OREB"] = (totals["OREB"] / games).round(1)
    totals["DREB"] = (totals["DREB"] / games).round(1)
    totals["Personal Fouls"] = (totals["PF"] / games).round(1)
    totals["Turnovers"] = (totals["TOV"] / games).round(1)
    totals["FG%"] = pd.to_numeric(totals["FGM"] / totals["FGA"].replace(0, pd.NA) * 100, errors="coerce").round(1)
    totals["3PT%"] = pd.to_numeric(totals["ThreePTM"] / totals["ThreePA"].replace(0, pd.NA) * 100, errors="coerce").round(1)
    totals["FT%"] = pd.to_numeric(totals["FTM"] / totals["FTA"].replace(0, pd.NA) * 100, errors="coerce").round(1)
    # PPS = PTS/FGA (points per shot, when FGA > 0); GCIR = (PTS×PPS) + 1.3(REB) + 1.5(AST) + 3(STL) + 2.5(BLK) + 0.7(OREB) − 1.5(TOV) − 0.8(PF)
    _pps = totals["PTS"] / totals["FGA"].replace(0, pd.NA)
    _pps = _pps.fillna(0).astype(float)
    _gcir_total = (
        totals["PTS"] * _pps
        + 1.3 * totals["REB"] + 1.5 * totals["AST"]
        + 3 * totals["STL"] + 2.5 * totals["BLK"] + 0.7 * totals["OREB"]
        - 1.5 * totals["TOV"] - 0.8 * totals["PF"]
    )
    totals["GCIR"] = (_gcir_total / games).fillna(0).round(1)
    if include_gcmvp:
        # GCMVP numerator per player: ((4 × PTS × (PTS / (FGA + 0.44 × FTA))) + 0.7 × REB + 1.2 × AST
        # + 1.8 × STL + 1.5 × BLK − 2 × TOV − 0.7 × PF)
        _tsa = totals["FGA"] + 0.44 * totals["FTA"]
        _pps_mvp = (totals["PTS"] / _tsa.replace(0, pd.NA)).fillna(0).astype(float)
        _gcmvp_num = (
            4 * totals["PTS"] * _pps_mvp
            + 0.7 * totals["REB"]
            + 1.2 * totals["AST"]
            + 1.8 * totals["STL"]
            + 1.5 * totals["BLK"]
            - 2.0 * totals["TOV"]
            - 0.7 * totals["PF"]
        )
        totals["GCMVP"] = (_gcmvp_num / games).fillna(0).round(1)
    labels = advanced_stats[["Player No.", "Team", "Player_Team_Label"]].drop_duplicates()
    totals = totals.merge(labels, on=["Player No.", "Team"], how="left")
    totals["Name"] = totals["Player_Team_Label"].fillna(
        "Player " + totals["Player No."].astype(str)
    )
    totals["Name"] = totals.apply(
        lambda r: _get_3on3_display_name(r["Team"], r["Player No."], r["Name"]), axis=1
    )
    totals["Name"] = totals["Name"] + " (" + totals["Team"].astype(str) + ")"
    base_cols = [
        "Name", "Games", "Points", "Rebounds", "Assists", "3PM", "FG Made", "Blocks",
        "OREB", "DREB", "Personal Fouls", "Turnovers",
        "FG%", "3PT%", "FT%", "GCIR"
    ]
    if include_gcmvp:
        base_cols.append("GCMVP")
    display_df = totals[base_cols].copy()
    for pct_col in ["FG%", "3PT%", "FT%"]:
        if pct_col in display_df.columns:
            display_df[pct_col] = display_df[pct_col].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")
    return display_df


def _playoff_game_sort_key(game_name: str) -> int:
    """Return sort order for playoff games: 1=Round 1, 2=Round 2, 3=Losers R1, 4=Semis, 5=Finals, 6=Third place, 7=Championship."""
    s = str(game_name).strip().lower()
    if "championship" in s:
        return 7
    if "third place" in s:
        return 6
    if "final" in s and "semi" not in s:
        return 5
    if "semi" in s:
        return 4
    if "losers" in s and ("round 1" in s or "r1" in s):
        return 3
    if "round 2" in s or "r2" in s:
        return 2
    if "round 1" in s or "r1" in s:
        return 1
    return 0


def _render_3on3_playoffs_box_page(game_data: pd.DataFrame, advanced_stats: pd.DataFrame):
    """Render playoff games + box scores in round order (R1 → R2 → Losers R1 → Semis → Finals → Third place → Championship)."""
    if st.button("← Back to 3 on 3 Dashboard", type="primary", key="back_3on3_po"):
        st.session_state["view_3on3"] = "main"
        st.rerun()

    st.subheader("📋 View all playoff games and box scores")
    st.caption("Rankings table below. Games in order: Round 1 → Round 2 → Losers bracket R1 → Semis → Finals → Third place → Championship.")

    game_type_norm = game_data["Game_Type"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip().str.lower()
    game_data = game_data[game_type_norm == "playoffs"].copy()
    if game_data.empty:
        st.info("No playoff games in the data.")
        _render_footer()
        return

    game_data = game_data.copy()
    _pts = pd.to_numeric(game_data["PTS"], errors="coerce").fillna(0)
    _fga = pd.to_numeric(game_data["FGA"], errors="coerce").fillna(0)
    _pps = (_pts / _fga.replace(0, pd.NA)).fillna(0).astype(float)
    game_data["_impact"] = (
        _pts * _pps
        + 1.3 * pd.to_numeric(game_data["REB"], errors="coerce").fillna(0)
        + 1.5 * pd.to_numeric(game_data["AST"], errors="coerce").fillna(0)
        + 3 * pd.to_numeric(game_data["STL"], errors="coerce").fillna(0)
        + 2.5 * pd.to_numeric(game_data["BLK"], errors="coerce").fillna(0)
        + 0.7 * pd.to_numeric(game_data["OREB"], errors="coerce").fillna(0)
        - 1.5 * pd.to_numeric(game_data["TOV"], errors="coerce").fillna(0)
        - 0.8 * pd.to_numeric(game_data["PF"], errors="coerce").fillna(0)
    ).astype(float)
    idx_best = game_data.groupby(["Game", "Game_Type"])["_impact"].idxmax()
    best_per_game = game_data.loc[idx_best, ["Game", "Game_Type", "Player No.", "Team", "_impact"]].copy()
    best_per_game = best_per_game.merge(
        advanced_stats[["Player No.", "Team", "Player_Team_Label"]].drop_duplicates(),
        on=["Player No.", "Team"], how="left"
    )
    best_per_game["Player_Team_Label"] = best_per_game["Player_Team_Label"].fillna(
        "Player " + best_per_game["Player No."].astype(str) + " (" + best_per_game["Team"].astype(str) + ")"
    )
    best_per_game["Display_Name"] = best_per_game.apply(
        lambda r: _get_3on3_display_name(r["Team"], r["Player No."], r["Player_Team_Label"]), axis=1
    )
    best_per_game["Display_Name"] = best_per_game["Display_Name"] + " (" + best_per_game["Team"].astype(str) + ")"
    pog_lookup = best_per_game.set_index(["Game", "Game_Type"])["Display_Name"].to_dict()

    game_team_pts = game_data.groupby(["Game", "Game_Type", "Team"], as_index=False)["PTS"].sum()
    games_list = []
    for (game_name, game_type), grp in game_team_pts.groupby(["Game", "Game_Type"]):
        teams = grp["Team"].tolist()
        scores = grp["PTS"].tolist()
        pog = pog_lookup.get((game_name, game_type), "")
        if len(teams) >= 2:
            t1, t2 = teams[0], teams[1]
            s1, s2 = int(round(scores[0])), int(round(scores[1]))
            winner = t1 if s1 > s2 else (t2 if s2 > s1 else "Tie")
            margin = abs(s1 - s2)
            games_list.append({
                "Game": game_name, "Game Type": game_type, "Team 1": t1, "Team 2": t2,
                "Score 1": s1, "Score 2": s2, "Winner": winner,
                "Won by": margin if winner != "Tie" else 0, "Player of the Game": pog,
            })
        else:
            games_list.append({
                "Game": game_name, "Game Type": game_type,
                "Team 1": teams[0] if teams else "", "Team 2": "",
                "Score 1": int(round(scores[0])) if scores else 0, "Score 2": 0,
                "Winner": teams[0] if teams else "", "Won by": 0, "Player of the Game": pog,
            })
    games_df = pd.DataFrame(games_list)
    if not games_df.empty:
        games_df["_order"] = games_df["Game"].map(_playoff_game_sort_key)
        games_df = games_df.sort_values("_order").drop(columns=["_order"])
    st.markdown("**Rankings**")
    st.dataframe(games_df, use_container_width=True, hide_index=True)
    st.markdown("---")

    game_data = game_data.merge(
        advanced_stats[["Player No.", "Team", "Player_Team_Label"]].drop_duplicates(),
        on=["Player No.", "Team"], how="left"
    )
    game_data["Player_Team_Label"] = game_data["Player_Team_Label"].fillna(
        "Player " + game_data["Player No."].astype(str) + " (" + game_data["Team"].astype(str) + ")"
    )
    game_data["Name"] = game_data.apply(
        lambda r: _get_3on3_display_name(r["Team"], r["Player No."], r["Player_Team_Label"]), axis=1
    )
    _col_3pt = "3PTM" if "3PTM" in game_data.columns else "3PM"
    game_groups = list(game_data.groupby(["Game", "Game_Type"]))
    game_groups.sort(key=lambda x: (_playoff_game_sort_key(x[0][0]), x[0][0]))
    for (game_name, game_type), grp in game_groups:
        teams = grp["Team"].unique().tolist()
        if len(teams) < 2:
            continue
        t1, t2 = teams[0], teams[1]
        t1_score = int(round(grp[grp["Team"] == t1]["PTS"].sum()))
        t2_score = int(round(grp[grp["Team"] == t2]["PTS"].sum()))
        st.markdown("---")
        st.markdown(f"### {game_name}")
        st.caption(f"**{t1}** {t1_score} — {t2_score} **{t2}**")
        tab1, tab2, tab3 = st.tabs([t1.upper(), t2.upper(), "TEAM STATS"])
        for tab, team in [(tab1, t1), (tab2, t2)]:
            with tab:
                team_grp = grp[grp["Team"] == team].copy()
                team_grp["Player"] = team_grp["Player No."].astype(str) + " " + team_grp["Name"]
                team_grp["FG"] = team_grp["FGM"].astype(int).astype(str) + "-" + team_grp["FGA"].astype(int).astype(str)
                team_grp["3PT"] = team_grp[_col_3pt].astype(int).astype(str) + "-" + team_grp["3PA"].astype(int).astype(str)
                team_grp["FT"] = team_grp["FTM"].astype(int).astype(str) + "-" + team_grp["FTA"].astype(int).astype(str)
                team_grp["TO"] = team_grp["TOV"]
                box_df = team_grp[["Player", "MIN", "PTS", "FG", "3PT", "FT", "REB", "AST", "STL", "BLK", "TO", "PF"]].copy()
                st.dataframe(box_df, use_container_width=True, hide_index=True)
        with tab3:
            tg1 = grp[grp["Team"] == t1]
            tg2 = grp[grp["Team"] == t2]
            def _pct(made, att): return f"{round(100 * made / att, 1)}" if att else "0"
            fg1, fga1 = tg1["FGM"].sum(), tg1["FGA"].sum()
            fg2, fga2 = tg2["FGM"].sum(), tg2["FGA"].sum()
            t31, t3a1 = tg1[_col_3pt].sum(), tg1["3PA"].sum()
            t32, t3a2 = tg2[_col_3pt].sum(), tg2["3PA"].sum()
            ft1, fta1 = tg1["FTM"].sum(), tg1["FTA"].sum()
            ft2, fta2 = tg2["FTM"].sum(), tg2["FTA"].sum()
            stats_rows = [
                ("Field goals", f"{int(fg1)}/{int(fga1)}", f"{int(fg2)}/{int(fga2)}"),
                ("FG %", _pct(fg1, fga1), _pct(fg2, fga2)),
                ("3-pointers", f"{int(t31)}/{int(t3a1)}", f"{int(t32)}/{int(t3a2)}"),
                ("3PT %", _pct(t31, t3a1), _pct(t32, t3a2)),
                ("Free throws", f"{int(ft1)}/{int(fta1)}", f"{int(ft2)}/{int(fta2)}"),
                ("FT %", _pct(ft1, fta1), _pct(ft2, fta2)),
                ("Total rebounds", str(int(tg1["REB"].sum())), str(int(tg2["REB"].sum()))),
                ("Offensive rebounds", str(int(tg1["OREB"].sum())), str(int(tg2["OREB"].sum()))),
                ("Defensive rebounds", str(int(tg1["DREB"].sum())), str(int(tg2["DREB"].sum()))),
                ("Assists", str(int(tg1["AST"].sum())), str(int(tg2["AST"].sum()))),
                ("Blocks", str(int(tg1["BLK"].sum())), str(int(tg2["BLK"].sum()))),
                ("Steals", str(int(tg1["STL"].sum())), str(int(tg2["STL"].sum()))),
                ("Turnovers", str(int(tg1["TOV"].sum())), str(int(tg2["TOV"].sum()))),
            ]
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown(f"**{t1}**")
                for label, v1, _ in stats_rows:
                    st.markdown(f"{label}: **{v1}**")
            with sc2:
                st.markdown(f"**{t2}**")
                for label, _, v2 in stats_rows:
                    st.markdown(f"{label}: **{v2}**")
        pog = pog_lookup.get((game_name, game_type), "")
        if pog:
            st.markdown(f"**Player of the Game:** {pog}")
    _render_footer()


def _render_3on3_games_box_page(game_data: pd.DataFrame, advanced_stats: pd.DataFrame):
    """Render the 'All games played + box scores' sub-page (Round Robin only) in traditional box score format."""
    if st.button("← Back to 3 on 3 Dashboard", type="primary", key="back_3on3"):
        st.session_state["view_3on3"] = "main"
        st.rerun()

    st.subheader("📋 View all round robin games and box scores")
    st.caption("Rankings table below. Traditional box score for each game; Player of the Game under each box score.")

    game_type_norm = game_data["Game_Type"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip().str.lower()
    game_data = game_data[game_type_norm == "round robin"].copy()
    if game_data.empty:
        st.info("No Round Robin games in the data.")
        _render_footer()
        return

    game_data = game_data.copy()
    _pts = pd.to_numeric(game_data["PTS"], errors="coerce").fillna(0)
    _fga = pd.to_numeric(game_data["FGA"], errors="coerce").fillna(0)
    _pps = (_pts / _fga.replace(0, pd.NA)).fillna(0).astype(float)
    game_data["_impact"] = (
        _pts * _pps
        + 1.3 * pd.to_numeric(game_data["REB"], errors="coerce").fillna(0)
        + 1.5 * pd.to_numeric(game_data["AST"], errors="coerce").fillna(0)
        + 3 * pd.to_numeric(game_data["STL"], errors="coerce").fillna(0)
        + 2.5 * pd.to_numeric(game_data["BLK"], errors="coerce").fillna(0)
        + 0.7 * pd.to_numeric(game_data["OREB"], errors="coerce").fillna(0)
        - 1.5 * pd.to_numeric(game_data["TOV"], errors="coerce").fillna(0)
        - 0.8 * pd.to_numeric(game_data["PF"], errors="coerce").fillna(0)
    ).astype(float)
    idx_best = game_data.groupby(["Game", "Game_Type"])["_impact"].idxmax()
    best_per_game = game_data.loc[idx_best, ["Game", "Game_Type", "Player No.", "Team", "_impact"]].copy()
    best_per_game = best_per_game.merge(
        advanced_stats[["Player No.", "Team", "Player_Team_Label"]].drop_duplicates(),
        on=["Player No.", "Team"], how="left"
    )
    best_per_game["Player_Team_Label"] = best_per_game["Player_Team_Label"].fillna(
        "Player " + best_per_game["Player No."].astype(str) + " (" + best_per_game["Team"].astype(str) + ")"
    )
    best_per_game["Display_Name"] = best_per_game.apply(
        lambda r: _get_3on3_display_name(r["Team"], r["Player No."], r["Player_Team_Label"]), axis=1
    )
    best_per_game["Display_Name"] = best_per_game["Display_Name"] + " (" + best_per_game["Team"].astype(str) + ")"
    pog_lookup = best_per_game.set_index(["Game", "Game_Type"])["Display_Name"].to_dict()

    game_team_pts = game_data.groupby(["Game", "Game_Type", "Team"], as_index=False)["PTS"].sum()
    games_list = []
    for (game_name, game_type), grp in game_team_pts.groupby(["Game", "Game_Type"]):
        teams = grp["Team"].tolist()
        scores = grp["PTS"].tolist()
        pog = pog_lookup.get((game_name, game_type), "")
        if len(teams) >= 2:
            t1, t2 = teams[0], teams[1]
            s1, s2 = int(round(scores[0])), int(round(scores[1]))
            winner = t1 if s1 > s2 else (t2 if s2 > s1 else "Tie")
            margin = abs(s1 - s2)
            games_list.append({
                "Game": game_name, "Game Type": game_type, "Team 1": t1, "Team 2": t2,
                "Score 1": s1, "Score 2": s2, "Winner": winner,
                "Won by": margin if winner != "Tie" else 0, "Player of the Game": pog,
            })
        else:
            games_list.append({
                "Game": game_name, "Game Type": game_type,
                "Team 1": teams[0] if teams else "", "Team 2": "",
                "Score 1": int(round(scores[0])) if scores else 0, "Score 2": 0,
                "Winner": teams[0] if teams else "", "Won by": 0, "Player of the Game": pog,
            })
    games_df = pd.DataFrame(games_list)
    st.dataframe(games_df, use_container_width=True, hide_index=True)

    # Add display name for traditional box score
    game_data = game_data.merge(
        advanced_stats[["Player No.", "Team", "Player_Team_Label"]].drop_duplicates(),
        on=["Player No.", "Team"], how="left"
    )
    game_data["Player_Team_Label"] = game_data["Player_Team_Label"].fillna(
        "Player " + game_data["Player No."].astype(str) + " (" + game_data["Team"].astype(str) + ")"
    )
    game_data["Name"] = game_data.apply(
        lambda r: _get_3on3_display_name(r["Team"], r["Player No."], r["Player_Team_Label"]), axis=1
    )

    # Traditional box score: Player (No. Name), MIN, PTS, FG, 3PT, FT, REB, AST, STL, BLK, TO, PF
    _col_3pt = "3PTM" if "3PTM" in game_data.columns else "3PM"
    for (game_name, game_type), grp in game_data.groupby(["Game", "Game_Type"]):
        teams = grp["Team"].unique().tolist()
        if len(teams) < 2:
            continue
        t1, t2 = teams[0], teams[1]
        t1_score = int(round(grp[grp["Team"] == t1]["PTS"].sum()))
        t2_score = int(round(grp[grp["Team"] == t2]["PTS"].sum()))

        st.markdown("---")
        st.markdown(f"### {game_name}")
        st.caption(f"**{t1}** {t1_score} — {t2_score} **{t2}**")

        tab1, tab2, tab3 = st.tabs([t1.upper(), t2.upper(), "TEAM STATS"])
        for tab, team in [(tab1, t1), (tab2, t2)]:
            with tab:
                team_grp = grp[grp["Team"] == team].copy()
                team_grp["Player"] = team_grp["Player No."].astype(str) + " " + team_grp["Name"]
                team_grp["FG"] = team_grp["FGM"].astype(int).astype(str) + "-" + team_grp["FGA"].astype(int).astype(str)
                team_grp["3PT"] = team_grp[_col_3pt].astype(int).astype(str) + "-" + team_grp["3PA"].astype(int).astype(str)
                team_grp["FT"] = team_grp["FTM"].astype(int).astype(str) + "-" + team_grp["FTA"].astype(int).astype(str)
                team_grp["TO"] = team_grp["TOV"]
                box_df = team_grp[["Player", "MIN", "PTS", "FG", "3PT", "FT", "REB", "AST", "STL", "BLK", "TO", "PF"]].copy()
                box_df = box_df.rename(columns={"MIN": "MIN", "TO": "TO"})
                st.dataframe(box_df, use_container_width=True, hide_index=True)

        with tab3:
            tg1 = grp[grp["Team"] == t1]
            tg2 = grp[grp["Team"] == t2]
            def _pct(made, att): return f"{round(100 * made / att, 1)}" if att else "0"
            fg1, fga1 = tg1["FGM"].sum(), tg1["FGA"].sum()
            fg2, fga2 = tg2["FGM"].sum(), tg2["FGA"].sum()
            t31, t3a1 = tg1[_col_3pt].sum(), tg1["3PA"].sum()
            t32, t3a2 = tg2[_col_3pt].sum(), tg2["3PA"].sum()
            ft1, fta1 = tg1["FTM"].sum(), tg1["FTA"].sum()
            ft2, fta2 = tg2["FTM"].sum(), tg2["FTA"].sum()
            stats_rows = [
                ("Field goals", f"{int(fg1)}/{int(fga1)}", f"{int(fg2)}/{int(fga2)}"),
                ("FG %", _pct(fg1, fga1), _pct(fg2, fga2)),
                ("3-pointers", f"{int(t31)}/{int(t3a1)}", f"{int(t32)}/{int(t3a2)}"),
                ("3PT %", _pct(t31, t3a1), _pct(t32, t3a2)),
                ("Free throws", f"{int(ft1)}/{int(fta1)}", f"{int(ft2)}/{int(fta2)}"),
                ("FT %", _pct(ft1, fta1), _pct(ft2, fta2)),
                ("Total rebounds", str(int(tg1["REB"].sum())), str(int(tg2["REB"].sum()))),
                ("Offensive rebounds", str(int(tg1["OREB"].sum())), str(int(tg2["OREB"].sum()))),
                ("Defensive rebounds", str(int(tg1["DREB"].sum())), str(int(tg2["DREB"].sum()))),
                ("Assists", str(int(tg1["AST"].sum())), str(int(tg2["AST"].sum()))),
                ("Blocks", str(int(tg1["BLK"].sum())), str(int(tg2["BLK"].sum()))),
                ("Steals", str(int(tg1["STL"].sum())), str(int(tg2["STL"].sum()))),
                ("Turnovers", str(int(tg1["TOV"].sum())), str(int(tg2["TOV"].sum()))),
            ]
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown(f"**{t1}**")
                for label, v1, _ in stats_rows:
                    st.markdown(f"{label}: **{v1}**")
            with sc2:
                st.markdown(f"**{t2}**")
                for label, _, v2 in stats_rows:
                    st.markdown(f"{label}: **{v2}**")
        pog = pog_lookup.get((game_name, game_type), "")
        if pog:
            st.markdown(f"**Player of the Game:** {pog}")

    _render_footer()


def _render_3on3_player_dashboard(game_data: pd.DataFrame, advanced_stats: pd.DataFrame):
    """Player Dashboard: select a player, see their averages and game-by-game box score."""
    _col_3pt = "3PTM" if "3PTM" in game_data.columns else "3PM"
    totals = game_data.groupby(["Player No.", "Team"], as_index=False).agg(
        Games=("Game", "nunique"),
        PTS=("PTS", "sum"), REB=("REB", "sum"), AST=("AST", "sum"),
        FGM=("FGM", "sum"), FGA=("FGA", "sum"),
        ThreePTM=(_col_3pt, "sum"),
        ThreePA=("3PA", "sum"), FTM=("FTM", "sum"), FTA=("FTA", "sum"),
        STL=("STL", "sum"), BLK=("BLK", "sum"), TOV=("TOV", "sum"),
    )
    for c in totals.columns:
        if c != "Player No." and c != "Team":
            totals[c] = pd.to_numeric(totals[c], errors="coerce").fillna(0)
    totals = totals.merge(
        advanced_stats[["Player No.", "Team", "Player_Team_Label"]].drop_duplicates(),
        on=["Player No.", "Team"], how="left"
    )
    totals["Name"] = totals["Player_Team_Label"].fillna("Player " + totals["Player No."].astype(str))
    totals["Name"] = totals.apply(lambda r: _get_3on3_display_name(r["Team"], r["Player No."], r["Name"]), axis=1)
    totals["Name"] = totals["Name"] + " (" + totals["Team"].astype(str) + ")"

    # Select a player
    st.subheader("👤 Player statistics")
    player_options = sorted(totals["Name"].unique().tolist())
    if not player_options:
        st.caption("No players in data.")
        return
    selected_name = st.selectbox(
        "Select a player to see their averages and game-by-game box score",
        options=player_options,
        key="3on3_player_box_select",
    )
    match = totals[totals["Name"] == selected_name]
    if match.empty:
        st.caption("Player not found.")
        return
    r = match.iloc[0]
    pno, team = r["Player No."], r["Team"]
    gp = int(r["Games"])
    g = gp if gp else 1
    # Per-game averages; shooting in FGM-FGA style (per-game avg rounded to 1 decimal)
    fgm_avg = (r["FGM"] / g).round(1)
    fga_avg = (r["FGA"] / g).round(1)
    t3m_avg = (r["ThreePTM"] / g).round(1)
    t3a_avg = (r["ThreePA"] / g).round(1)
    ftm_avg = (r["FTM"] / g).round(1)
    fta_avg = (r["FTA"] / g).round(1)
    pts_avg = (r["PTS"] / g).round(1)
    reb_avg = (r["REB"] / g).round(1)
    ast_avg = (r["AST"] / g).round(1)
    stl_avg = (r["STL"] / g).round(1)
    blk_avg = (r["BLK"] / g).round(1)
    to_avg = (r["TOV"] / g).round(1)
    st.markdown(f"**{selected_name}**")
    st.caption(f"**Averages (per game):** GP {gp} · PTS {pts_avg} · FG {fgm_avg:.1f}-{fga_avg:.1f} · 3PT {t3m_avg:.1f}-{t3a_avg:.1f} · FT {ftm_avg:.1f}-{fta_avg:.1f} · REB {reb_avg} · AST {ast_avg} · STL {stl_avg} · BLK {blk_avg} · TO {to_avg}**")

    st.subheader("📋 Game-by-game box score")
    player_games = game_data[(game_data["Player No."] == pno) & (game_data["Team"] == team)].copy()
    for col in ["PTS", "FGM", "FGA", "REB", "OREB", "DREB", "AST", "STL", "BLK", "TOV", "PF"]:
        if col in player_games.columns:
            player_games[col] = pd.to_numeric(player_games[col], errors="coerce").fillna(0)
    _col_3pm = "3PTM" if "3PTM" in player_games.columns else "3PM"
    if "3PA" in player_games.columns:
        player_games["3PA"] = pd.to_numeric(player_games["3PA"], errors="coerce").fillna(0)
    if "FTM" in player_games.columns:
        player_games["FTM"] = pd.to_numeric(player_games["FTM"], errors="coerce").fillna(0)
    if "FTA" in player_games.columns:
        player_games["FTA"] = pd.to_numeric(player_games["FTA"], errors="coerce").fillna(0)
    player_games["FG%"] = (100 * player_games["FGM"] / player_games["FGA"].replace(0, 1)).round(1)
    player_games["3PT%"] = (100 * player_games[_col_3pm] / player_games["3PA"].replace(0, 1)).round(1)
    player_games["FT%"] = (100 * player_games["FTM"] / player_games["FTA"].replace(0, 1)).round(1)
    box_cols = ["Game", "Game_Type", "PTS", "FGM", "FGA", "FG%", _col_3pm, "3PA", "3PT%", "FTM", "FTA", "FT%", "REB", "OREB", "DREB", "AST", "STL", "BLK", "TOV", "PF"]
    box_cols = [c for c in box_cols if c in player_games.columns]
    box_df = player_games[box_cols].copy()
    box_df = box_df.rename(columns={_col_3pm: "3PM", "TOV": "TO"})
    box_df = box_df.sort_values(["Game_Type", "Game"], ascending=[True, True])
    st.caption(f"**{selected_name}** — each row is one game.")
    st.dataframe(box_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("💬 3 on 3 Tournament Assistant")
    st.caption("Grounded in **this tournament’s** data. Use the sidebar for Rule-Based, Hybrid, or OpenAI.")
    prof = data_manager.get_player_profile(int(pno), str(team), season=3)
    render_3on3_ai_chat_interface(
        player_profile=prof if "error" not in prof else None
    )


def show_3on3_dashboard():
    """3 on 3 Basketball Tournament Dashboard – Team Dashboard or Player Dashboard."""
    st.header("🏀 3 on 3 Basketball Tournament Dashboard")

    try:
        game_data = data_manager.load_player_data(season=3)
        advanced_stats = data_manager.load_advanced_stats(season=3)
    except Exception as e:
        st.error(f"Error loading tournament data: {str(e)}")
        _render_footer()
        return

    # Ensure Game_Type exists (old CSVs may not have it – treat all as Round Robin)
    if "Game_Type" not in game_data.columns:
        game_data = game_data.copy()
        game_data["Game_Type"] = "Round Robin"

    # Sub-pages: Round Robin or Playoffs games + box scores (Back to return)
    if st.session_state.get("view_3on3") == "games_box":
        _render_3on3_games_box_page(game_data, advanced_stats)
        return
    if st.session_state.get("view_3on3") == "playoffs_box":
        _render_3on3_playoffs_box_page(game_data, advanced_stats)
        return

    # Two buttons: Team Dashboard | Player Dashboard
    mode = st.session_state.get("3on3_mode", "team")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Team Dashboard", type="primary" if mode == "team" else "secondary", use_container_width=True, key="3on3_team_btn"):
            st.session_state["3on3_mode"] = "team"
            st.rerun()
    with col2:
        if st.button("👤 Player Dashboard", type="primary" if mode == "player" else "secondary", use_container_width=True, key="3on3_player_btn"):
            st.session_state["3on3_mode"] = "player"
            st.rerun()

    if mode == "player":
        _render_3on3_player_dashboard(game_data, advanced_stats)
        _render_footer()
        return

    # ------ Team Dashboard: Round Robin overview (first thing) ------
    st.subheader("📊 Round Robin Overview")
    # Filter by Game_Type set by convert_3on3_tournament.py (uses your playoff keywords there)
    game_type_norm = game_data["Game_Type"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip().str.lower()
    round_robin = game_data[game_type_norm == "round robin"].copy()
    if round_robin.empty:
        st.info("No Round Robin games in the data. All games may be marked as Playoffs, or Game_Type is missing.")
    else:
        # Total games and team records (wins / losses) — from Round Robin games only
        rr_team_pts = round_robin.groupby(["Game", "Team"], as_index=False)["PTS"].sum()
        rr_games_total = rr_team_pts["Game"].nunique()
        # Winner per game = team with higher total PTS in that game
        winners = []
        for game_name, grp in rr_team_pts.groupby("Game"):
            grp = grp.sort_values("PTS", ascending=False)
            if len(grp) >= 2 and grp.iloc[0]["PTS"] > grp.iloc[1]["PTS"]:
                winners.append(grp.iloc[0]["Team"])
        wins_per_team = pd.Series(winners).value_counts() if winners else pd.Series(dtype=int)
        # Games played per team = number of Round Robin games that team appeared in
        games_per_team = rr_team_pts.groupby("Team")["Game"].nunique()
        records = []
        for team in games_per_team.index:
            played = int(games_per_team[team])
            w = int(wins_per_team.get(team, 0))
            l = played - w
            records.append({"Team": team, "Wins": w, "Losses": l, "Round Robin Record": f"{w}-{l}"})
        records_df = pd.DataFrame(records).sort_values("Wins", ascending=False)[["Team", "Wins", "Losses", "Round Robin Record"]]
        st.caption(f"**Total Round Robin games played:** {rr_games_total}")
        st.caption("Team records below are **Round Robin only** (only games with Game Type = Round Robin; playoffs excluded).")
        st.dataframe(records_df, use_container_width=True, hide_index=True)
        st.markdown("")  # small spacing
        display_rr = _build_3on3_player_table(round_robin, advanced_stats)
        column_config = {col: st.column_config.Column(col, help=STAT_TOOLTIPS.get(col, "")) for col in display_rr.columns if STAT_TOOLTIPS.get(col)}
        st.dataframe(display_rr, use_container_width=True, hide_index=True, column_config=column_config)
    st.markdown("")
    if st.button("📋 View all round robin games and box scores", type="secondary", key="go_games_box"):
        st.session_state["view_3on3"] = "games_box"
        st.rerun()

    # ------ 2) Playoffs overview (when present) ------
    playoffs = game_data[game_type_norm == "playoffs"].copy()
    if not playoffs.empty:
        st.markdown("---")
        st.subheader("🏆 Playoffs Overview")
        display_po = _build_3on3_player_table(playoffs, advanced_stats)
        column_config_po = {col: st.column_config.Column(col, help=STAT_TOOLTIPS.get(col, "")) for col in display_po.columns if STAT_TOOLTIPS.get(col)}
        st.dataframe(display_po, use_container_width=True, hide_index=True, column_config=column_config_po)
        st.markdown("")
        if st.button("📋 View all playoff games and box scores", type="secondary", key="go_playoffs_box"):
            st.session_state["view_3on3"] = "playoffs_box"
            st.rerun()
    else:
        st.markdown("---")
        st.subheader("🏆 Playoffs Overview")
        st.info(
            "No playoff games detected. In your Excel workbook (**3 on 3  basketball tournament .xlsx**), "
            "rename the **sheet tab** for each playoff game so the name includes the word **Playoffs** "
            "(e.g. \"Playoffs - Round 1\", \"Playoffs - Third Place Game\"). Then run: **python convert_3on3_tournament.py** "
            "and refresh this page."
        )

    # ------ 3 on 3 Tournament Averages (per-game) and Totals (season sums) ------
    rr_games_total = round_robin["Game"].nunique() if not round_robin.empty else 0
    po_games_total = playoffs["Game"].nunique() if not playoffs.empty else 0
    st.markdown("---")
    st.subheader("📋 3 on 3 Tournament Averages")
    st.caption(f"**Round Robin:** {rr_games_total} games  |  **Playoffs:** {po_games_total} games  |  **Total:** {rr_games_total + po_games_total} games. Per-game averages below.")
    display_all = _build_3on3_player_table(game_data, advanced_stats, include_gcmvp=True)
    column_config_all = {col: st.column_config.Column(col, help=STAT_TOOLTIPS.get(col, "")) for col in display_all.columns if STAT_TOOLTIPS.get(col)}
    st.dataframe(display_all, use_container_width=True, hide_index=True, column_config=column_config_all)

    # 3 on 3 Tournament Totals (season totals, not averages)
    _col_3pt = "3PTM" if "3PTM" in game_data.columns else "3PM"
    player_totals_raw = game_data.groupby(["Player No.", "Team"], as_index=False).agg(
        Games=("Game", "nunique"),
        PTS=("PTS", "sum"), REB=("REB", "sum"), AST=("AST", "sum"),
        ThreePTM=(_col_3pt, "sum"), FGM=("FGM", "sum"), BLK=("BLK", "sum"),
        OREB=("OREB", "sum"), DREB=("DREB", "sum"), PF=("PF", "sum"), TOV=("TOV", "sum"),
        FGA=("FGA", "sum"), ThreePA=("3PA", "sum"), FTM=("FTM", "sum"), FTA=("FTA", "sum"),
    )
    for c in player_totals_raw.columns:
        if c not in ["Player No.", "Team"]:
            player_totals_raw[c] = pd.to_numeric(player_totals_raw[c], errors="coerce").fillna(0)
    player_totals_raw = player_totals_raw.merge(
        advanced_stats[["Player No.", "Team", "Player_Team_Label"]].drop_duplicates(),
        on=["Player No.", "Team"], how="left"
    )
    player_totals_raw["Name"] = player_totals_raw["Player_Team_Label"].fillna(
        "Player " + player_totals_raw["Player No."].astype(str)
    )
    player_totals_raw["Name"] = player_totals_raw.apply(
        lambda r: _get_3on3_display_name(r["Team"], r["Player No."], r["Name"]), axis=1
    )
    player_totals_raw["Name"] = player_totals_raw["Name"] + " (" + player_totals_raw["Team"].astype(str) + ")"
    player_totals_raw["Points"] = player_totals_raw["PTS"].astype(int)
    player_totals_raw["Rebounds"] = player_totals_raw["REB"].astype(int)
    player_totals_raw["Assists"] = player_totals_raw["AST"].astype(int)
    player_totals_raw["3PM"] = player_totals_raw["ThreePTM"].astype(int)
    player_totals_raw["FG Made"] = player_totals_raw["FGM"].astype(int)
    player_totals_raw["Blocks"] = player_totals_raw["BLK"].astype(int)
    player_totals_raw["OREB"] = player_totals_raw["OREB"].astype(int)
    player_totals_raw["DREB"] = player_totals_raw["DREB"].astype(int)
    player_totals_raw["Personal Fouls"] = player_totals_raw["PF"].astype(int)
    player_totals_raw["Turnovers"] = player_totals_raw["TOV"].astype(int)
    player_totals_raw["FG%"] = (100 * player_totals_raw["FGM"] / player_totals_raw["FGA"].replace(0, 1)).round(1)
    player_totals_raw["3PT%"] = (100 * player_totals_raw["ThreePTM"] / player_totals_raw["ThreePA"].replace(0, 1)).round(1)
    player_totals_raw["FT%"] = (100 * player_totals_raw["FTM"] / player_totals_raw["FTA"].replace(0, 1)).round(1)
    totals_display = player_totals_raw[[
        "Name", "Games", "Points", "Rebounds", "Assists", "3PM", "FG Made", "Blocks",
        "OREB", "DREB", "Personal Fouls", "Turnovers", "FG%", "3PT%", "FT%"
    ]].copy()
    for pct_col in ["FG%", "3PT%", "FT%"]:
        totals_display[pct_col] = totals_display[pct_col].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")
    st.subheader("📋 3 on 3 Tournament Totals")
    st.caption("Season totals (not per-game).")
    st.dataframe(totals_display, use_container_width=True, hide_index=True, column_config={col: st.column_config.Column(col, help=STAT_TOOLTIPS.get(col, "")) for col in totals_display.columns if STAT_TOOLTIPS.get(col)})

    # Team totals (all games): one row per team, season totals
    _col_3pm = "3PM" if "3PM" in game_data.columns else "3PTM"
    team_per_game = game_data.groupby(["Game", "Team"], as_index=False).agg(
        PTS=("PTS", "sum"),
        REB=("REB", "sum"),
        AST=("AST", "sum"),
        ThreePTM=(_col_3pm, "sum"),
        FGM=("FGM", "sum"),
        BLK=("BLK", "sum"),
        OREB=("OREB", "sum"),
        DREB=("DREB", "sum"),
        PF=("PF", "sum"),
        TOV=("TOV", "sum"),
        STL=("STL", "sum"),
    )
    team_totals = team_per_game.groupby("Team", as_index=False).agg(
        Games=("Game", "nunique"),
        PTS=("PTS", "sum"),
        REB=("REB", "sum"),
        AST=("AST", "sum"),
        ThreePTM=("ThreePTM", "sum"),
        FGM=("FGM", "sum"),
        BLK=("BLK", "sum"),
        OREB=("OREB", "sum"),
        DREB=("DREB", "sum"),
        PF=("PF", "sum"),
        TOV=("TOV", "sum"),
        STL=("STL", "sum"),
    )
    team_totals = team_totals.rename(columns={
        "ThreePTM": "3PM", "FGM": "FG Made", "BLK": "Blocks",
        "PF": "Personal Fouls", "TOV": "Turnovers",
    })
    st.caption("**Team totals** (sum of all games for each team)")
    st.dataframe(team_totals, use_container_width=True, hide_index=True)

    st.markdown("---")
    # ------ 3) Games played: game type, who won, by how much, player of the game ------
    st.subheader("📋 Games Played")
    # Per-game GCIR for Player of the Game: PPS = PTS/FGA; GCIR = (PTS×PPS) + 1.3(REB) + 1.5(AST) + 3(STL) + 2.5(BLK) + 0.7(OREB) − 1.5(TOV) − 0.8(PF)
    game_data = game_data.copy()
    _pts = pd.to_numeric(game_data["PTS"], errors="coerce").fillna(0)
    _fga = pd.to_numeric(game_data["FGA"], errors="coerce").fillna(0)
    _pps = (_pts / _fga.replace(0, pd.NA)).fillna(0).astype(float)
    game_data["_impact"] = (
        _pts * _pps
        + 1.3 * pd.to_numeric(game_data["REB"], errors="coerce").fillna(0)
        + 1.5 * pd.to_numeric(game_data["AST"], errors="coerce").fillna(0)
        + 3 * pd.to_numeric(game_data["STL"], errors="coerce").fillna(0)
        + 2.5 * pd.to_numeric(game_data["BLK"], errors="coerce").fillna(0)
        + 0.7 * pd.to_numeric(game_data["OREB"], errors="coerce").fillna(0)
        - 1.5 * pd.to_numeric(game_data["TOV"], errors="coerce").fillna(0)
        - 0.8 * pd.to_numeric(game_data["PF"], errors="coerce").fillna(0)
    ).astype(float)
    # Best player per game (max GCIR)
    idx_best = game_data.groupby(["Game", "Game_Type"])["_impact"].idxmax()
    best_per_game = game_data.loc[idx_best, ["Game", "Game_Type", "Player No.", "Team", "_impact"]].copy()
    best_per_game = best_per_game.merge(
        advanced_stats[["Player No.", "Team", "Player_Team_Label"]].drop_duplicates(),
        on=["Player No.", "Team"],
        how="left"
    )
    best_per_game["Player_Team_Label"] = best_per_game["Player_Team_Label"].fillna(
        "Player " + best_per_game["Player No."].astype(str) + " (" + best_per_game["Team"].astype(str) + ")"
    )
    best_per_game["Display_Name"] = best_per_game.apply(
        lambda r: _get_3on3_display_name(r["Team"], r["Player No."], r["Player_Team_Label"]), axis=1
    )
    best_per_game["Display_Name"] = best_per_game["Display_Name"] + " (" + best_per_game["Team"].astype(str) + ")"
    pog_lookup = best_per_game.set_index(["Game", "Game_Type"])["Display_Name"].to_dict()

    # Per-game team totals (PTS)
    game_team_pts = game_data.groupby(["Game", "Game_Type", "Team"], as_index=False)["PTS"].sum()
    games_list = []
    for (game_name, game_type), grp in game_team_pts.groupby(["Game", "Game_Type"]):
        teams = grp["Team"].tolist()
        scores = grp["PTS"].tolist()
        pog = pog_lookup.get((game_name, game_type), "")
        if len(teams) >= 2:
            t1, t2 = teams[0], teams[1]
            s1, s2 = int(round(scores[0])), int(round(scores[1]))
            winner = t1 if s1 > s2 else (t2 if s2 > s1 else "Tie")
            margin = abs(s1 - s2)
            games_list.append({
                "Game": game_name,
                "Game Type": game_type,
                 "Team 1": t1,
                "Team 2": t2,
                "Score 1": s1,
                "Score 2": s2,
                "Winner": winner,
                "Won by": margin if winner != "Tie" else 0,
                "Player of the Game": pog,
            })
        else:
            games_list.append({
                "Game": game_name,
                "Game Type": game_type,
                "Team 1": teams[0] if teams else "",
                "Team 2": "",
                "Score 1": int(round(scores[0])) if scores else 0,
                "Score 2": 0,
                "Winner": teams[0] if teams else "",
                "Won by": 0,
                "Player of the Game": pog,
            })
    games_df = pd.DataFrame(games_list)
    st.dataframe(games_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    if not round_robin.empty and st.checkbox("Show player comparison chart (Round Robin)", value=False, key="3on3_chart"):
        try:
            import plotly.express as px
            display_rr = _build_3on3_player_table(round_robin, advanced_stats)
            fig = px.bar(
                display_rr.sort_values("GCIR", ascending=True).tail(12),
                x="Name",
                y="GCIR",
                title="GCIR by Player (Round Robin)",
                color="GCIR",
                color_continuous_scale="Blues",
            )
            fig.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.info("Chart is unavailable in this environment.")

    st.markdown("---")
    st.subheader("💬 3 on 3 Tournament Assistant")
    st.caption("Ask about this tournament, strategy for 3 on 3, leaderboards, or team matchups.")
    render_3on3_ai_chat_interface(player_profile=None)

    _render_footer()


def show_sample_report():
    """3️⃣ Player Performance Report - Wow page"""
    # Larger font for Player Performance Report (increase by ~20%)
    st.markdown("""
        <style>
        div[data-testid="stVerticalBlock"] > div {
            font-size: 1.2rem !important;
        }
        .report-page h3, .stMarkdown h3 { font-size: 1.9rem !important; }
        .report-page h4, .stMarkdown h4 { font-size: 1.6rem !important; }
        .report-page p, .stMarkdown p { font-size: 1.25rem !important; }
        [data-testid="stMetricValue"] { font-size: 1.75rem !important; }
        [data-testid="stMetricLabel"] { font-size: 1.15rem !important; }
        </style>
    """, unsafe_allow_html=True)

    st.header("📋 Player Performance Report")

    season_num = _get_season_num()

    players = data_manager.get_all_players(season=season_num)
    if not players:
        st.warning("No players found for selected season.")
        _render_footer()
        return
    
    options = [p["label"] for p in players]
    selected = st.selectbox("Select a player", options, key="sample_report_player")

    idx = options.index(selected)
    player = players[idx]
    profile = data_manager.get_player_profile(player["player_no"], player["team"], season=season_num)

    if "error" in profile:
        st.error(profile["error"])
        _render_footer()
        return
    
    st.markdown(f"### {player['label']}")
    st.markdown("#### Game Summary")
    st.markdown(f"**{profile['total_games']} games played** — Season averages below.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Points", f"{profile['stats']['points']['average']:.1f}")
    with col2:
        st.metric("Assists", f"{profile['stats']['assists']['average']:.1f}")
    with col3:
        st.metric("Turnovers", f"{profile['stats']['turnovers']['average']:.1f}")
    with col4:
        fg = profile["stats"]["shooting"]["fg_pct"]
        st.metric("Shooting %", f"{fg:.1%}" if pd.notna(fg) else "N/A")

    st.markdown("---")
    st.markdown("#### Game-by-Game Box Scores")
    game_data = data_manager.load_player_data(season=season_num)
    player_games = game_data[
        (game_data["Player No."] == player["player_no"]) & (game_data["Team"] == player["team"])
    ].copy()
    if not player_games.empty:
        box_df = player_games[
            ["Game", "PTS", "FGM", "FGA", "FG_PCT", "3PTM", "3PA", "3P%", "FTM", "FTA", "FT%",
             "REB", "OREB", "DREB", "AST", "STL", "BLK", "TOV", "PF", "Efficiency"]
        ].copy()
        box_df = box_df.rename(columns={"FG_PCT": "FG%", "Efficiency": "EFF"})
        box_df["FG%"] = box_df["FG%"].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
        box_df["3P%"] = box_df["3P%"].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
        box_df["FT%"] = box_df["FT%"].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
        st.dataframe(box_df, use_container_width=True, hide_index=True)
    else:
        st.info("No game-by-game data available.")

    st.markdown("---")
    st.markdown("#### Analysis")

    strength = profile.get("strengths", [])
    weakness = profile.get("weaknesses", [])

    st.markdown(f"**Strength:** {strength[0] if strength else 'Versatile player'}")
    st.markdown(f"**Area to Improve:** {weakness[0] if weakness else 'Consistency'}")

    # Suggested drills based on weaknesses (specific, like AI assistant)
    drills_shown = set()
    for w in weakness[:2]:
        drills = drill_library.get_drills_for_weakness(str(w))
        if drills:
            st.markdown(f"**Suggested drills for *{w}*:**")
            for drill in drills[:3]:
                if drill["name"] not in drills_shown:
                    drills_shown.add(drill["name"])
                    st.markdown(f"- **{drill['name']}** ({drill['difficulty']}, {drill['duration']}) — {drill['description']}")
                    for step in drill.get("instructions", [])[:2]:
                        st.markdown(f"  - {step}")
                    st.markdown("")
    if not drills_shown:
        st.markdown("**Suggested Focus:** General skill development — Form Shooting, Right Hand Dribbling, Box Out Drill")

    st.markdown("---")
    st.caption("*Data → Analysis → Recommendation*")
    st.markdown("---")
    st.subheader("💡 AI Assistant")
    st.caption("Ask questions about training, performance, or game strategy for this player.")
    render_ai_chat_interface(player_profile=profile)
    _render_footer()


def main():
    logger.log_page_visit("Dashboard")

    page = _get_page()

    # Show nav only when not on homepage (or show everywhere for consistency)
    _render_nav_buttons()

    if page == "home":
        show_homepage()
    elif page == "dashboard":
        show_live_dashboard()
    elif page == "dashboard_3on3":
        show_3on3_dashboard()
    elif page == "sample_report":
        show_sample_report()
    else:
        show_homepage()


if __name__ == "__main__":
    main()
