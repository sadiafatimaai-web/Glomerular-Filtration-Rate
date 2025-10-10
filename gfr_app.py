# gfr_app.py
import streamlit as st
from utils_nav import render_sidebar

st.set_page_config(
    page_title="GFR Physiology Simulator",
    page_icon="🫘",
    layout="wide",
)

# Left sidebar navigation
render_sidebar()

# Header band
st.markdown("""
<div style="background:linear-gradient(90deg,#1a73e8,#5b8def);padding:28px;border-radius:16px;color:white;">
  <h1 style="margin:0;">🫘 GFR Physiology Simulator</h1>
  <p style="margin:8px 0 0 0;font-size:18px;">Interactive learning platform for medical students</p>
</div>
""", unsafe_allow_html=True)

st.markdown("#### Developed by **Dr Sadia Fatima**")

left, right = st.columns([2,1], gap="large")
with left:
    st.header("Welcome")
    st.write(
        "Explore **Starling forces**, **renal autoregulation**, and **clinical cases** with interactive sliders and charts."
    )
    st.subheader("What you'll learn")
    st.markdown(
        """
        - ✅ Starling forces and their effects on GFR  
        - ✅ Renal autoregulation mechanisms  
        - ✅ Clinical scenarios & worksheets  
        - ✅ Hemodynamic parameter interactions  
        """
    )
with right:
    st.header("Quick Stats")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Clinical Cases", 4)
        st.metric("Parameters", 6)
    with c2:
        st.metric("Scenarios", 7)
        st.metric("Learning", "∞")

st.divider()

st.info("Use the **Navigation** menu on the left to open each page.")
