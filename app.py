import streamlit as st

st.set_page_config(
    page_title="MK Dons – CEF Sandbox",
    layout="wide"
)

st.title("MK Dons – CEF Sandbox")
st.markdown("---")

st.markdown("## Welcome")
st.write("Choose a page below to begin.")

col1, col2 = st.columns(2)

with col1:
    if st.button("⚽ Individual Coach View", use_container_width=True):
        st.switch_page("pages/1_Individual_Coach_View.py")

with col2:
    if st.button("👥 Block Average View", use_container_width=True):
        st.switch_page("pages/2_Block_Average_View.py")

st.markdown("---")
st.write("Upload your Excel file within the selected page.")
