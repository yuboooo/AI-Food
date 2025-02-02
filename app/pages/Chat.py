# chat.py
import streamlit as st
from mongodb import MongoDB
from utils.session_manager import require_auth
from user import show_user_profile
from utils.session_manager import get_authenticator

authenticator = get_authenticator()

st.title("Chat and Friend Management")

# Require authentication for this page
require_auth()

# User is authenticated at this point
user = st.session_state["user"]

# Display user profile
show_user_profile(authenticator)

# --- Send Friend Request Interface ---
st.header("Send a Friend Request")
new_friend_email = st.text_input("Enter the email of the person you want to add:")
if st.button("Send Friend Request"):
    if new_friend_email:
        with MongoDB() as mongo:
            result = mongo.send_friend_request(user["email"], new_friend_email)
            st.write(result["message"])
    else:
        st.warning("Please enter a valid email.")

# --- Pending Friend Requests ---
st.header("Pending Friend Requests")
with MongoDB() as mongo:
    pending_requests = mongo.get_pending_friend_requests(user["email"])

if pending_requests:
    for requester in pending_requests:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"Friend request from: {requester}")
        with col2:
            if st.button("Approve", key=f"approve_{requester}"):
                with MongoDB() as mongo:
                    result = mongo.approve_friend_request(user["email"], requester)
                    st.success(result["message"])
                    st.rerun()
        with col3:
            if st.button("Decline", key=f"decline_{requester}"):
                with MongoDB() as mongo:
                    result = mongo.decline_friend_request(user["email"], requester)
                    st.info(result["message"])
                    st.rerun()
else:
    st.info("No pending friend requests.")

# --- Confirmed Friend List with Delete Option ---
st.header("Your Confirmed Friends")
with MongoDB() as mongo:
    confirmed_friends = mongo.get_friend_list(user["email"])

if confirmed_friends:
    for friend in confirmed_friends:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(friend)
        with col2:
          # Instead of calling st.experimental_rerun(), update the UI variables manually.
          if st.button("Delete", key=f"delete_{friend}"):
              with MongoDB() as mongo:
                  result = mongo.delete_friend(user["email"], friend)
                  st.write(result["message"])
                  # Manually update the confirmed_friends variable
                  confirmed_friends = mongo.get_friend_list(user["email"])
                  st.session_state["confirmed_friends"] = confirmed_friends
                  st.success("Friend deleted! Please refresh the page to see the update.")

else:
    st.info("No confirmed friends yet.")

# --- Chat Section (Placeholder) ---
st.header("Chat")
st.write("Chat functionality coming soon!")
