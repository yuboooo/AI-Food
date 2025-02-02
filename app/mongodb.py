from pymongo import MongoClient
import streamlit as st
from datetime import datetime
import base64

class MongoDB:
    def __init__(self):
        try:
            # Get connection string from streamlit secrets
            mongodb_uri = st.secrets["mongodb"]["MONGODB_URI"]
            
            # Connection with timeout and proper options
            self.client = MongoClient(
                mongodb_uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=None,
                connect=True
            )
            
            # Test the connection
            self.client.server_info()
            
            self.db = self.client.food_ai_db
            self.users = self.db.users
            
            print("MongoDB connection successful")
            
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise Exception("Failed to connect to MongoDB")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def save_analysis(self, email, image_data, ingredients, final_nutrition_info, text_summary):
        """Save food analysis with image, ingredients, nutrition info, and summary"""
        # Convert image to base64 for storage
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        analysis_entry = {
            "date": datetime.now(),
            "image": image_base64,
            "ingredients": ingredients,
            "final_nutrition_info": final_nutrition_info,
            "text_summary": text_summary
        }
        
        self.users.update_one(
            {"email": email},
            {"$push": {"food_history": analysis_entry}},
            upsert=True
        )

    def get_user_history(self, email):
        """Get all food analysis history for a user"""
        user = self.users.find_one({"email": email})
        if user and "food_history" in user:
            return user["food_history"]
        return []

    def create_or_get_user(self, google_user):
        """Create a new user or get existing user after Google authentication"""
        user = self.users.find_one({"email": google_user["email"]})
        
        if not user:
            # Create new user document
            user_data = {
                "email": google_user["email"],
                "name": google_user["name"],
                "picture": google_user.get("picture", ""),
                "created_at": datetime.now(),
                "food_history": []  # Initialize empty history
            }
            self.users.insert_one(user_data)
            return user_data
        
        return user