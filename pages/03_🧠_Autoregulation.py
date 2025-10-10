# pages/03_Autoregulation.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils_nav import render_sidebar
from physiology import autoregulated_values, rpf_from_map

st.set_page_config(page_title="GFR — Autoregulation", layout="wide")
render_sidebar()

st.title("🧠 Renal Autoregulation")

st.markdown("Renal autoregulation maintains relatively stable **GFR** and **RPF** between **~80–180 mmHg** MAP.")

# Controls
colA, colB = st.columns(2)
with colA:
    use_auto = st.toggle("Autoregulation", value=True)
    status = "🟢 ACTIVE" if use_auto else "🔴 INACTIVE"
    st.write("Status:", status)
with colB:
    map_min, map_max = st.slider("MAP range for analysis", 40, 220, (40, 220))

MAPs = np.linspace(map_min, map_max, 60)
GFRs, RPFs = [], []

for m in MAPs:
    if use_auto:
        g, r = autoregulated_values(m)
    else:
        # Without autoregulation: simple proportional response
        r = rpf_from_map(m, 1.0, 2.0)
        g = 0.18 * r  # tie GFR loosely to RPF
    GFRs.append(g); RPFs.append(r)

# Charts
c1, c2 = st.columns(2)
with c1:
    fig = go.Figure()
    fig.add_scatter(x=MAPs, y=GFRs, mode="lines", name="GFR")
    fig.add_hline(y=120, line=dict(dash="dash"), annotation_text="Normal GFR ≈ 120")
    fig.update_layout(title="GFR vs MAP", xaxis_title="MAP (mmHg)", yaxis_title="GFR (mL/min)", height=360)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig2 = go.Figure()
    fig2.add_scatter(x=MAPs, y=RPFs, mode="lines", name="RPF")
    fig2.add_hline(y=650, line=dict(dash="dash"), annotation_text="Normal RPF ≈ 650")
    fig2.update_layout(title="RPF vs MAP", xaxis_title="MAP (mmHg)", yaxis_title="RPF (mL/min)", height=360)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("Interactive Point Analysis")
MAP_point = st.slider("Select MAP for analysis", 40, 220, 100)

if use_auto:
    g_auto, r_auto = autoregulated_values(MAP_point)
else:
    r_auto = rpf_from_map(MAP_point, 1.0, 2.0)
    g_auto = 0.18 * r_auto

# Compare with “no autoregulation”
r_no = rpf_from_map(MAP_point, 1.0, 2.0)
g_no = 0.18 * r_no

colx, coly = st.columns(2)
with colx:
    st.write("**With Autoregulation**")
    st.metric("GFR", f"{g_auto:,.1f} mL/min")
    st.metric("RPF", f"{r_auto:,.1f} mL/min")
with coly:
    st.write("**Without Autoregulation**")
    st.metric("GFR", f"{g_no:,.1f} mL/min")
    st.metric("RPF", f"{r_no:,.1f} mL/min")

st.info(
    "✅ Within ~80–180 mmHg, **GFR** and **RPF** remain near-normal when autoregulation is active. "
    "Outside that range, stability is lost."
)


