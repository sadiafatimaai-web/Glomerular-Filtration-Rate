st.markdown("""
<style>
footer {visibility: hidden;}
div.block-container {
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)


import streamlit as st

st.set_page_config(page_title="GFR Physiology Simulator", page_icon="🫘", layout="wide")

st.markdown("""
<div style="background:linear-gradient(90deg,#1a73e8,#5b8def);padding:28px;border-radius:16px;color:white;">
<h1>🫘 GFR Physiology Simulator</h1>
<p>Interactive Learning Platform for Medical Students</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([2,1])
with left:
    st.header("Welcome!")
    st.markdown("""
- Understand **Starling Forces**  
- Explore **Autoregulation**  
- Simulate **Clinical Cases**  
- Predict **GFR changes** with parameter tweaks  
""")
with right:
    st.header("Quick Stats")
    c1,c2 = st.columns(2)
    c1.metric("Clinical Cases", 4)
    c1.metric("Parameters", 6)
    c2.metric("Scenarios", 7)
    c2.metric("Learning", "∞")

st.divider()
st.markdown("""
### Navigation
Use the sidebar to move between:
- 📘 Introduction  
- 🧮 Parameter Simulator  
- 🧠 Autoregulation  
- 🎞️ Videos and Slides  
- 📝 Cases & Worksheet
""")
# ───────────────────────────────────────────────
# FOOTER / NAVIGATION BAR
# ───────────────────────────────────────────────
st.markdown("---")

footer_col1, footer_col2 = st.columns([3, 2])

with footer_col1:
    st.markdown("""
    **Navigation:**  
    [🏠 Home](./01_%F0%9F%93%98_GFR_Introduction) | 
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
    References: <i>Guyton & Hall</i>, <i>Ganong</i>, <i>Sherwood</i>
    </div>
    """, unsafe_allow_html=True)
