import streamlit as st

ALLOWED_EMAIL_DOMAIN = "mkdons.com"
OIDC_PROVIDER_NAME = "microsoft"


def _extract_email() -> str:
    """Safely read the authenticated user's email from Streamlit OIDC profile."""
    user = st.user

    for key in ("email", "upn", "preferred_username"):
        value = None

        if hasattr(user, "get"):
            value = user.get(key)

        if not value:
            value = getattr(user, key, None)

        if isinstance(value, str) and value.strip():
            return value.strip().lower()

    return ""


def enforce_mkdons_sso() -> None:
    """Require Microsoft SSO and restrict access to @mkdons.com users only."""

    if not hasattr(st, "login") or not hasattr(st, "logout") or not hasattr(st, "user"):
        st.error(
            "This app requires a newer Streamlit version with OIDC support "
            "(st.login / st.user / st.logout)."
        )
        st.stop()

    if not st.user.is_logged_in:
        st.title("Sign in required")
        st.info("Please sign in with your MK Dons Microsoft account to access this app.")

        if st.button("🔐 Sign in with Outlook / Microsoft", type="primary"):
            st.login(OIDC_PROVIDER_NAME)

        st.stop()

    email = _extract_email()

    if not email.endswith(f"@{ALLOWED_EMAIL_DOMAIN}"):
        st.error(
            "Access denied. You must sign in with an @mkdons.com email address "
            "to use this app."
        )
        st.write(f"Signed in as: `{email or 'Unknown account'}`")

        if st.button("Sign out"):
            st.logout()

        st.stop()

    st.session_state["authenticated_email"] = email
