# src/roles.py

import streamlit as st

def is_customer():
    return 'user' in st.session_state and st.session_state['user'].get('role') == 'Customer'

def is_admin():
    return 'user' in st.session_state and st.session_state['user'].get('role') == 'Admin'

def is_analyst():
    return 'user' in st.session_state and st.session_state['user'].get('role') == 'Analyst'
