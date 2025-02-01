import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

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

if __name__ == "__main__":
    show_profile()
