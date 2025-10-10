st.markdown("""
<style>
footer {visibility: hidden;}
div.block-container {
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)


import streamlit as st
from utils_nav import render_sidebar

st.set_page_config(page_title="GFR Physiology Simulator", page_icon="🫘", layout="wide")
render_sidebar()


st.title("🎞️ Educational Videos and Slides")
st.caption("Visual learning resources to deepen your understanding of glomerular filtration and renal physiology.")

# ───────────────────────────────────────────────
# Introduction
# ───────────────────────────────────────────────
st.markdown("""
Here you’ll find **video tutorials** and **lecture slides** explaining the concepts behind
the **glomerular filtration rate (GFR)** and its regulation.

These materials reinforce what you’ve explored in the simulator:
- Starling forces and their impact on filtration  
- Autoregulation mechanisms  
- Clinical applications of GFR measurement  
""")

st.divider()

# ───────────────────────────────────────────────
# Section 1: Core Concept Videos
# ───────────────────────────────────────────────
st.subheader("🎬 Core Concept Videos")

st.markdown("#### 1️⃣ Glomerular Filtration and Starling Forces (5 min)")
st.video("https://www.youtube.com/watch?v=0f2e9tVEX3c")

st.markdown("#### 2️⃣ Renal Autoregulation — Myogenic & Tubuloglomerular Feedback (6 min)")
st.video("https://www.youtube.com/watch?v=zSMXo5Jm9x4")

st.markdown("#### 3️⃣ Filtration Fraction and Clinical Correlations (4 min)")
st.video("https://www.youtube.com/watch?v=Kj1p9fEkw9A")

st.info("💡 Tip: Use these videos before or after running the simulator to connect concepts to visual physiology.")

st.divider()

# ───────────────────────────────────────────────
# Section 2: Lecture Slides (Embedded)
# ───────────────────────────────────────────────
st.subheader("📑 Lecture Slides")

st.markdown("""
Below are interactive lecture slides.  
Use the arrow controls to navigate between them.  
If they don’t load, open the direct link provided.
""")

st.markdown("**🔹 GFR Physiology – Concept Overview (Google Slides)**")
st.components.v1.iframe(
    "https://docs.google.com/presentation/d/e/2PACX-1vTgL4KfP7tQdtdo8D7x8BHpYAYu3yQFxEKib7D3BYAw0I3lKz79gI5rbJBTQbnf2xM/embed?start=false&loop=false&delayms=60000",
    height=480
)
st.markdown("[Open in new tab →](https://docs.google.com/presentation/d/e/2PACX-1vTgL4KfP7tQdtdo8D7x8BHpYAYu3yQFxEKib7D3BYAw0I3lKz79gI5rbJBTQbnf2xM/pub?start=false&loop=false)")

st.markdown("**🔹 Autoregulation and Clinical Examples**")
st.components.v1.iframe(
    "https://docs.google.com/presentation/d/e/2PACX-1vRMHgqvL27ZDWV6C9yN5Aw7wA7TkRjMTvLVrA6qPq-UbOYNX46xX_MZ5vZ4z0AHew/embed?start=false&loop=false&delayms=60000",
    height=480
)
st.markdown("[Open in new tab →](https://docs.google.com/presentation/d/e/2PACX-1vRMHgqvL27ZDWV6C9yN5Aw7wA7TkRjMTvLVrA6qPq-UbOYNX46xX_MZ5vZ4z0AHew/pub?start=false&loop=false)")

st.divider()

# ───────────────────────────────────────────────
# Section 3: Quick Reference
# ───────────────────────────────────────────────
st.subheader("🧾 Quick Reference Summary")

st.markdown("""
**Normal Ranges**
| Parameter | Typical Value | Notes |
|------------|----------------|-------|
| GFR | 120–125 mL/min | ≈180 L/day |
| RPF | 650 mL/min | ≈20% of cardiac output |
| FF | 18–20 % | GFR/RPF |
| MAP | 80–180 mmHg | Autoregulation plateau |
| πgc | 25 mmHg | Glomerular oncotic pressure |

**Key Relationships**
- `GFR = Kf × (Pgc − Pbs − πgc)`
- `RPF = MAP / (Ra + Re)`
- `FF = (GFR / RPF) × 100%`
""")

st.divider()

# ───────────────────────────────────────────────
# Try This Exercise
# ───────────────────────────────────────────────
st.subheader("🎯 Try This Exercise")

st.markdown("""
1. Watch *Glomerular Filtration and Starling Forces*.  
   → Identify which variables most strongly influence **Pgc**.  
2. From the *Autoregulation video*, note how the **macula densa** affects **afferent tone**.  
3. Open the slides and explain why **efferent constriction** increases **FF** but may decrease **RPF**.  
4. Summarize: How does **hypertension** affect the autoregulatory plateau?  
""")

st.info("💡 Tip: Use the **Parameter Simulator** tab to test what you just learned in real-time.")

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
