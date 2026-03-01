"""
AI Dashboard Integration Module
Provides Streamlit UI components for AI Assistant chat interface
"""

import streamlit as st
from ai_assistant import ai_assistant
from rule_based_assistant import rule_based_assistant
from data_manager import data_manager

def _pick_assistant() -> tuple[object, str]:
    """
    Choose which assistant to use.
    Default: Rule-Based (your coded assistant).
    Optional: OpenAI (if enabled and user selects it).
    """
    choice = st.sidebar.selectbox(
        "Assistant mode",
        ["Rule-Based (your coded assistant)", "OpenAI (paid)"],
        index=0,
        help="Rule-Based is free and uses your drill library + logic. OpenAI uses your API key and may cost money.",
    )

    if choice.startswith("OpenAI") and ai_assistant.enabled:
        return ai_assistant, "AI"

    # Default / fallback
    return rule_based_assistant, "Rule-Based"

def render_ai_chat_interface(player_profile=None):
    """
    Render ChatGPT-style chat interface for Coaching Assistant (AI or Rule-Based)
    """
    coaching_assistant, assistant_type = _pick_assistant()

    if assistant_type == "AI":
        st.header("🤖 AI Coaching Assistant")
        st.markdown("Ask me anything about your performance, training, or game strategy!")
        st.info("Using OpenAI (paid). If you don’t want to pay, switch Assistant mode to Rule-Based in the sidebar.")
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
            with st.spinner("Thinking..." if assistant_type == "AI" else "Analyzing..."):
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

