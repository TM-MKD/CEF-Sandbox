import streamlit as st

st.set_page_config(
    page_title="MK Dons – CEF Sandbox",
    layout="wide"
)

st.title("MK Dons – CEF Sandbox")
st.markdown("---")

st.subheader("Welcome")
st.write("Select the dashboard you would like to open.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚽ Individual Coach")
    if st.button("Open Dashboard", key="coach", use_container_width=True):
        st.switch_page("pages/1_Individual_Coach_View.py")

with col2:
    st.markdown("### 👥 Block Average")
    if st.button("Open Dashboard", key="block", use_container_width=True):
        st.switch_page("pages/2_Block_Average_View.py")
