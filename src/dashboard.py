import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from src.db import users_col
from src.model import recommend_plans_simple

def show_dashboard():
    st.title("Your Telecom Dashboard")

    # Dark theme colors 
    colors = {
        'background': '#1E1E2F',
        'text': '#CCCCCC',
        'pie': ['#5A9BD5', '#F28E2B', '#E15759'],  # blue, orange, red
        'bar_current': '#3E8EDE',  # bright blue
        'bar_recommended': '#E37400',  # orange
        'progress': '#00CC96'  # green
    }
    
    # st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-color: {colors['background']};
#         color: {colors['text']};
#     }}
#     .block-container {{
#         color: {colors['text']};
#     }}
#     </style>
#     """, unsafe_allow_html=True)

    try:
        user_email = st.session_state['user']['email']
        user_data = users_col.find_one({"email": user_email})
        if not user_data:
            st.error("User record not found.")
            return

        profile = user_data.get('profile', {})
        if not profile:
            st.warning("Please complete your profile first!")
            return

        # Usage metrics
        data_usage = profile.get('data_usage', 0)
        call_minutes = profile.get('call_minutes', 0)
        sms_count = profile.get('sms_count', 0)
        monthly_bill = profile.get('monthly_bill', 0.0)
        budget = profile.get('budget', 0)
        current_plan = profile.get('current_plan', 'N/A')

        st.subheader("Usage Summary")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Data Usage (GB)", f"{data_usage}", delta=None)
        col2.metric("Call Minutes", f"{call_minutes}", delta=None)
        col3.metric("SMS Count", f"{sms_count}", delta=None)

        st.markdown(f"**Current Plan:** {current_plan}")
        st.markdown(f"**Monthly Bill:** ₹{monthly_bill}")
        st.markdown(f"**Preferred Budget:** ₹{budget}")

        # Pie chart - usage breakdown
        labels = ['Data (GB)', 'Call Minutes', 'SMS Count']
        values = [data_usage, call_minutes, sms_count]

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker_colors=colors['pie'],
            textinfo='label+percent',
            insidetextorientation='radial'
        )])
        fig_pie.update_layout(
            title_text='Usage Breakdown',
            paper_bgcolor=colors['background'],
            font_color=colors['text']
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Budget usage progress
        if budget > 0:
            usage_ratio = min(monthly_bill / budget, 1.0)
            st.markdown("### Budget Usage")
            st.progress(usage_ratio)
            st.write(f"₹{monthly_bill} billed out of ₹{budget} budget")
            if monthly_bill > budget:
                st.warning("You have exceeded your preferred budget!")

        # Fetch all user profiles for recommendations
        all_users = []
        for user in users_col.find():
            p = user.get('profile', {})
            if p and 'current_plan' in p:
                all_users.append({
                    'email': user.get('email'),
                    'data_usage': p.get('data_usage', 0),
                    'call_minutes': p.get('call_minutes', 0),
                    'sms_count': p.get('sms_count', 0),
                    'current_plan': p.get('current_plan', "")
                })
        all_users_profiles = pd.DataFrame(all_users)

        plans_data = [
            {"planName": "Jio Unlimited 999", "price": 999, "dataGB": "Unlimited 5G", "validityDays": 84, "call": "Unlimited", "sms": "100/day"},
            {"planName": "Jio 499 Plan", "price": 499, "dataGB": "2 GB/day", "validityDays": 28, "call": "Unlimited", "sms": "100/day"},
            {"planName": "Jio 299 Plan", "price": 299, "dataGB": "1.5 GB/day", "validityDays": 28, "call": "Unlimited", "sms": "100/day"},
            {"planName": "Jio 199 Plan", "price": 199, "dataGB": "2 GB total", "validityDays": 18, "call": "Unlimited", "sms": "100/day"},
            {"planName": "Jio 1499 Annual Plan", "price": 1499, "dataGB": "2 GB/day", "validityDays": 365, "call": "Unlimited", "sms": "100/day"},
        ]
        plans_df = pd.DataFrame(plans_data)

        with st.spinner('Generating recommendations...'):
            recommendations = recommend_plans_simple(profile, all_users_profiles, plans_df, n=5)

        st.subheader("Plan Comparison")
        # Bar chart comparing current plan price vs recommended plan prices
        bar_labels = ['Current Plan'] + recommendations['planName'].tolist()
        bar_prices = [monthly_bill] + recommendations['price'].tolist()
        bar_colors = [colors['bar_current']] + [colors['bar_recommended']] * len(recommendations)

        fig_bar = go.Figure([
            go.Bar(name='Price (₹)', x=bar_labels, y=bar_prices, marker_color=bar_colors)
        ])
        fig_bar.update_layout(
            title='Current Plan vs Recommended Plans',
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            yaxis_title='Price (₹)',
            xaxis_title='Plan'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Display recommendations with expanders
        st.subheader("Recommended Plans Details")
        for idx, row in recommendations.iterrows():
            with st.expander(f"{row['planName']} - ₹{row['price']}", expanded=False):
                st.markdown(f"**Data:** {row['dataGB']}")
                st.markdown(f"**Validity:** {row['validityDays']} days")
                st.markdown(f"**Calls:** {row['call']}")
                st.markdown(f"**SMS:** {row['sms']}")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
