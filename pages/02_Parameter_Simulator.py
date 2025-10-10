# pages/02_Parameter_Simulator.py
import streamlit as st
import numpy as np
from utils_nav import render_sidebar
from physiology import nfp, gfr, rpf_from_map, rbf_from_rpf, filtration_fraction

st.set_page_config(page_title="GFR — Parameter Simulator", layout="wide")
render_sidebar()

st.title("🧮 Hemodynamic Parameter Manipulation")

st.markdown("Adjust parameters and see **GFR**, **RPF**, **RBF**, **FF**, **Pgc**, and **NFP** update live.")

# Sliders
c1, c2 = st.columns(2)
with c1:
    MAP = st.slider("Mean Arterial Pressure (MAP) [mmHg]", 50, 200, 100)
    Ra  = st.slider("Afferent Arteriolar Resistance (Ra) [rel units]", 0.50, 5.00, 1.00, 0.05)
    Re  = st.slider("Efferent Arteriolar Resistance (Re) [rel units]", 0.50, 6.00, 2.00, 0.05)
    Pbs = st.slider("Bowman's Capsule Pressure (Pbs) [mmHg]", 5, 40, 10)
with c2:
    pi_gc = st.slider("Plasma Oncotic Pressure (πgc) [mmHg]", 15, 35, 25)
    Kf    = st.slider("Ultrafiltration Coefficient (Kf) [mL/min/mmHg]", 2.0, 20.0, 12.0, 0.1)
    Hct   = st.slider("Hematocrit (%)", 20, 60, 45)

# Simple Pgc model proportional to MAP & resistance ratio
Pgc = np.clip(0.99 * MAP * (Re / (Ra + Re)) + 10, 40, 110)

NFP = nfp(Pgc, Pbs, pi_gc, 0.0)
GFR = gfr(Kf, NFP)
RPF = rpf_from_map(MAP, Ra, Re)
RBF = rbf_from_rpf(RPF, Hct)
FF  = filtration_fraction(GFR, RPF)

st.divider()
st.subheader("Calculated Results")
c3, c4, c5 = st.columns(3)
with c3:
    st.metric("GFR", f"{GFR:,.1f} mL/min")
    st.metric("RPF", f"{RPF:,.1f} mL/min")
with c4:
    st.metric("RBF", f"{RBF:,.1f} mL/min")
    st.metric("FF",  f"{FF:,.1f}%")
with c5:
    st.metric("Pgc", f"{Pgc:,.1f} mmHg")
    st.metric("NFP", f"{NFP:,.1f} mmHg")

st.divider()
st.subheader("Interpretation Guide")
st.markdown("""
**GFR:**
- >90 mL/min: normal  
- 60–89: mild ↓  
- 30–59: moderate ↓  
- 15–29: severe ↓  
- <15: kidney failure  

**Key relationships**  
- `GFR = Kf × NFP`  
- `NFP = Pgc - Pbs - πgc`  
- `FF = GFR / RPF × 100%`  
- `RBF = RPF / (1 - Hct)`
""")

