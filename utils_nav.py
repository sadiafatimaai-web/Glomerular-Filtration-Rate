# utils_nav.py
import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        # Works on Streamlit Cloud (>=1.26)
        st.page_link("gfr_app.py", label="🏠 Home")
        st.page_link("pages/01_📘_GFR_Introduction.py", label="📘 Introduction")
        st.page_link("pages/02_🧮_Parameter_Simulator.py", label="🧮 Parameter Simulator")
        st.page_link("pages/03_🧠_Autoregulation.py", label="🧠 Autoregulation")
        st.page_link("pages/06_⚡_Quick_Scenarios.py", label="⚡ Quick Scenarios")
        st.page_link("pages/05_📝_Cases_and_Worksheet.py", label="📝 Cases & Worksheet")
        st.page_link("pages/04_🎞️_Videos_and_Slides.py", label="🎞️ Videos & Slides")

        st.markdown("---")
        st.caption("Developed by **Dr Sadia Fatima** • October 2025")

