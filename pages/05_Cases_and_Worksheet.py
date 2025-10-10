from utils_nav import render_sidebar
render_sidebar()

st.markdown("""
<style>
footer {visibility: hidden;}
div.block-container {
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)


import streamlit as st
import pandas as pd
from physiology import HemodynamicsInput, compute_hemodynamics

st.title("📝 Clinical Cases and Worksheet")
st.caption("Explore classic physiological and pathological cases by simulating changes in renal hemodynamics.")

# ───────────────────────────────────────────────
# Introduction
# ───────────────────────────────────────────────
st.markdown("""
This section lets you **apply your understanding** of GFR regulation to common **clinical scenarios**.
Each case simulates realistic hemodynamic conditions — adjust and analyze how **GFR**, **RPF**, and **FF** respond.

🧠 **Goal:** Predict the direction of change (↑ / ↓ / ↔) before running the case — then verify with the simulation!
""")

# ───────────────────────────────────────────────
# Case Selector
# ───────────────────────────────────────────────
st.subheader("⚡ Select a Case")

case = st.selectbox(
    "Choose a scenario:",
    [
        "Baseline (Normal Physiology)",
        "Acute Hemorrhage (Hypotension)",
        "Dehydration (↑πgc, ↓MAP)",
        "Urinary Tract Obstruction (↑Pbs)",
        "Nephrotic Syndrome (↓πgc)",
        "Renal Artery Stenosis (↑Ra)",
        "Efferent Arteriolar Constriction (↑Re)",
        "Glomerulonephritis (↓Kf)"
    ],
)

# Baseline values
params = HemodynamicsInput(MAP=100, Ra=1.0, Re=1.0, Pbs=10, pi_gc=25, Kf=12, Hct=45)
case_desc = ""

# Modify parameters per case
if case == "Acute Hemorrhage (Hypotension)":
    params.MAP = 65
    params.Ra = 1.4
    params.Re = 1.6
    params.pi_gc = 28
    params.Pbs = 12
    case_desc = "Severe blood loss → ↓MAP, reflex ↑Ra and ↑Re → ↓RBF, ↓GFR, ↑FF"

elif case == "Dehydration (↑πgc, ↓MAP)":
    params.MAP = 85
    params.pi_gc = 32
    params.Ra = 1.2
    params.Re = 1.5
    case_desc = "Fluid loss → ↓MAP, ↑πgc (due to hemoconcentration) → ↓GFR, ↓RPF, ↑FF"

elif case == "Urinary Tract Obstruction (↑Pbs)":
    params.Pbs = 30
    case_desc = "Obstruction ↑Pbs opposes filtration → ↓NFP → ↓GFR"

elif case == "Nephrotic Syndrome (↓πgc)":
    params.pi_gc = 15
    case_desc = "Low plasma protein → ↓πgc → ↓oncotic opposition → ↑NFP → ↑GFR"

elif case == "Renal Artery Stenosis (↑Ra)":
    params.Ra = 3.0
    case_desc = "↑Ra → ↓Pgc → ↓GFR & ↓RPF → ↓FF"

elif case == "Efferent Arteriolar Constriction (↑Re)":
    params.Re = 2.5
    case_desc = "↑Re → ↑Pgc → ↑GFR, ↓RPF → ↑FF"

elif case == "Glomerulonephritis (↓Kf)":
    params.Kf = 5
    case_desc = "Damage to filtration barrier → ↓Kf → ↓GFR (even if pressures normal)"

else:
    case_desc = "Normal renal physiology for comparison."

# Compute
result = compute_hemodynamics(params)

# ───────────────────────────────────────────────
# Display Results
# ───────────────────────────────────────────────
st.markdown("### 📊 Case Results")

cols = st.columns(6)
cols[0].metric("MAP", f"{params.MAP} mmHg")
cols[1].metric("GFR", f"{result.GFR:.1f} mL/min")
cols[2].metric("RPF", f"{result.RPF:.1f} mL/min")
cols[3].metric("RBF", f"{result.RBF:.1f} mL/min")
cols[4].metric("FF", f"{result.FF:.1f}%")
cols[5].metric("NFP", f"{result.NFP:.1f} mmHg")

st.info(f"🩺 **Case Summary:** {case_desc}")

# ───────────────────────────────────────────────
# Interpretation Table
# ───────────────────────────────────────────────
st.divider()
st.subheader("📘 Physiological Comparison Table")

data = {
    "Scenario": [
        "Baseline",
        "Hemorrhage",
        "Dehydration",
        "Obstruction",
        "Nephrotic Syndrome",
        "Renal Artery Stenosis",
        "Efferent Constriction",
        "Glomerulonephritis"
    ],
    "MAP": [100, 65, 85, 100, 100, 100, 100, 100],
    "GFR": ["Normal", "↓", "↓", "↓↓", "↑", "↓", "↑", "↓↓"],
    "RPF": ["Normal", "↓↓", "↓", "↓", "↔", "↓↓", "↓", "↔"],
    "FF":  ["~20%", "↑", "↑", "↓↓", "↑", "↑", "↑↑", "↓"],
    "Key Mechanism": [
        "Normal pressures & Kf",
        "↓MAP, ↑Ra/Re → ↓Pgc",
        "↑πgc opposes filtration",
        "↑Pbs opposes filtration",
        "↓πgc reduces oncotic opposition",
        "↑Ra reduces inflow pressure",
        "↑Re maintains Pgc despite ↓RPF",
        "↓Kf reduces filtration surface area"
    ]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# ───────────────────────────────────────────────
# Worksheet Section
# ───────────────────────────────────────────────
st.divider()
st.subheader("✏️ Worksheet — Predict, Then Simulate")

st.markdown("""
Use the space below to note your predictions before running each case.

| Parameter | Baseline | Case Prediction (↑ / ↓ / ↔) | Actual Result | Notes |
|------------|-----------|------------------------------|----------------|-------|
| GFR | 120 | | | |
| RPF | 650 | | | |
| FF  | 20% | | | |
| Pgc | 55 | | | |
| NFP | 10 | | | |

You can copy this table into your notes or export it as part of your worksheet.
""")

st.divider()

# ───────────────────────────────────────────────
# Exercises
# ───────────────────────────────────────────────
st.subheader("🎯 Try This Exercise")

st.markdown("""
1. In **Acute Hemorrhage**, which mechanism initially maintains GFR despite ↓MAP?  
2. How does **Efferent constriction** increase FF even when RPF falls?  
3. Why does **Nephrotic Syndrome** cause a transient ↑GFR that may later decline?  
4. Which variable decreases GFR the most: ↑Pbs, ↓MAP, or ↓Kf?  
5. Combine two pathologies (e.g., Dehydration + Obstruction) — what happens to NFP?  
""")

st.info("💡 Tip: Switch between cases and note the pattern of change in GFR, RPF, and FF — it’s a great way to master renal physiology.")

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
