# gfr_app.py  (top-level entry for your Streamlit multipage app)

import streamlit as st

# Page config (do this before drawing anything)
st.set_page_config(
    page_title="GFR Physiology Simulator",
    page_icon="🫘",
    layout="wide",
    menu_items={"about": "GFR Physiology Simulator • Interactive learning for first-year medical students"}
)

# ---------- HOME CONTENT (kept light; the detailed intro lives in pages/01_... ) ----------
st.markdown("""
<div style="background:linear-gradient(90deg,#1a73e8,#5b8def);padding:28px;border-radius:16px;color:white;">
  <h1 style="margin:0;">🫘 GFR Physiology Simulator</h1>
  <p style="margin:8px 0 0 0;font-size:18px;">Interactive Learning Platform for First-Year Medical Students</p>
</div>
""", unsafe_allow_html=True)

st.markdown("#### Developed by **Dr Sadia Fatima** — *October 2025*")

left, right = st.columns([2,1], gap="large")
with left:
    st.header("Welcome!")
    st.write(
        "Explore **Starling forces**, **renal autoregulation**, and **clinical cases** with interactive sliders and charts."
    )
    st.subheader("What you'll learn")
    st.markdown(
        """
        - ✅ Starling forces and their effects on GFR  
        - ✅ Renal autoregulation mechanisms  
        - ✅ Clinical applications in real patient scenarios  
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
st.subheader("Navigate")
st.write(
    "Use the left sidebar to open pages:\n"
    "- 📘 **Introduction**\n"
    "- 🧮 **Parameter Simulator**\n"
    "- 🧠 **Autoregulation**\n"
    "- ⚡ **Quick Scenarios**\n"
    "- 📝 **Cases & Worksheet**\n"
    "- 🎞️ **Videos & Slides**"
)

# Optional: your custom footer/navigation (same block you add to each page)
st.markdown("---")
footer_col1, footer_col2 = st.columns([3, 2])
with footer_col1:
    st.markdown("""
    **Navigation:**  
    [📘 Introduction](./01_%F0%9F%93%98_GFR_Introduction) | 
    [🧮 Simulator](./02_%F0%9F%A7%AE_Parameter_Simulator) | 
    [🧠 Autoregulation](./03_%F0%9F%A7%A0_Autoregulation) | 
    [⚡ Scenarios](./06_%E2%9A%A1_Quick_Scenarios) | 
    [📝 Cases](./05_%F0%9F%93%9D_Cases_and_Worksheet) | 
    [🎞️ Videos](./04_%F0%9F%8E%9E%EF%B8%8F_Videos_and_Slides)
    """)
with footer_col2:
    st.markdown("""
    <div style='text-align: right; font-size: 0.9em; color: gray;'>
    Developed by <b>Dr Sadia Fatima</b> • October 2025
    </div>
    """, unsafe_allow_html=True)
