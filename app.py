import streamlit as st

st.set_page_config(
    page_title="MK Dons – CEF Sandbox",
    layout="wide"
)

st.title("MK Dons – CEF Sandbox")
st.markdown("---")

st.markdown("""
Welcome to the **Coach Evaluation Framework Sandbox**.

Use the navigation menu on the left to access:

- **Individual Coach View** → Review one coach’s scores
- **Block Average View** → Review average scores across all coaches in a block

Upload your evaluation data within each page to begin.
""")
