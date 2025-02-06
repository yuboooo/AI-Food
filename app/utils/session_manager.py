import streamlit as st
from mongodb import MongoDB
from streamlit_google_auth import Authenticate
import tempfile
import json
import os

def get_authenticator():
    """Get or create the authenticator instance"""
    if 'authenticator' not in st.session_state:
        google_credentials = {
            "web": {
                "client_id": st.secrets["google"]["client_id"],
                "client_secret": st.secrets["google"]["client_secret"],
                "project_id": st.secrets["google"]["project_id"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": [st.secrets["google"]["redirect_uri"]],
                "javascript_origins": "https://food-ai.streamlit.app"
            }
        }

        # Create temporary credentials file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(google_credentials, f)
            temp_credentials_path = f.name

        st.session_state.authenticator = Authenticate(
            secret_credentials_path=temp_credentials_path,
            cookie_name='my_cookie_name',
            cookie_key='this_is_secret',
            redirect_uri=st.secrets["google"]["redirect_uri"],
        )
        
        # Clean up temporary file
        os.unlink(temp_credentials_path)
        
    return st.session_state.authenticator

def verify_session():
    """Verify user session and return user data if valid"""
    authenticator = get_authenticator()
    
    # First check if user is already authenticated via Google
    authenticator.check_authentification()
    
    # If Google auth is successful, update session state
    if st.session_state.get('connected'):
        if 'user' not in st.session_state:
            st.session_state['user'] = {
                "email": st.session_state['user_info'].get('email'),
                "name": st.session_state['user_info'].get('name'),
                "picture": st.session_state['user_info'].get('picture')
            }
            # Create/update MongoDB session
            with MongoDB() as mongo:
                user_data = mongo.create_or_get_user(st.session_state['user_info'])
                st.query_params['session_token'] = user_data['session_token']
        return True
        
    # If not authenticated via Google, check for session token
    session_token = st.query_params.get('session_token', None)
    if session_token:
        with MongoDB() as mongo:
            user = mongo.verify_session(session_token)
            if user:
                st.session_state['connected'] = True
                st.session_state['user_info'] = {
                    'email': user['email'],
                    'name': user['name'],
                    'picture': user.get('picture', '')
                }
                st.session_state['user'] = st.session_state['user_info']
                return True
    
    return False

def require_auth():
    """Use this for pages that require authentication"""
    if not verify_session():
        st.error("Please log in to access this page")
        authenticator = get_authenticator()
        authenticator.login()
        st.stop()

def show_user_sidebar():
    """Display user info and logout button in sidebar"""
    with st.sidebar:
        st.markdown("---")  # Add separator
        if st.session_state.get('connected'):
            # User info section at bottom of sidebar
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(st.session_state['user_info'].get('picture'), width=50)
                with col2:
                    st.write(f"👤 {st.session_state['user_info'].get('name')}")
                    st.write(f"📧 {st.session_state['user_info'].get('email')}")
                
                if st.button('🚪 Log out'):
                    with MongoDB() as mongo:
                        mongo.invalidate_session(st.session_state['user_info'].get('email'))
                    st.query_params.clear()
                    for key in ['connected', 'user_info', 'user']:
                        if key in st.session_state:
                            del st.session_state[key]
                    get_authenticator().logout()
                    st.rerun()
        else:
            st.write("Not logged in")
            authenticator = get_authenticator()
            authenticator.login() 