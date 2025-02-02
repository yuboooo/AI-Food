import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from streamlit_calendar import calendar
from mongodb import MongoDB
import json
from user import show_user_profile
from utils.session_manager import get_authenticator



authenticator = get_authenticator()

def show_profile():
    st.title("Nutrition Profile Dashboard")
    show_user_profile(authenticator)
    # Assuming we have a user's nutrition history stored in a database
    # For now, let's create sample data
    @st.cache_data
    def load_user_nutrition_history():
        # This should be replaced with actual database queries
        dates = pd.date_range(end=datetime.now(), periods=30).tolist()
        sample_data = {
            'date': dates,
            'calories': [random.randint(1500, 2500) for _ in range(30)],
            'protein': [random.randint(40, 100) for _ in range(30)],
            'carbs': [random.randint(150, 300) for _ in range(30)],
            'fat': [random.randint(30, 80) for _ in range(30)]
        }
        return pd.DataFrame(sample_data)

    # Load user data
    user_data = load_user_nutrition_history()

    # Create dashboard layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Calorie intake over time
        st.subheader("Calorie Intake Timeline")
        fig_calories = px.line(user_data, x='date', y='calories',
                             title='Daily Calorie Intake')
        st.plotly_chart(fig_calories)

        # Macronutrient distribution
        st.subheader("Macronutrient Distribution")
        fig_macros = go.Figure()
        for macro in ['protein', 'carbs', 'fat']:
            fig_macros.add_trace(go.Scatter(x=user_data['date'], 
                                          y=user_data[macro],
                                          name=macro.capitalize()))
        st.plotly_chart(fig_macros)

    with col2:
        # Summary statistics
        st.subheader("Weekly Summary")
        recent_data = user_data.tail(7)
        
        avg_calories = recent_data['calories'].mean()
        avg_protein = recent_data['protein'].mean()
        avg_carbs = recent_data['carbs'].mean()
        avg_fat = recent_data['fat'].mean()

        st.metric("Avg. Daily Calories", f"{avg_calories:.0f} kcal")
        st.metric("Avg. Daily Protein", f"{avg_protein:.1f}g")
        st.metric("Avg. Daily Carbs", f"{avg_carbs:.1f}g")
        st.metric("Avg. Daily Fat", f"{avg_fat:.1f}g")

        # Progress towards goals
        st.subheader("Goals Progress")
        # These should be customizable by user
        calorie_goal = 2000
        protein_goal = 80
        carbs_goal = 250
        fat_goal = 65

        progress_calories = avg_calories / calorie_goal
        st.progress(min(progress_calories, 1.0), "Calories")
        
        progress_protein = avg_protein / protein_goal
        st.progress(min(progress_protein, 1.0), "Protein")
        
        progress_carbs = avg_carbs / carbs_goal
        st.progress(min(progress_carbs, 1.0), "Carbs")
        
        progress_fat = avg_fat / fat_goal
        st.progress(min(progress_fat, 1.0), "Fat")

    # Add a separator
    st.markdown("---")
    
    # Calendar Section
    st.subheader("Food History Calendar")
    
    # Simple calendar styling
    st.markdown("""
        <style>
        .fc {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
        }
        .fc-event {
            border-radius: 5px !important;
            padding: 2px 5px !important;
        }
        .fc-day-today {
            background-color: #e8f5e9 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    try:
        mongo = MongoDB()
        user_data = mongo.users.find_one({"email": st.session_state['user_info'].get('email')})
        food_history = user_data.get('food_history', []) if user_data else []
        
        # Group meals by date
        meals_by_date = {}
        for entry in food_history:
            date_str = entry['date'].isoformat() if isinstance(entry['date'], datetime) else entry['date']
            date_key = date_str.split('T')[0]
            if date_key not in meals_by_date:
                meals_by_date[date_key] = []
            meals_by_date[date_key].append(entry)
        
        # Create individual events for each meal
        calendar_events = []
        for date, meals in meals_by_date.items():
            # Sort meals by datetime
            meals.sort(key=lambda x: x['date'] if isinstance(x['date'], datetime) else x['date'])
            
            # Create an event for each meal
            for i, meal in enumerate(meals, 1):
                meal_time = meal['date']
                if isinstance(meal_time, datetime):
                    start_time = meal_time.isoformat()
                else:
                    start_time = date
                
                event = {
                    'title': f"Meal {i}",
                    'start': start_time,
                    'id': f"{date}-meal-{i}",
                    'backgroundColor': '#4CAF50',
                    'borderColor': '#4CAF50',
                    'textColor': '#ffffff',
                }
                calendar_events.append(event)
        
        # Calendar configuration
        calendar_options = {
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,timeGridDay",
            },
            "initialView": "dayGridMonth",
            "selectable": True,
            "dayMaxEvents": True,
            "editable": False,
            "events": calendar_events,
            "height": 650,
        }
        
        # Display calendar
        calendar_state = calendar(events=calendar_events, options=calendar_options)
        
        # Show food details when a meal is selected
        if calendar_state and 'eventClick' in calendar_state:
            event_id = calendar_state['eventClick']['event']['id']
            date = event_id.split('-meal-')[0]
            meal_index = int(event_id.split('-meal-')[1]) - 1
            
            selected_meals = meals_by_date.get(date, [])
            if selected_meals and meal_index < len(selected_meals):
                selected_meal = selected_meals[meal_index]
                # Add the date as a main title
                meal_date = datetime.fromisoformat(date) if isinstance(date, str) else date
                st.markdown(f"# 📅 {meal_date.strftime('%B %d, %Y')}")
                
                # Create dropdown for meal selection
                meal_options = [f"Meal {i+1}" for i in range(len(selected_meals))]
                selected_meal_index = st.selectbox(
                    "Select meal to view details",
                    range(len(meal_options)),
                    format_func=lambda x: meal_options[x],
                    index=meal_index
                )
                
                # Display details for the selected meal
                selected_meal = selected_meals[selected_meal_index]
                st.markdown(f"### 🍽️ {meal_options[selected_meal_index]} Details")
                display_meal_details(selected_meal)

    except Exception as e:
        st.error(f"Error loading food history: {str(e)}")

def display_meal_details(entry):
    """Helper function to display detailed meal information"""
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("##### 📋 Ingredients")
        ingredients_list = "• " + "\n• ".join(entry['ingredients'])
        st.markdown(ingredients_list)
        
        st.markdown("##### 📝 Summary")
        st.markdown(f"_{entry['text_summary']}_")
    
    with col2:
        st.markdown("##### 📊 Detailed Nutrition")
        nutrition_info = entry.get('final_nutrition_info', [])
        
        # Define nutrient display names and units
        nutrient_display = {
            "energy": ("Calories", "kcal"),
            "protein": ("Protein", "g"),
            "carbs": ("Carbohydrates", "g"),
            "fat": ("Fat", "g")
        }
        
        # Check if nutrition_info is a list
        if isinstance(nutrition_info, list):
            # Display each nutrient's range
            for item in nutrition_info:
                if isinstance(item, dict):  # Verify item is a dictionary
                    nutrient = item.get('nutrient', '')
                    if nutrient in nutrient_display:
                        display_name, unit = nutrient_display[nutrient]
                        min_val = float(str(item.get('min', 0)).replace(',', ''))
                        max_val = float(str(item.get('max', 0)).replace(',', ''))
                        st.markdown(
                            f"**{display_name}:** {min_val:.1f} - {max_val:.1f} {unit}"
                        )
        elif isinstance(nutrition_info, dict):
            # Handle case where nutrition_info is a dictionary
            for nutrient, value in nutrition_info.items():
                if nutrient in nutrient_display:
                    display_name, unit = nutrient_display[nutrient]
                    try:
                        # Convert value to float, handling string values
                        value = float(str(value).replace(',', ''))
                        st.markdown(f"**{display_name}:** {value:.1f} {unit}")
                    except (ValueError, TypeError):
                        # If conversion fails, display the raw value
                        st.markdown(f"**{display_name}:** {value} {unit}")
        
        # Add time information if available
        if isinstance(entry['date'], datetime):
            st.markdown("##### 🕒 Time")
            st.markdown(entry['date'].strftime("%I:%M %p"))

if __name__ == "__main__":
    show_profile()