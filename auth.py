import streamlit as st


def _load_allowed_emails() -> set[str]:
    """Load an optional email allowlist from Streamlit secrets."""
    configured = st.secrets.get("allowed_emails", []) if hasattr(st, "secrets") else []

    if isinstance(configured, str):
        configured = [configured]

    allowed = {
        email.strip().lower()
        for email in configured
        if isinstance(email, str) and email.strip()
    }

    return allowed


def enforce_email_login() -> None:
    """Simple email login gate shown at app start."""
    if st.session_state.get("is_authenticated"):
        return

    st.title("Login")
    st.info("Sign in to access the Coach Evaluation Framework.")

    email = st.text_input("Email address", placeholder="name@example.com")

    allowed_emails = _load_allowed_emails()

    if st.button("Log in", type="primary"):
        normalized_email = email.strip().lower()

        if not normalized_email or "@" not in normalized_email:
            st.error("Please enter a valid email address.")
            st.stop()

        if allowed_emails and normalized_email not in allowed_emails:
            st.error("This email address does not have access yet.")
            st.stop()

        st.session_state["is_authenticated"] = True
        st.session_state["authenticated_email"] = normalized_email
        st.rerun()

    if not allowed_emails:
        st.caption(
            "Allowlist is not configured yet. Any valid email can log in for now. "
            "Add `allowed_emails` in `.streamlit/secrets.toml` when ready."
        )

    st.stop()


def render_logout_button() -> None:
    """Small utility to let authenticated users sign out."""
    if not st.session_state.get("is_authenticated"):
        return

    if st.button("🔓 Log out"):
        st.session_state["is_authenticated"] = False
        st.session_state.pop("authenticated_email", None)
        st.rerun()
