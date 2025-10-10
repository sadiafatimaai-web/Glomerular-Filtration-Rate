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
import numpy as np
import plotly.graph_objects as go
from physiology import HemodynamicsInput, compute_hemodynamics

st.title("🧠 Renal Autoregulation Mechanisms")
st.caption("Understand how GFR and RPF remain stable over a wide range of arterial pressures.")

# ───────────────────────────────────────────────
# Intro
# ───────────────────────────────────────────────
st.markdown("""
**Renal autoregulation** maintains relatively constant **GFR** and **RPF** despite wide
fluctuations in **mean arterial pressure (MAP)**.

Toggle autoregulation **ON/OFF** to visualize how the kidney protects filtration.
""")

# Reset mechanism
if st.button("🔄 Reset to Baseline"):
    st.experimental_rerun()

# Toggle
auto_state = st.radio("Autoregulation Status", ["🟢 ON (Active)", "🔴 OFF (Inactive)"], index=0)

# MAP range
MAP_min, MAP_max = st.slider("MAP Range for Analysis [mmHg]", 40, 220, (40, 220), 5)
MAP_values = np.arange(MAP_min, MAP_max + 1, 5)

# ───────────────────────────────────────────────
# Base Parameters
# ───────────────────────────────────────────────
base = HemodynamicsInput(MAP=100, Ra=1.0, Re=1.0, Pbs=10, pi_gc=25, Kf=12.0, Hct=45)

# ───────────────────────────────────────────────
# Compute both conditions
# ───────────────────────────────────────────────
GFR_auto, GFR_noauto, RPF_auto, RPF_noauto = [], [], [], []

for MAP in MAP_values:
    # With autoregulation: Ra/Re adjust dynamically
    if auto_state == "🟢 ON (Active)":
        if MAP < 80:
            Ra, Re = 1.5, 1.0
        elif MAP > 180:
            Ra, Re = 0.7, 1.2
        else:
            Ra, Re = 1.0, 1.0
    else:
        Ra, Re = 1.0, 1.0

    inp = HemodynamicsInput(MAP=MAP, Ra=Ra, Re=Re, Pbs=10, pi_gc=25, Kf=12, Hct=45)
    out = compute_hemodynamics(inp)

    GFR_auto.append(out.GFR if auto_state == "🟢 ON (Active)" else np.nan)
    GFR_noauto.append(out.GFR)
    RPF_auto.append(out.RPF if auto_state == "🟢 ON (Active)" else np.nan)
    RPF_noauto.append(out.RPF)

# ───────────────────────────────────────────────
# GFR Plot (with shaded autoregulation range)
# ───────────────────────────────────────────────
st.markdown("### 📊 GFR vs Mean Arterial Pressure")

fig_gfr = go.Figure()

# Shaded autoregulation zone
fig_gfr.add_vrect(
    x0=80, x1=180,
    fillcolor="rgba(0,200,0,0.1)",
    layer="below", line_width=0,
    annotation_text="Autoregulation Range (80–180 mmHg)", annotation_position="top left"
)

# Lines
fig_gfr.add_trace(go.Scatter(
    x=MAP_values, y=GFR_noauto,
    mode="lines", name="Without Autoregulation",
    line=dict(color="red", dash="dash")
))
if auto_state == "🟢 ON (Active)":
    fig_gfr.add_trace(go.Scatter(
        x=MAP_values, y=GFR_auto,
        mode="lines", name="With Autoregulation",
        line=dict(color="green", width=3)
    ))

fig_gfr.update_layout(
    xaxis_title="MAP (mmHg)",
    yaxis_title="GFR (mL/min)",
    height=420, showlegend=True
)
st.plotly_chart(fig_gfr, use_container_width=True)

# ───────────────────────────────────────────────
# RPF Plot (with shaded zone)
# ───────────────────────────────────────────────
st.markdown("### 📈 RPF vs Mean Arterial Pressure")

fig_rpf = go.Figure()

fig_rpf.add_vrect(
    x0=80, x1=180,
    fillcolor="rgba(0,200,0,0.1)",
    layer="below", line_width=0,
    annotation_text="Autoregulation Range (80–180 mmHg)", annotation_position="top left"
)

fig_rpf.add_trace(go.Scatter(
    x=MAP_values, y=RPF_noauto,
    mode="lines", name="Without Autoregulation",
    line=dict(color="orange", dash="dot")
))
if auto_state == "🟢 ON (Active)":
    fig_rpf.add_trace(go.Scatter(
        x=MAP_values, y=RPF_auto,
        mode="lines", name="With Autoregulation",
        line=dict(color="blue", width=3)
    ))

fig_rpf.update_layout(
    xaxis_title="MAP (mmHg)",
    yaxis_title="RPF (mL/min)",
    height=420, showlegend=True
)
st.plotly_chart(fig_rpf, use_container_width=True)

# ───────────────────────────────────────────────
# Interactive Analysis
# ───────────────────────────────────────────────
st.divider()
st.markdown("### 🎯 Interactive Point Analysis")

selected_MAP = st.slider("Select MAP for Analysis [mmHg]", 40, 220, 100, 1)

def analyze(map_value, auto):
    if auto:
        if map_value < 80:
            Ra, Re = 1.5, 1.0
        elif map_value > 180:
            Ra, Re = 0.7, 1.2
        else:
            Ra, Re = 1.0, 1.0
    else:
        Ra, Re = 1.0, 1.0
    inp = HemodynamicsInput(MAP=map_value, Ra=Ra, Re=Re, Pbs=10, pi_gc=25, Kf=12, Hct=45)
    return compute_hemodynamics(inp)

auto_out = analyze(selected_MAP, auto=True)
noauto_out = analyze(selected_MAP, auto=False)

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### With Autoregulation:")
    st.metric("GFR", f"{auto_out.GFR:.1f} mL/min")
    st.metric("RPF", f"{auto_out.RPF:.1f} mL/min")
with col2:
    st.markdown("#### Without Autoregulation:")
    st.metric("GFR", f"{noauto_out.GFR:.1f} mL/min")
    st.metric("RPF", f"{noauto_out.RPF:.1f} mL/min")

diff_GFR = auto_out.GFR - noauto_out.GFR
diff_RPF = auto_out.RPF - noauto_out.RPF

st.markdown(f"**Analysis at MAP = {selected_MAP} mmHg:**")
st.write(f"• GFR Difference: {diff_GFR:.1f} mL/min")
st.write(f"• RPF Difference: {diff_RPF:.1f} mL/min")

# Interpretation logic
if 80 <= selected_MAP <= 180:
    st.success("✅ Within autoregulation range — GFR and RPF are well maintained.")
elif selected_MAP < 80:
    st.warning("⚠️ Below autoregulation threshold — both GFR and RPF begin to fall sharply.")
else:
    st.warning("⚠️ Above autoregulation range — hyperfiltration risk (↑Pgc, potential glomerular injury).")

# ───────────────────────────────────────────────
# Educational Notes
# ───────────────────────────────────────────────
st.divider()
st.subheader("🧩 Autoregulation Mechanisms")

st.markdown("""
- **Myogenic Response:** Afferent arteriole constricts when stretched by ↑ pressure  
- **Tubuloglomerular Feedback:** Macula densa senses ↑ NaCl → afferent constriction  
- **Effective Range:** ~80–180 mmHg MAP (green shaded zone)
""")

# ───────────────────────────────────────────────
# Try This Exercise
# ───────────────────────────────────────────────
st.divider()
st.subheader("🧠 Try This Exercise")

st.markdown("""
**Challenge Questions:**
1. At what **MAP** does **GFR** start dropping sharply when autoregulation is OFF?  
2. How do the **GFR** and **RPF** curves differ in their plateau zones?  
3. What happens if **autoregulation fails** (e.g., in AKI or sepsis)?  
4. How do **myogenic** and **tubuloglomerular** mechanisms complement each other?
""")

st.info("💡 Tip: Set MAP range 40–220 mmHg, toggle autoregulation ON/OFF, and observe how stability changes.")

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

