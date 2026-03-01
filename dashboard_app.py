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
import plotly.express as px
from data_manager import data_manager
from site_logger import logger
from ai_dashboard_integration import render_ai_chat_interface
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
    """Get current season (1 or 2) from session state."""
    sel = st.session_state.get("season_rising_stars", "Season 1 Rising Stars")
    return 1 if sel == "Season 1 Rising Stars" else 2


def _render_nav_buttons():
    """Render navigation at top, season switcher in right corner (only on Dashboard and Player Performance Report)."""
    page = _get_page()
    show_season = page in ("dashboard", "sample_report")
    left_cols, right_col = st.columns([4, 1])
    with left_cols:
        c1, c2, c3, _ = st.columns(4)
        with c1:
            if st.button("🏠 Home", use_container_width=True) and page != "home":
                _set_page("home")
        with c2:
            if st.button("📊 Player Dashboard", use_container_width=True) and page != "dashboard":
                _set_page("dashboard")
        with c3:
            if st.button("📋 Player Performance Report", use_container_width=True) and page != "sample_report":
                _set_page("sample_report")
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
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 View Dashboard", use_container_width=True, type="primary"):
            _set_page("dashboard")
    with col2:
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
        "*Impact Score combines positive contributions and subtracts negative plays to measure overall game performance.*"
    )

    st.markdown("---")
    st.subheader("🧠 How It Works")
    st.markdown("1️⃣ Game stats are recorded live")
    st.markdown("2️⃣ Performance metrics are calculated")
    st.markdown("3️⃣ An Impact Score is generated")
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


# Stat column tooltips for Player Dashboard (shown on hover)
STAT_TOOLTIPS = {
    "Name": "Player name and team",
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
    "Impact Score": "A performance rating that measures your total positive contribution (points, assists, rebounds, defense) minus negative plays (turnovers and fouls).",
}


def show_live_dashboard():
    """2️⃣ Live Dashboard - Player Stats Table"""
    st.header("📊 Player Dashboard")
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
    totals["FG%"] = (totals["FGM"] / totals["FGA"].replace(0, pd.NA) * 100).round(1)
    totals["3PT%"] = (totals["ThreePTM"] / totals["ThreePA"].replace(0, pd.NA) * 100).round(1)
    totals["FT%"] = (totals["FTM"] / totals["FTA"].replace(0, pd.NA) * 100).round(1)
    totals["Impact_Score"] = (
        totals["Points"] + totals["Assists"] + totals["Rebounds"]
        + (totals["STL"] / games).fillna(0) + (totals["BLK"] / games).fillna(0)
        - totals["Turnovers"] - totals["Personal Fouls"]
    ).round(1)

    labels = advanced_stats[["Player No.", "Team", "Player_Team_Label"]].drop_duplicates()
    totals = totals.merge(labels, on=["Player No.", "Team"], how="left")
    totals["Name"] = totals["Player_Team_Label"].fillna(
        "Player " + totals["Player No."].astype(str) + " (" + totals["Team"].astype(str) + ")"
    )

    display_df = totals[[
        "Name", "Points", "Rebounds", "Assists", "3PM", "FG Made", "Blocks",
        "OREB", "DREB", "Personal Fouls", "Turnovers",
        "FG%", "3PT%", "FT%", "Impact_Score"
    ]].copy()
    display_df = display_df.rename(columns={"Impact_Score": "Impact Score"})
    # Format percentages to 1 decimal
    for pct_col in ["FG%", "3PT%", "FT%"]:
        if pct_col in display_df.columns:
            display_df[pct_col] = display_df[pct_col].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")

    column_config = {col: st.column_config.Column(col, help=STAT_TOOLTIPS.get(col, "")) for col in display_df.columns if STAT_TOOLTIPS.get(col)}
    st.dataframe(display_df, use_container_width=True, hide_index=True, column_config=column_config)

    # Optional bar chart
    if st.checkbox("Show player comparison chart", value=False):
        fig = px.bar(
            display_df.sort_values("Impact Score", ascending=True).tail(12),
            x="Name",
            y="Impact Score",
            title="Impact Score by Player",
            color="Impact Score",
            color_continuous_scale="Blues",
        )
        fig.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("💡 AI Assistant")
    st.caption("Ask questions about performance, training, or game strategy.")
    render_ai_chat_interface(player_profile=None)

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
    elif page == "sample_report":
        show_sample_report()

    else:
        show_homepage()


if __name__ == "__main__":
    main()
