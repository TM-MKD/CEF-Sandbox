import streamlit as st
 
 st.set_page_config(
     page_title="Home",       # This controls the sidebar name for the page
+    layout="wide",
+    initial_sidebar_state="collapsed"
+)
+
+st.markdown(
+    """
+    <style>
+    [data-testid="stSidebar"],
+    [data-testid="collapsedControl"] {
+        display: none;
+    }
+    </style>
+    """,
+    unsafe_allow_html=True
 )
 
 # ===================== HEADER =====================
 col1, col2 = st.columns([1, 6])
 
 with col1:
     try:
         st.image("assets/mkdons_badge.png", width=80)
     except:
         pass
 
 with col2:
     st.markdown(
         "<h1 style='margin:0; padding:0;'>MK Dons – Coach Evaluation Framework</h1>", 
         unsafe_allow_html=True
     )
 
 st.markdown("---")
 st.markdown("## Welcome")
 st.write("Choose a page below to begin.")
 
 col1, col2 = st.columns(2)
 with col1:
     if st.button("⚽ Individual Coach View", use_container_width=True):
         st.switch_page("pages/1_Individual_Coach_View.py")
