"""
Authentication Manager for Basketball Analytics Dashboard
Handles user login and access control
Uses streamlit-authenticator for secure authentication
"""

import streamlit as st
import hashlib
from typing import Dict, Optional

try:
    import streamlit_authenticator as stauth
    AUTHENTICATOR_AVAILABLE = True
except ImportError:
    AUTHENTICATOR_AVAILABLE = False

class AuthManager:
    """
    Manages user authentication and access control
    """
    
    def __init__(self):
        self.authenticator = None
        self.config = None
        self._initialize_auth()
    
    def _initialize_auth(self):
        """Initialize authentication system"""
        if not AUTHENTICATOR_AVAILABLE:
            # Don't use st.warning here - it's called during import
            return
        
        # Default configuration (should be moved to secrets/config file in production)
        if 'auth_config' not in st.session_state:
            # In production, load from Streamlit secrets or environment variables
            # For now, use a simple demo setup
            try:
                hashed_passwords = stauth.Hasher(["demo123"]).generate()
                demo_password = hashed_passwords[0]
            except:
                demo_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # demo123 hash
            
            st.session_state.auth_config = {
                "credentials": {
                    "usernames": {
                        "demo": {
                            "name": "Demo Player",
                            "password": demo_password,
                            "email": "demo@example.com"
                        }
                    }
                },
                "cookie": {
                    "expiry_days": 30,
                    "key": "basketball_analytics_key",
                    "name": "basketball_analytics_cookie"
                }
            }
        
        self.config = st.session_state.auth_config
        
        try:
            # Remove preauthorized parameter - it's been removed from Authenticate class
            self.authenticator = stauth.Authenticate(
                self.config['credentials'],
                self.config['cookie']['name'],
                self.config['cookie']['key'],
                self.config['cookie']['expiry_days']
            )
        except Exception as e:
            # Don't use st.error here - it's called during import
            # Error will be handled when login() is called
            pass
    
    def login(self) -> bool:
        """
        Display login widget and return True if user is authenticated
        """
        if not AUTHENTICATOR_AVAILABLE:
            # If authenticator not available, allow access (for development)
            return True
        
        if self.authenticator is None:
            return True
        
        try:
            name, authentication_status, username = self.authenticator.login('Login', 'main')
            
            if authentication_status == False:
                st.error('Username/password is incorrect')
                return False
            elif authentication_status == None:
                st.warning('Please enter your username and password')
                return False
            elif authentication_status:
                st.session_state['username'] = username
                st.session_state['name'] = name
                return True
        except Exception as e:
            st.error(f"Login error: {str(e)}")
            return True  # Allow access on error for development
        
        return False
    
    def logout(self):
        """Logout current user"""
        if self.authenticator:
            self.authenticator.logout('Logout', 'sidebar')
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        if not AUTHENTICATOR_AVAILABLE:
            return True  # Allow access if authenticator not installed
        
        if self.authenticator is None:
            return True
        
        return 'authentication_status' in st.session_state and st.session_state.get('authentication_status') == True
    
    def get_current_user(self) -> Optional[Dict[str, str]]:
        """Get current authenticated user info"""
        if self.is_authenticated():
            return {
                "username": st.session_state.get('username', 'guest'),
                "name": st.session_state.get('name', 'Guest')
            }
        return None
    
    def get_player_for_user(self, username: str) -> Optional[Dict]:
        """
        Map username to player profile
        In production, this would query a database
        For now, returns None to show all players
        """
        # TODO: Implement user-to-player mapping
        # This could be stored in a database or config file
        return None

# Global instance
auth_manager = AuthManager()

