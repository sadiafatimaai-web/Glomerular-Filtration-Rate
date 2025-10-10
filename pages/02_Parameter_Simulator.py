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
render_sidebar()
from physiology import HemodynamicsInput, compute_hemodynamics

st.title("Hemodynamic Parameter Manipulation")
st.caption("Adjust Starling forces and hemodynamic variables to see real-time effects on GFR, RPF, RBF, FF, Pgc, and NFP.")

# ───────────────────────────────────────────────
# Preset Scenarios
# ───────────────────────────────────────────────
st.subheader("⚡ Quick Scenarios")

preset = st.selectbox(
    "Select a predefined physiological or pathological condition:",
    [
        "Baseline (Normal)",
        "↑ Ra — Afferent Constriction",
        "↑ Re — Efferent Constriction",
        "↑ Pbs — Urinary Tract Obstruction",
        "↑ πgc — Dehydration",
        "↓ MAP — Hypotension",
        "↓ Kf — Glomerular Damage",
        "↓ πgc — Nephrotic Syndrome (Low Protein)",
    ],
    index=0,
)

# Default values
MAP, Ra, Re, Pbs, pi_gc, Kf, Hct = 100, 1.0, 1.0, 10, 25, 12.0, 45

# Apply presets
if preset == "↑ Ra — Afferent Constriction":
    Ra = 3.0
    st.info("↑Ra reduces both RBF and GFR → ↓Pgc, ↓NFP")
elif preset == "↑ Re — Efferent Constriction":
    Re = 2.5
    st.info("↑Re raises Pgc and GFR, but reduces RPF → ↑FF")
elif preset == "↑ Pbs — Urinary Tract Obstruction":
    Pbs = 25
    st.warning("↑Pbs opposes filtration → ↓NFP, ↓GFR")
elif preset == "↑ πgc — Dehydration":
    pi_gc = 35
    st.warning("↑πgc increases oncotic opposition → ↓NFP, ↓GFR")
elif preset == "↓ MAP — Hypotension":
    MAP = 65
    st.warning("↓MAP → ↓Pgc, ↓NFP, ↓GFR (risk of AKI)")
elif preset == "↓ Kf — Glomerular Damage":
    Kf = 5
    st.warning("↓Kf (e.g., glomerulonephritis) → ↓GFR even with normal pressures")
elif preset == "↓ πgc — Nephrotic Syndrome (Low Protein)":
    pi_gc = 15
    st.info("↓πgc → ↓oncotic opposition → ↑NFP, ↑GFR")
else:
    st.success("Baseline (Normal physiology) — adjust sliders to explore freely")

# ───────────────────────────────────────────────
# Parameter Controls
# ───────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    st.subheader("Hemodynamic Parameters")
    MAP = st.slider("Mean Arterial Pressure (MAP) [mmHg]", 50, 200, MAP, 1)
    Ra  = st.slider("Afferent Arteriolar Resistance (Ra) [relative units]", 0.50, 5.00, Ra, 0.05)
    Re  = st.slider("Efferent Arteriolar Resistance (Re) [relative units]", 0.50, 6.00, Re, 0.05)
    Pbs = st.slider("Bowman's Capsule Pressure (Pbs) [mmHg]", 5, 40, Pbs, 1)

with right:
    st.subheader("Additional Parameters")
    pi_gc = st.slider("Plasma Oncotic Pressure (πgc) [mmHg]", 15, 35, pi_gc, 1)
    Kf    = st.slider("Ultrafiltration Coefficient (Kf) [mL/min/mmHg]", 2.00, 20.00, Kf, 0.5)
    Hct   = st.slider("Hematocrit (%)", 20, 60, Hct, 1)

# Reset Button
if st.button("🔄 Reset to Baseline"):
    st.experimental_rerun()

# ───────────────────────────────────────────────
# Calculations
# ───────────────────────────────────────────────
inp = HemodynamicsInput(MAP=MAP, Ra=Ra, Re=Re, Pbs=Pbs, pi_gc=pi_gc, Kf=Kf, Hct=Hct)
out = compute_hemodynamics(inp)

st.markdown("### 🧮 Calculated Results")
cols = st.columns(6)
cols[0].metric("GFR", f"{out.GFR:,.1f} mL/min")
cols[1].metric("RPF", f"{out.RPF:,.1f} mL/min")
cols[2].metric("RBF", f"{out.RBF:,.1f} mL/min")
cols[3].metric("FF", f"{out.FF:,.1f}%")
cols[4].metric("Pgc", f"{out.Pgc:,.1f} mmHg")
cols[5].metric("NFP", f"{out.NFP:,.1f} mmHg")

st.divider()

# ───────────────────────────────────────────────
# Interpretation Guide
# ───────────────────────────────────────────────
st.subheader("📘 Interpretation Guide")

with st.expander("GFR Interpretation"):
    st.markdown("""
- **> 90 mL/min:** Normal kidney function  
- **60–89 mL/min:** Mild decrease (Stage 2 CKD)  
- **30–59 mL/min:** Moderate decrease (Stage 3 CKD)  
- **15–29 mL/min:** Severe decrease (Stage 4 CKD)  
- **< 15 mL/min:** Kidney failure (Stage 5 CKD)
""")

with st.expander("Filtration Fraction (FF)"):
    st.markdown("""
- **Normal:** 16–20%  
- **Increased FF:** Suggests efferent constriction (↑Re)  
- **Decreased FF:** Suggests afferent constriction (↑Ra) or ↑Pbs/↑πgc
""")

with st.expander("Key Relationships"):
    st.markdown("""
**Equations:**
- GFR = Kf × NFP  
- NFP = Pgc − Pbs − πgc  
- FF = (GFR / RPF) × 100%  
- RBF = RPF / (1 − Hct)
""")

with st.expander("Clinical Pearls"):
    st.markdown("""
- ↑Re → ↑Pgc → may maintain or ↑GFR (↑FF)  
- ↑Ra → ↓Pgc → ↓GFR & ↓RBF  
- ↑Pbs (obstruction) → ↓NFP → ↓GFR  
- ↑πgc (dehydration) → ↓NFP → ↓GFR  
- ↓Kf (glomerular damage) → ↓GFR even with normal pressures  
- ↓πgc (nephrotic syndrome) → ↑GFR
""")

st.divider()

# ───────────────────────────────────────────────
# Try This Exercise
# ───────────────────────────────────────────────
st.subheader("🧩 Try This Exercise")

st.markdown("""
**Challenge Questions:**
1. What happens to **GFR** and **FF** when you increase **efferent resistance (Re)** while keeping other parameters constant?  
2. At what **MAP** does **GFR** become critically low? What changes if you also increase **Kf**?  
3. Compare **↑Ra** vs **mild ↑Re** — how do they differently affect **GFR** and **FF**?  
4. How do **↑Pbs** (obstruction) and **↑πgc** (dehydration) separately reduce **NFP**?
""")

st.info("💡 Tip: Start with baseline, tweak one slider at a time, and observe how the metrics respond.")

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

