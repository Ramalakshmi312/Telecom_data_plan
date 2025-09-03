import streamlit as st
from src.auth import register_user, login_user
from src.profile1 import profile_form
from src.dashboard import show_dashboard
from src.roles import is_customer, is_admin, is_analyst


def show_admin_panel():
    st.title("Admin Panel - Coming Soon")


def show_analytics():
    st.title("Analytics Dashboard - Coming Soon")


def main():
    st.sidebar.title("Telecom Data Plan System")

    if 'user' not in st.session_state:
        st.sidebar.subheader("Login or Register")
        choice = st.sidebar.selectbox("Choose action", ["Login", "Register"])

        if choice == "Register":
            st.markdown('<div class="block-container">', unsafe_allow_html=True)
            st.markdown("## 🎉 **Register New Account**", unsafe_allow_html=True)
            email = st.text_input("📧 Email", key="register_email")
            name = st.text_input("👤 Name", key="register_name")
            password = st.text_input("🔒 Password", type="password", key="register_password")
            if st.button("Register", key="register_btn"):
                if not email or not name or not password:
                    st.error("⚠️ Please fill all fields.")
                else:
                    success, msg = register_user(email, password, name)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
            st.markdown('</div>', unsafe_allow_html=True)

        elif choice == "Login":
            st.markdown('<div class="block-container">', unsafe_allow_html=True)
            st.markdown("## 🔐 **Login to Your Account**", unsafe_allow_html=True)
            email = st.text_input("📧 Email", key="login_email")
            password = st.text_input("🔒 Password", type="password", key="login_password")
            if st.button("Login", key="login_btn"):
                if not email or not password:
                    st.error("⚠️ Please enter both email and password.")
                else:
                    if login_user(email, password):
                        st.session_state['user'] = {'name': email, 'email': email,
                                                    'role': st.session_state['user']['role']}
                        st.success("✅ Logged in successfully!")
                        st.stop()
                    else:
                        st.error("❌ Invalid login credentials.")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.sidebar.subheader(f"Welcome, {st.session_state['user']['name']}!")
        st.sidebar.write(f"Your role: {st.session_state['user']['role']}")  # Debug: show user role

        menu = st.sidebar.radio("Navigation", ["Profile", "Dashboard", "Admin Panel", "Analytics", "Logout"])

        if menu == "Profile":
            profile_form()

        elif menu == "Dashboard":
            if is_customer():
                show_dashboard()
            else:
                st.warning("Dashboard available for Customers only.")

        elif menu == "Admin Panel":
            if is_admin():
                show_admin_panel()
            else:
                st.error("Access denied. Admins only.")

        elif menu == "Analytics":
            if is_analyst():
                show_analytics()
            else:
                st.error("Access denied. Analysts only.")

        elif menu == "Logout":
            st.session_state.pop("user")
            st.warning("You have been logged out.")
            st.stop()


if __name__ == "__main__":
    main()
