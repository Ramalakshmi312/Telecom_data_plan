import streamlit as st
from src.db import users_col, plans_col
from bson.objectid import ObjectId

ROLE_OPTIONS = ["Customer", "Admin", "Analyst"]

def user_management():
    st.markdown("## User Management")

    users = list(users_col.find({}, {"email": 1, "role": 1, "_id": 0}))
    if not users:
        st.info("No users found.")
        return

    st.markdown("### Users and Their Roles")
    for user in users:
        email = user.get("email", "")
        current_role = user.get("role", "Customer")

        cols = st.columns([3, 3, 1])
        cols[0].write(email)
        new_role = cols[1].selectbox(
            f"Select role for {email}",
            ROLE_OPTIONS,
            index=ROLE_OPTIONS.index(current_role),
            key=email,
        )
        if cols[2].button("Save", key=f"save_{email}"):
            users_col.update_one({"email": email}, {"$set": {"role": new_role}})
            st.success(f"Role updated for {email} to {new_role}")


def plan_management():
    st.markdown("## Plan Management")

    plans = list(plans_col.find())
    if plans:
        st.markdown("### Existing Plans")
        for plan in plans:
            cols = st.columns([3, 1, 1])
            cols[0].write(f"{plan.get('planName')} - ₹{plan.get('price')}")
            if cols[1].button("Edit", key=f"edit_{str(plan['_id'])}"):
                st.session_state['edit_plan_id'] = str(plan['_id'])
            if cols[2].button("Delete", key=f"del_{str(plan['_id'])}"):
                plans_col.delete_one({"_id": ObjectId(st.session_state.get('edit_plan_id', plan['_id']))})
                st.success(f"Deleted plan {plan.get('planName')}")
                st.experimental_rerun()
    else:
        st.info("No plans found.")

    with st.form("plan_form", clear_on_submit=True):
        is_editing = 'edit_plan_id' in st.session_state
        plan = None
        if is_editing:
            plan = plans_col.find_one({"_id": ObjectId(st.session_state['edit_plan_id'])})

        plan_name = st.text_input("Plan Name", value=plan.get('planName') if plan else "")
        price = st.number_input("Price (₹)", min_value=0, step=1, value=plan.get('price') if plan else 0)
        data_gb = st.text_input("Data (GB or Unlimited)", value=plan.get('dataGB') if plan else "")
        validity = st.number_input("Validity (days)", min_value=1, step=1, value=plan.get('validityDays') if plan else 1)
        call = st.text_input("Calls", value=plan.get('call') if plan else "")
        sms = st.text_input("SMS", value=plan.get('sms') if plan else "")

        submitted = st.form_submit_button("Save Plan")

        if submitted:
            plan_data = {
                "planName": plan_name,
                "price": price,
                "dataGB": data_gb,
                "validityDays": validity,
                "call": call,
                "sms": sms
            }
            if is_editing:
                plans_col.update_one({"_id": ObjectId(st.session_state['edit_plan_id'])}, {"$set": plan_data})
                st.success(f"Updated plan {plan_name}")
                del st.session_state['edit_plan_id']
            else:
                plans_col.insert_one(plan_data)
                st.success(f"Added new plan {plan_name}")
            st.experimental_rerun()


def show_admin_panel():
    st.title("Admin Panel")
    menu = st.selectbox("Select Admin Section", ["User Management", "Plan Management"])

    if menu == "User Management":
        user_management()
    elif menu == "Plan Management":
        plan_management()
