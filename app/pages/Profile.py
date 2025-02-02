import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from streamlit_calendar import calendar
from mongodb import MongoDB
import json

def show_profile():
    st.title("Nutrition Profile Dashboard")
    
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
    
    # Add custom CSS for calendar styling
    st.markdown("""
        <style>
        /* Calendar container */
        .fc {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        /* Header styling */
        .fc-toolbar-title {
            color: #1f1f1f !important;
            font-size: 1.3em !important;
            font-weight: 600 !important;
        }
        
        /* Button styling */
        .fc-button {
            background-color: #4CAF50 !important;
            border-color: #4CAF50 !important;
            color: white !important;
            box-shadow: none !important;
            border-radius: 5px !important;
            padding: 6px 12px !important;
        }
        
        .fc-button:hover {
            background-color: #45a049 !important;
            border-color: #45a049 !important;
        }
        
        /* Today button */
        .fc-today-button {
            background-color: #2196F3 !important;
            border-color: #2196F3 !important;
        }
        
        /* Calendar cells */
        .fc-daygrid-day {
            transition: background-color 0.2s;
        }
        
        .fc-daygrid-day:hover {
            background-color: #f5f5f5;
        }
        
        /* Today's date highlight */
        .fc-day-today {
            background-color: #e8f5e9 !important;
        }
        
        /* Event styling */
        .fc-event {
            border-radius: 5px !important;
            padding: 2px 5px !important;
            margin: 2px 0 !important;
            border: none !important;
            transition: transform 0.2s;
        }
        
        .fc-event:hover {
            transform: scale(1.02);
        }
        
        /* Week numbers */
        .fc-week-number {
            color: #666;
            font-size: 0.9em;
        }
        
        /* Header cells */
        .fc-col-header-cell {
            background-color: #f8f9fa;
            padding: 10px 0 !important;
            font-weight: 600 !important;
        }
        
        /* More events popup */
        .fc-more-popover {
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize active meal index in session state if not exists
    if 'active_meal_index' not in st.session_state:
        st.session_state.active_meal_index = 0

    try:
        mongo = MongoDB()
        user_data = mongo.users.find_one({"email": st.session_state['user_info'].get('email')})
        food_history = user_data.get('food_history', []) if user_data else []
        
        # Create calendar events from food history
        calendar_events = []
        for entry in food_history:
            if isinstance(entry['date'], str):
                date_str = entry['date']
            else:
                date_str = entry['date'].isoformat()
                
            event = {
                'title': f"🍽️ {', '.join(entry['ingredients'][:2])}",
                'start': date_str,
                'end': date_str,
                'id': date_str,
                'allDay': True,
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
                "right": "dayGridMonth",
            },
            "initialView": "dayGridMonth",
            "selectable": True,
            "selectMirror": True,
            "dayMaxEvents": True,
            "weekNumbers": False,
            "navLinks": True,
            "editable": False,
            "events": calendar_events,
            "height": 650,  # Fixed height for better appearance
            "aspectRatio": 1.8,  # Width to height ratio
            "firstDay": 1,  # Start week on Monday
            "eventTimeFormat": {
                "hour": "2-digit",
                "minute": "2-digit",
                "meridiem": False
            },
        }
        
        # Display calendar
        calendar_state = calendar(events=calendar_events, options=calendar_options)
        
        # Show food details when a date is selected
        if calendar_state and 'eventClick' in calendar_state:
            selected_event = calendar_state['eventClick']
            selected_date = selected_event['event']['start']
            
            # Find all food entries for the selected date
            selected_entries = [
                entry for entry in food_history 
                if (isinstance(entry['date'], str) and entry['date'].startswith(selected_date)) or
                   (hasattr(entry['date'], 'isoformat') and entry['date'].isoformat().startswith(selected_date))
            ]
            
            if selected_entries:
                st.markdown(f"### 🗓️ Meals for {selected_date.split('T')[0]}")
                
                # Display first entry's nutrition summary
                first_entry = selected_entries[0]
                display_nutrition_summary(first_entry)
                
                # Display all entries in expandable sections
                for i, entry in enumerate(selected_entries):
                    # Create a unique key for each expander
                    expander_key = f"meal_{i}_{selected_date}"
                    
                    # When an expander is clicked, update the active meal index
                    with st.expander(
                        f"🍽️ Meal {i+1}: {', '.join(entry['ingredients'][:2])}...",
                        expanded=(i == st.session_state.active_meal_index)
                    ) as exp:
                        display_meal_details(entry)
                        # If this expander is clicked (expanded), update active_meal_index
                        if exp:
                            st.session_state.active_meal_index = i
                        elif i == st.session_state.active_meal_index and not exp:
                            st.session_state.active_meal_index = None

                # Update nutrition summary to show active meal
                if st.session_state.active_meal_index is not None:
                    active_entry = selected_entries[st.session_state.active_meal_index]
                    display_nutrition_summary(active_entry)

    except Exception as e:
        st.error(f"Error loading food history: {str(e)}")

def display_nutrition_summary(entry):
    """Display a summary card of nutrition information"""
    st.markdown("""
        <style>
        .nutrition-card {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #f0f2f6;
            margin-bottom: 1rem;
        }
        .nutrition-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-top: 0.5rem;
        }
        .nutrition-item {
            text-align: center;
            padding: 0.5rem;
            background-color: white;
            border-radius: 0.3rem;
        }
        </style>
    """, unsafe_allow_html=True)

    nutrition_info = entry['final_nutrition_info']
    
    # Create a clean nutrition summary
    st.markdown('<div class="nutrition-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 Quick Nutrition Summary")
    
    # Display key nutrition metrics in a grid
    cols = st.columns(4)
    metrics = [
        ("Calories", nutrition_info.get('calories', 'N/A'), "🔥"),
        ("Protein", nutrition_info.get('protein', 'N/A'), "🥩"),
        ("Carbs", nutrition_info.get('carbs', 'N/A'), "🌾"),
        ("Fat", nutrition_info.get('fat', 'N/A'), "🥑")
    ]
    
    for col, (label, value, emoji) in zip(cols, metrics):
        col.metric(f"{emoji} {label}", value)
    
    st.markdown('</div>', unsafe_allow_html=True)

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
        for key, value in entry['final_nutrition_info'].items():
            st.markdown(f"**{key}:** {value}")
        
        # Add time information if available
        if isinstance(entry['date'], datetime):
            st.markdown("##### 🕒 Time")
            st.markdown(entry['date'].strftime("%I:%M %p"))

if __name__ == "__main__":
    show_profile()