import streamlit as st
from src.db import users_col


def load_profile(email):
    """Load user profile data from MongoDB."""
    user = users_col.find_one({"email": email})
    return user.get('profile', {}) if user else {}


def save_profile(email, profile_data):
    """Save/update user profile data in MongoDB."""
    users_col.update_one({"email": email}, {"$set": {"profile": profile_data}})


def profile_form():
    # Removed call to inject_custom_css()

    user_email = st.session_state['user']['email']
    profile = load_profile(user_email)

    st.header("Complete Your Profile")

    plan_options = [
        "Jio Unlimited 999",
        "Jio 499 Plan",
        "Jio 299 Plan",
        "Jio 199 Plan",
        "Jio 1499 Annual Plan"
    ]
    current_plan_default_index = plan_options.index(profile.get('current_plan')) if profile.get('current_plan') in plan_options else 0
    current_plan = st.selectbox("Current Plan Name", options=plan_options, index=current_plan_default_index, key="current_plan")

    monthly_bill = st.number_input(
        "Monthly Bill Amount (₹)", min_value=0.0, value=profile.get('monthly_bill', 0.0), key="monthly_bill"
    )

    budget_options = [0, 199, 299, 499, 999, 1499]
    budget_labels = ["No preference", "₹199", "₹299", "₹499", "₹999", "₹1499"]
    budget_default_index = budget_options.index(profile.get('budget', 0)) if profile.get('budget') in budget_options else 0
    budget_label = st.selectbox("Preferred Budget", options=budget_labels, index=budget_default_index, key="budget_label")
    budget = budget_options[budget_labels.index(budget_label)]

    data_usage = st.number_input(
        "Monthly Data Usage (GB)", min_value=0.0, value=profile.get('data_usage', 0.0), key="data_usage"
    )
    call_minutes = st.number_input(
        "Monthly Call Minutes", min_value=0, value=profile.get('call_minutes', 0), key="call_minutes"
    )
    sms_count = st.number_input(
        "Monthly SMS Count", min_value=0, value=profile.get('sms_count', 0), key="sms_count"
    )

    if st.button("Save Profile", key="save_profile"):
        new_profile = {
            "data_usage": data_usage,
            "call_minutes": call_minutes,
            "sms_count": sms_count,
            "current_plan": current_plan,
            "monthly_bill": monthly_bill,
            "budget": budget
        }
        save_profile(user_email, new_profile)
        st.success("Profile saved successfully!")
