import streamlit as st

ALLOWED_EMAILS = {
    "martin.prickett@mkdons.com",
    "thomas.mitchell@mkdons.com",
    "matty.mortimer@mkdons.com",
}


def render_login_header() -> None:
    """Render the branded header shown above the login form."""
    col1, col2 = st.columns([1, 6])

    with col1:
        try:
            st.image("assets/mkdons_badge.png", width=80)
        except Exception:
            pass

    with col2:
        st.markdown(
            "<h1 style='margin:0; padding:0;'>MK Dons – Coach Evaluation Framework</h1>",
            unsafe_allow_html=True,
        )

    st.markdown("---")


def enforce_email_login() -> None:
    """Simple email login gate shown at app start."""
    if st.session_state.get("is_authenticated"):
        return

    render_login_header()
    st.title("Login")
    st.info("Sign in to access the Coach Evaluation Framework.")

    email = st.text_input("Email address", placeholder="name@example.com")
    _password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button("Log in", type="primary"):
        normalized_email = email.strip().lower()

        if not normalized_email or "@" not in normalized_email:
            st.error("Please enter a valid email address.")
            st.stop()

        if normalized_email not in ALLOWED_EMAILS:
            st.error("This email address does not have access.")
            st.stop()

        st.session_state["is_authenticated"] = True
        st.session_state["authenticated_email"] = normalized_email
        st.rerun()

    st.stop()


def render_logout_button() -> None:
