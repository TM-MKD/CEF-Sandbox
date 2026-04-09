import streamlit as st

ALLOWED_EMAIL_DOMAIN = "mkdons.com"
OIDC_PROVIDER_NAME = "microsoft"


REQUIRED_AUTH_CONFIG = {
    "auth": ["redirect_uri", "cookie_secret"],
    "auth.microsoft": ["client_id", "client_secret", "server_metadata_url"],
}


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


def _is_user_logged_in() -> bool:
    """Handle Streamlit versions where st.user may not expose .is_logged_in as an attribute."""
    user = st.user

    if hasattr(user, "is_logged_in"):
        return bool(user.is_logged_in)

    if hasattr(user, "get"):
        is_logged_in = user.get("is_logged_in")
        if is_logged_in is not None:
            return bool(is_logged_in)

    return bool(_extract_email())


def _missing_oidc_config() -> list[str]:
    """Return a list of missing required Streamlit auth keys."""
    missing = []

    for section, keys in REQUIRED_AUTH_CONFIG.items():
        section_value = st.secrets.get(section, {}) if hasattr(st, "secrets") else {}

        for key in keys:
            value = None

            if hasattr(section_value, "get"):
                value = section_value.get(key)
            elif isinstance(section_value, dict):
                value = section_value.get(key)

            if not value:
                missing.append(f"{section}.{key}")

    return missing


def enforce_mkdons_sso() -> None:
    """Require Microsoft SSO and restrict access to @mkdons.com users only."""

    if not hasattr(st, "login") or not hasattr(st, "logout") or not hasattr(st, "user"):
        st.error(
            "This app requires a newer Streamlit version with OIDC support "
            "(st.login / st.user / st.logout)."
        )
        st.stop()

    if not _is_user_logged_in():
        st.title("Sign in required")
        st.info("Please sign in with your MK Dons Microsoft account to access this app.")

        missing_config = _missing_oidc_config()
        if missing_config:
            st.error(
                "SSO setup is incomplete. Add the missing keys in `.streamlit/secrets.toml` "
                "and restart the app."
            )
            st.code("\n".join(missing_config), language="text")
            st.stop()

        if st.button("🔐 Sign in with Outlook / Microsoft", type="primary"):
            try:
                st.login(OIDC_PROVIDER_NAME)
            except Exception:
                st.error(
                    "Unable to start Microsoft sign-in. Please verify your Azure app "
                    "redirect URI, tenant metadata URL, and client credentials."
                )

        st.stop()

    email = _extract_email()

    if not email.endswith(f"@{ALLOWED_EMAIL_DOMAIN}"):
        st.error(
            "Access denied. You must sign in with an @mkdons.com email address "
            "to use this app."
        )
        st.write(f"Signed in as: `{email or 'Unknown account'}`")

        if st.button("Sign out"):
            try:
                st.logout()
            except Exception:
                st.warning("Unable to sign out cleanly in this session. Please refresh the app.")

        st.stop()

    st.session_state["authenticated_email"] = email
