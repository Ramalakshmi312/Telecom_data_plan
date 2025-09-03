import streamlit as st
import pandas as pd
import plotly.express as px
from src.db import users_col, plans_col

def show_analytics():
    st.title("Analytics Dashboard")

    # Example filters (date filtering logic can be enhanced later)
    st.sidebar.header("Filters")
    date_range = st.sidebar.date_input("Select Date Range", [])

    # KPIs
    total_users = users_col.count_documents({})
    total_plans = plans_col.count_documents({})

    col1, col2 = st.columns(2)
    col1.metric("Total Users", total_users)
    col2.metric("Total Plans", total_plans)

    # Example: Plan usage distribution (dummy data)
    plan_names = [plan['planName'] for plan in plans_col.find()]
    usage_counts = [len(plan_names) - i for i in range(len(plan_names))]  # dummy descending values

    df_usage = pd.DataFrame({'Plan': plan_names, 'UsageCount': usage_counts})

    fig = px.pie(df_usage, names='Plan', values='UsageCount', title='Plan Usage Distribution')
    st.plotly_chart(fig, use_container_width=True)

    st.write("More advanced analytics and filters can be added here.")
