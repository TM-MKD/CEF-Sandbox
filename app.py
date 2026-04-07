import streamlit as st

st.set_page_config(
    page_title="MK Dons – CEF Sandbox",
    layout="wide"
)

st.title("MK Dons – CEF Sandbox")
st.markdown("---")

st.markdown("""
### Welcome

Use the **sidebar on the left** to navigate between pages.

Available pages:

- **Individual Coach View**
- **Block Average View**

Upload your Excel file within the selected page.
""")

st.sidebar.success("Select a page above.")
