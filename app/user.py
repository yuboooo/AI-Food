import streamlit as st
import os

def show_user_profile():
    """Display user profile information"""
    if st.session_state.authenticated:
        st.write("Welcome! You are logged in.")
        # Add any user profile information you want to display here
    else:
        st.write("Please log in to view your profile.")
