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
    st.page_link(
        "pages/1_Individual_Coach_View.py",
        label="⚽ Individual Coach View",
        icon="📊"
    )

with col2:
    st.page_link(
        "pages/2_Block_Average_View.py",
        label="👥 Block Average View",
        icon="📈"
    )

st.markdown("---")
st.write("Upload your Excel file within the selected page.")
