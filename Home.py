import streamlit as st

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="MK Dons – CEF Home Page",
    layout="wide"
)

# ===================== HEADER =====================
col1, col2 = st.columns([1, 6])

with col1:
    try:
        st.image("assets/mkdons_badge.png", width=80)  # Badge image
    except:
        pass

with col2:
    st.markdown(
        """
        <h1 style='margin:0; padding:0;'>MK Dons – CEF Home Page</h1>
        """, unsafe_allow_html=True
    )

st.markdown("---")

# ===================== WELCOME MESSAGE =====================
st.markdown("## Welcome")
st.write("Choose a page below to begin.")

# ===================== NAVIGATION BUTTONS =====================
col1, col2 = st.columns(2)

with col1:
    if st.button("⚽ Individual Coach View", use_container_width=True):
        st.switch_page("pages/1_Individual_Coach_View.py")

with col2:
    if st.button("👥 Block Average View", use_container_width=True):
        st.switch_page("pages/2_Block_Average_View.py")

st.markdown("---")
st.write("Upload your Excel file within the selected page.")
