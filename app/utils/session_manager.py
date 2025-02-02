import streamlit as st
from mongodb import MongoDB
from streamlit_google_auth import Authenticate

def get_authenticator():
    """Get or create the authenticator instance"""
    if 'authenticator' not in st.session_state:
        st.session_state.authenticator = Authenticate(
            secret_credentials_path='./.streamlit/google_credentials.json',
            cookie_name='my_cookie_name',
            cookie_key='this_is_secret',
            redirect_uri='http://localhost:5173',
        )
    return st.session_state.authenticator

def verify_session():
    """Verify user session and return user data if valid"""
    authenticator = get_authenticator()
    
    # First check if user is already authenticated via Google
    authenticator.check_authentification()
    
    if st.session_state.get('connected'):
        # User is authenticated via Google
        if 'user' not in st.session_state:
            st.session_state['user'] = {
                "email": st.session_state['user_info'].get('email'),
                "name": st.session_state['user_info'].get('name'),
                "picture": st.session_state['user_info'].get('picture')
            }
        return True
        
    # If not authenticated via Google, check for session token
    if 'user' not in st.session_state:
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
    return True 