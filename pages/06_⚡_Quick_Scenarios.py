import streamlit as st
import pandas as pd
import plotly.express as px
from physiology import HemodynamicsInput, compute_hemodynamics

st.title("⚡ Quick Scenarios")
st.caption("Compare different physiological and pathological scenarios side-by-side.")

st.markdown("""
Use this section to **instantly simulate and visualize** how multiple renal conditions
affect **GFR**, **RPF**, and **Filtration Fraction (FF)**.
""")

# ───────────────────────────────────────────────
# Define Scenarios
# ───────────────────────────────────────────────
scenarios = {
    "Baseline (Normal)": HemodynamicsInput(MAP=100, Ra=1.0, Re=1.0, Pbs=10, pi_gc=25, Kf=12, Hct=45),
    "↑ Ra — Afferent Constriction": HemodynamicsInput(MAP=100, Ra=3.0, Re=1.0, Pbs=10, pi_gc=25, Kf=12, Hct=45),
    "↑ Re — Efferent Constriction": HemodynamicsInput(MAP=100, Ra=1.0, Re=2.5, Pbs=10, pi_gc=25, Kf=12, Hct=45),
    "↑ Pbs — Obstruction": HemodynamicsInput(MAP=100, Ra=1.0, Re=1.0, Pbs=25, pi_gc=25, Kf=12, Hct=45),
    "↑ πgc — Dehydration": HemodynamicsInput(MAP=100, Ra=1.0, Re=1.0, Pbs=10, pi_gc=35, Kf=12, Hct=45),
    "↓ MAP — Hypotension": HemodynamicsInput(MAP=65, Ra=1.0, Re=1.0, Pbs=10, pi_gc=25, Kf=12, Hct=45),
    "↓ Kf — Glomerular Damage": HemodynamicsInput(MAP=100, Ra=1.0, Re=1.0, Pbs=10, pi_gc=25, Kf=5, Hct=45),
    "↓ πgc — Nephrotic Syndrome": HemodynamicsInput(MAP=100, Ra=1.0, Re=1.0, Pbs=10, pi_gc=15, Kf=12, Hct=45),
}

# Compute Results
results = []
for name, params in scenarios.items():
    out = compute_hemodynamics(params)
    results.append({
        "Scenario": name,
        "GFR (mL/min)": out.GFR,
        "RPF (mL/min)": out.RPF,
        "RBF (mL/min)": out.RBF,
        "FF (%)": out.FF,
        "Pgc (mmHg)": out.Pgc,
        "NFP (mmHg)": out.NFP,
    })

df = pd.DataFrame(results)

# ───────────────────────────────────────────────
# Display Comparison Table
# ───────────────────────────────────────────────
st.subheader("📋 Scenario Summary")
st.dataframe(df.style.format({
    "GFR (mL/min)": "{:.1f}",
    "RPF (mL/min)": "{:.1f}",
    "RBF (mL/min)": "{:.1f}",
    "FF (%)": "{:.1f}",
    "Pgc (mmHg)": "{:.1f}",
    "NFP (mmHg)": "{:.1f}",
}), use_container_width=True)

st.divider()

# ───────────────────────────────────────────────
# Visualization
# ───────────────────────────────────────────────
st.subheader("📈 Visual Comparison")

metric_choice = st.selectbox(
    "Select metric to visualize:",
    ["GFR (mL/min)", "RPF (mL/min)", "FF (%)", "NFP (mmHg)", "Pgc (mmHg)"],
    index=0,
)

fig = px.bar(
    df,
    x="Scenario",
    y=metric_choice,
    text=metric_choice,
    color="Scenario",
    color_discrete_sequence=px.colors.qualitative.Safe,
)
fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
fig.update_layout(yaxis_title=metric_choice, showlegend=False, height=520)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ───────────────────────────────────────────────
# Clinical Insight
# ───────────────────────────────────────────────
st.subheader("💡 Interpretation Highlights")

with st.expander("Key Observations by Scenario"):
    st.markdown("""
- **↑Ra (Afferent Constriction):** ↓Pgc → ↓NFP → ↓GFR & ↓RPF  
- **↑Re (Efferent Constriction):** ↑Pgc → ↑GFR, ↓RPF → ↑FF  
- **↑Pbs (Obstruction):** ↑Pbs opposes filtration → ↓NFP → ↓GFR  
- **↑πgc (Dehydration):** ↑oncotic pressure → ↓NFP → ↓GFR  
- **↓MAP (Hypotension):** ↓driving pressure → ↓Pgc → ↓GFR  
- **↓Kf (Glomerular Damage):** ↓membrane permeability → ↓GFR  
- **↓πgc (Nephrotic Syndrome):** ↓oncotic opposition → ↑NFP → ↑GFR  
""")

st.markdown("""
✅ **Quick Summary:**
- **Efferent constriction** (↑Re) → preserves or raises GFR  
- **Afferent constriction / obstruction / hypotension** → lower GFR  
- **↓Kf** → intrinsic renal disease pattern  
- **↓πgc** → rare hyperfiltration state (↑GFR, ↑FF)
""")

st.success("Try toggling between scenarios to visualize classic Starling force interactions!")
