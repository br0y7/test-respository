"""
AI Dashboard Integration Module
Provides Streamlit UI components for AI Assistant chat interface
"""

import streamlit as st
from ai_assistant import ai_assistant
from rule_based_assistant import rule_based_assistant, tournament_3on3_assistant
from data_manager import data_manager
from three_on_three_knowledge import get_3on3_tournament_context

def _pick_assistant() -> tuple[object, str]:
    """
    Choose which assistant to use.
    Default: Rule-Based (your coded assistant).
    Optional: OpenAI (if enabled and user selects it).
    """
    # Default selection:
    # - If OpenAI is enabled, start in Hybrid mode (best experience).
    # - Otherwise, start in Rule-Based (always available).
    default_index = 1 if getattr(ai_assistant, "enabled", False) else 0
    choice = st.sidebar.selectbox(
        "Assistant mode",
        ["Rule-Based (your coded assistant)", "Hybrid (Rule-Based + OpenAI)", "OpenAI (paid)"],
        index=default_index,
        help="Rule-Based is free and uses your drill library + logic. OpenAI uses your API key and may cost money.",
    )

    if choice.startswith("OpenAI") and ai_assistant.enabled:
        return ai_assistant, "AI"

    # Hybrid: use your rule-based assistant to draft an answer, then have OpenAI refine it.
    if choice.startswith("Hybrid") and ai_assistant.enabled:
        return ai_assistant, "Hybrid"

    # Default / fallback
    return rule_based_assistant, "Rule-Based"


def _pick_assistant_3on3() -> tuple[object, str]:
    """Assistant mode for the 3 on 3 tournament page — uses tournament CSVs (season 3)."""
    default_index = 1 if getattr(ai_assistant, "enabled", False) else 0
    choice = st.sidebar.selectbox(
        "3 on 3 — Assistant mode",
        ["Rule-Based (3 on 3)", "Hybrid (3 on 3 + OpenAI)", "OpenAI (3 on 3, paid)"],
        index=default_index,
        key="assistant_mode_3on3",
        help="Answers use **this tournament’s** stats. OpenAI is optional and uses your API key.",
    )

    if choice.startswith("OpenAI") and ai_assistant.enabled:
        return ai_assistant, "AI"

    if choice.startswith("Hybrid") and ai_assistant.enabled:
        return ai_assistant, "Hybrid"

    return tournament_3on3_assistant, "Rule-Based"


def render_3on3_ai_chat_interface(player_profile=None):
    """
    Chat for the 3 on 3 tournament dashboard: rule-based + optional OpenAI,
    with tournament-specific context (GCIR, pace, Round Robin vs Playoffs).
    """
    coaching_assistant, assistant_type = _pick_assistant_3on3()
    ctx = get_3on3_tournament_context()

    if assistant_type == "AI":
        st.subheader("🏀 3 on 3 Tournament Assistant")
        st.markdown("Ask about **this tournament**, strategy for 3 on 3, drills, or who’s leading in the stats.")
        st.info("Using OpenAI. Switch to **Rule-Based** in the sidebar if you prefer no API calls.")
    elif assistant_type == "Hybrid":
        st.subheader("🏀 3 on 3 Hybrid Assistant")
        st.markdown("Rule-based answers use **tournament data**; OpenAI refines the reply with 3 on 3 context.")
    else:
        st.subheader("🏀 3 on 3 Tournament Assistant")
        st.markdown("Tips and stats are tuned for **3 on 3** (space, pace, GCIR/GCMVP on this dashboard).")

    hist_key = "chat_history_3on3"
    if hist_key not in st.session_state:
        st.session_state[hist_key] = []

    for message in st.session_state[hist_key]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ask about this 3 on 3 tournament...", key="chat_input_3on3"):
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            with st.spinner(
                "Refining with OpenAI..." if assistant_type in ("AI", "Hybrid") else "Analyzing tournament data..."
            ):
                if assistant_type == "Hybrid":
                    draft = tournament_3on3_assistant.get_ai_response(prompt, player_profile)
                    with st.expander("Rule-based draft (3 on 3 data)"):
                        st.write(draft)

                    refined_prompt = (
                        f"{ctx}\n\n"
                        "You are refining a rule-based coaching draft for a **3 on 3 basketball tournament**.\n\n"
                        f"RULE-BASED DRAFT:\n{draft}\n\n"
                        f"USER QUESTION:\n{prompt}\n\n"
                        "Return a concise, actionable reply. Emphasize 3 on 3: spacing, quick decisions, "
                        "limiting turnovers, and rebounding. Reference GCIR/GCMVP only if it helps the user."
                    )
                    response = coaching_assistant.get_ai_response(refined_prompt, player_profile)
                elif assistant_type == "AI":
                    openai_prompt = f"{ctx}\n\n---\n\nUser question:\n{prompt}"
                    response = coaching_assistant.get_ai_response(openai_prompt, player_profile)
                else:
                    response = tournament_3on3_assistant.get_ai_response(prompt, player_profile)
                st.write(response)

        if (
            len(st.session_state[hist_key]) == 0
            or st.session_state[hist_key][-1]["content"] != response
        ):
            st.session_state[hist_key].append({"role": "user", "content": prompt})
            st.session_state[hist_key].append({"role": "assistant", "content": response})

    if st.button("Clear 3 on 3 chat", key="clear_chat_3on3"):
        st.session_state[hist_key] = []
        st.rerun()


def render_ai_chat_interface(player_profile=None):
    """
    Render ChatGPT-style chat interface for Coaching Assistant (AI or Rule-Based)
    """
    coaching_assistant, assistant_type = _pick_assistant()

    if assistant_type == "AI":
        st.header("🤖 AI Coaching Assistant")
        st.markdown("Ask me anything about your performance, training, or game strategy!")
        st.info("Using OpenAI (paid). If you don’t want to pay, switch Assistant mode to Rule-Based in the sidebar.")
    elif assistant_type == "Hybrid":
        st.header("🤖 Hybrid Coaching Assistant")
        st.markdown("Combines free rule-based analysis with OpenAI refinement.")
        st.info("OpenAI is enabled for refinement; rule-based output is used as context.")
    else:
        st.header("💡 Coaching Assistant")
        st.markdown("Ask me anything about your performance, training, or game strategy!")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your game..."):
        # Add user message to chat
        st.chat_message("user").write(prompt)
        
        # Get coaching response (AI or rule-based)
        with st.chat_message("assistant"):
            with st.spinner(
                "Refining with OpenAI..." if assistant_type in ("AI", "Hybrid") else "Analyzing..."
            ):
                if assistant_type == "Hybrid":
                    # Step 1: rule-based draft (free + deterministic)
                    draft = rule_based_assistant.get_ai_response(prompt, player_profile)
                    with st.expander("Rule-Based draft (used as context)"):
                        st.write(draft)

                    # Step 2: OpenAI refinement using the draft as context
                    refined_prompt = (
                        "You are refining a rule-based coaching draft.\n\n"
                        f"RULE-BASED DRAFT:\n{draft}\n\n"
                        f"USER QUESTION:\n{prompt}\n\n"
                        "Return an improved coaching response that keeps the key insights from the draft, "
                        "but is clearer, more actionable, and more personalized to the player context."
                    )
                    response = coaching_assistant.get_ai_response(refined_prompt, player_profile)
                else:
                    response = coaching_assistant.get_ai_response(prompt, player_profile)
                st.write(response)
        
        # Update history (already done in ai_assistant, but ensure it's displayed)
        if len(st.session_state.chat_history) == 0 or st.session_state.chat_history[-1]["content"] != response:
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt
            })
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

def render_personalized_feedback(player_profile):
    """
    Render automatic personalized feedback section
    """
    st.header("📊 Personalized Performance Analysis")
    
    if "error" in player_profile:
        st.error("Player data not available.")
        return
    
    # Show key stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Points Per Game", f"{player_profile['stats']['points']['average']:.1f}")
        st.metric("Rebounds Per Game", f"{player_profile['stats']['rebounds']['average']:.1f}")
    
    with col2:
        st.metric("Assists Per Game", f"{player_profile['stats']['assists']['average']:.1f}")
        st.metric("Turnovers Per Game", f"{player_profile['stats']['turnovers']['average']:.1f}")
    
    with col3:
        fg_pct = player_profile['stats']['shooting']['fg_pct']
        st.metric("Field Goal %", f"{fg_pct:.1%}")
        three_pct = player_profile['stats']['shooting']['three_pct']
        st.metric("Three-Point %", f"{three_pct:.1%}")
    
    # Strengths and Weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Strengths")
        strengths = player_profile.get('strengths', [])
        if strengths:
            for strength in strengths:
                st.success(f"• {strength}")
        else:
            st.info("Keep working hard!")
    
    with col2:
        st.subheader("🎯 Areas for Improvement")
        weaknesses = player_profile.get('weaknesses', [])
        if weaknesses:
            for weakness in weaknesses:
                st.warning(f"• {weakness}")
        else:
            st.success("Great all-around game!")
    
    coaching_assistant, assistant_type = _pick_assistant()

    # Get coaching feedback (AI or rule-based)
    button_text = "Get AI Coaching Analysis" if assistant_type == "AI" else "Get Coaching Analysis"
    if st.button(button_text, type="primary"):
        with st.spinner("Generating personalized feedback..."):
            feedback = coaching_assistant.get_personalized_feedback(player_profile)
            st.markdown("### 💡 Coaching Analysis")
            st.markdown(feedback)

