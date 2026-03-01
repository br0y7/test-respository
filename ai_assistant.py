"""
AI Assistant Module for Basketball Analytics Dashboard
Handles AI-powered coaching advice and chat interface
Uses OpenAI API (can be switched to other providers)
"""

import os
from typing import Dict, List, Optional, Any
from data_manager import data_manager
from ai_knowledge_base import get_full_knowledge_base

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

import requests

# Import streamlit only when needed to avoid issues during module import
try:
    import streamlit as st
except:
    st = None

class AIAssistant:
    """
    AI Assistant for providing personalized basketball coaching advice
    """
    
    def __init__(self):
        # Try to get API key from environment or Streamlit secrets
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.backend_url = os.getenv("AI_BACKEND_URL")  # e.g. http://127.0.0.1:3000
        if st is not None:
            try:
                self.api_key = self.api_key or st.secrets.get("OPENAI_API_KEY", None)
                self.backend_url = self.backend_url or st.secrets.get("AI_BACKEND_URL", None)
            except:
                pass
        
        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            self.enabled = True
        else:
            self.enabled = False
            self.client = None

        # If a backend URL is configured, prefer it (backend-only mode)
        self.backend_enabled = bool(self.backend_url)
    
    def generate_coaching_prompt(self, player_profile: Dict[str, Any]) -> str:
        """
        Generate structured prompt for AI based on player data
        This is the key to getting personalized, actionable advice
        """
        if "error" in player_profile:
            return "Player data not available."
        
        stats = player_profile.get("stats", {})
        strengths = player_profile.get("strengths", [])
        weaknesses = player_profile.get("weaknesses", [])
        advanced_stats = player_profile.get("advanced_stats", {})
        
        # Get knowledge base for context
        knowledge_base = get_full_knowledge_base()
        
        prompt = f"""You are a professional NBA shooting coach and basketball development specialist with access to comprehensive basketball knowledge.

{knowledge_base}

PLAYER PROFILE:
- Player Number: {player_profile.get('player_no')}
- Team: {player_profile.get('team')}
- Total Games Played: {player_profile.get('total_games')}

PERFORMANCE STATISTICS:
- Points: {stats.get('points', {}).get('average', 0):.1f} PPG (Max: {stats.get('points', {}).get('max', 0)})
- Rebounds: {stats.get('rebounds', {}).get('average', 0):.1f} RPG (Max: {stats.get('rebounds', {}).get('max', 0)})
- Assists: {stats.get('assists', {}).get('average', 0):.1f} APG (Max: {stats.get('assists', {}).get('max', 0)})
- Turnovers: {stats.get('turnovers', {}).get('average', 0):.1f} TPG
- Steals: {stats.get('steals', {}).get('average', 0):.1f} SPG
- Blocks: {stats.get('blocks', {}).get('average', 0):.1f} BPG

SHOOTING PERCENTAGES:
- Field Goal %: {stats.get('shooting', {}).get('fg_pct', 0):.1%}
- Three-Point %: {stats.get('shooting', {}).get('three_pct', 0):.1%}
- Free Throw %: {stats.get('shooting', {}).get('ft_pct', 0):.1%}"""
        
        if advanced_stats:
            prompt += f"""

ADVANCED METRICS:
- Assist/Turnover Ratio: {advanced_stats.get('ast_tov_ratio', 0):.2f}
- True Shooting %: {advanced_stats.get('ts_percentage', 0):.1f}%
- Rebound %: {advanced_stats.get('reb_percentage', 0):.1f}%
- Win Shares: {advanced_stats.get('ws', 0):.2f}
- VORP: {advanced_stats.get('vorp', 0):.3f}"""
        
        prompt += f"""

IDENTIFIED STRENGTHS: {', '.join(strengths) if strengths else 'None specifically identified'}
IDENTIFIED WEAKNESSES: {', '.join(weaknesses) if weaknesses else 'None specifically identified'}

YOUR TASK: Provide personalized, actionable coaching advice using the drill library and knowledge base above. Focus on:
1. How to leverage strengths to create advantages
2. Specific drills from the drill library to address weaknesses (mention drill names and durations)
3. Game strategy recommendations based on their playing style
4. 2-3 concrete, measurable improvement goals

Keep responses concise, practical, and encouraging. Use basketball terminology appropriately. Reference specific drills from the library when recommending training."""
        
        return prompt
    
    def get_ai_response(self, user_question: str, player_profile: Optional[Dict[str, Any]] = None) -> str:
        """
        Get AI response to user question with player context
        """
        if self.backend_enabled:
            try:
                system_prompt = None
                if player_profile:
                    system_prompt = self.generate_coaching_prompt(player_profile)

                r = requests.post(
                    f"{self.backend_url.rstrip('/')}/api/ask",
                    json={"message": user_question, "system_prompt": system_prompt},
                    timeout=30,
                )
                if r.status_code != 200:
                    return f"Backend error ({r.status_code}): {r.text}"
                return r.json().get("reply", "")
            except Exception as e:
                return f"Error calling backend AI: {str(e)}"

        if not self.enabled or self.client is None:
            return "⚠️ AI Assistant is not available. Configure AI_BACKEND_URL (recommended) or OPENAI_API_KEY."
        
        try:
            # Build messages for chat
            messages = []
            
            # System message with player context
            if player_profile:
                system_prompt = self.generate_coaching_prompt(player_profile)
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            else:
                # General advice mode - include full knowledge base
                knowledge_base = get_full_knowledge_base()
                messages.append({
                    "role": "system",
                    "content": f"""You are a professional basketball coach assistant with access to comprehensive basketball knowledge.

{knowledge_base}

You can help with:
- Player-specific coaching advice (when player profile is provided)
- League-wide statistics and leaderboards
- Team scouting reports (strengths/weaknesses)
- Specific drill recommendations from the drill library
- Basketball training and skill development

Provide helpful, actionable advice using the knowledge above. Always include stat definitions when showing leaderboards. Use specific drills from the drill library when recommending training."""
                })
            
            # Add conversation history if available
            if st is not None and 'chat_history' in st.session_state:
                for msg in st.session_state.chat_history[-6:]:  # Last 6 messages for context
                    messages.append(msg)
            
            # Add current question
            messages.append({
                "role": "user",
                "content": user_question
            })
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Can be upgraded to gpt-4
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_message = response.choices[0].message.content
            
            # Update chat history
            if st is not None:
                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []
                
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_question
                })
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": ai_message
                })
            
            return ai_message
            
        except Exception as e:
            return f"Error getting AI response: {str(e)}. Please check your API key and connection."
    
    def get_personalized_feedback(self, player_profile: Dict[str, Any]) -> str:
        """
        Generate automatic personalized feedback based on player stats
        """
        if self.backend_enabled:
            prompt = self.generate_coaching_prompt(player_profile)
            try:
                r = requests.post(
                    f"{self.backend_url.rstrip('/')}/api/ask",
                    json={
                        "message": "Provide a comprehensive personalized coaching analysis and improvement plan for this player.",
                        "system_prompt": prompt,
                    },
                    timeout=30,
                )
                if r.status_code != 200:
                    return f"Backend error ({r.status_code}): {r.text}"
                return r.json().get("reply", "")
            except Exception as e:
                return f"Error calling backend AI: {str(e)}"

        if not self.enabled or self.client is None:
            return "⚠️ AI Assistant is not available. Configure AI_BACKEND_URL (recommended) or OPENAI_API_KEY."
        
        prompt = self.generate_coaching_prompt(player_profile)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Provide a comprehensive personalized coaching analysis and improvement plan for this player."}
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating feedback: {str(e)}"

# Global instance
ai_assistant = AIAssistant()

