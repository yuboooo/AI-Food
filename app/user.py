import streamlit as st
import os

def show_user_profile(authenticator):
    """Display user profile in the sidebar"""
    with st.sidebar:
        # Push the profile to the bottom using an empty container
        # spacer = st.container()
        
        # Profile container at the bottom
        with st.container():
            st.markdown("### User Profile")
            # Update the path to point to the app directory
            credentials_path = os.path.join('app', 'google_credentials.json')
            
            if 'name' in st.session_state:
                if st.button('Log out'):
                    authenticator.logout()
            else:
                authenticator.login(credentials_path)  # Pass the credentials path
                st.write("Please log in to continue.")