# pages/02_📊_Parameter_Simulator.py
import streamlit as st

try:
    from physiology import compute_outputs as _physio_compute  # optional
    HAVE_PHYSIO = True
except Exception:
    HAVE_PHYSIO = False

from utils_nav import render_sidebar
st.set_page_config(page_title="GFR — Parameter Simulator", layout="wide")
render_sidebar()

st.title("📊 Parameter Simulator")
st.caption("Manipulate Starling forces and hemodynamic parameters to see real-time effects on GFR, RPF, FF, Pgc, NFP and RBF.")

# ---------------- Baseline (calibrated) ----------------
BASELINE = {
    "MAP": 100.0,  # mmHg
    "Ra": 1.0,     # relative
    "Re": 2.0,     # relative
    "Pbs": 10.0,   # mmHg
    "Kf": 6.0,     # mL/min/mmHg
    "pi_gc": 25.0, # mmHg
    "Hct": 45.0,   # %
}

# set defaults in session_state once
for k, v in BASELINE.items():
    st.session_state.setdefault(k, v)

# Unified rerun that works on old/new Streamlit
def _rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# ---------------- Calibrated fallback (same as Quick Scenarios) ----------------
def _fallback_compute(p: dict) -> dict:
    MAP, Ra, Re = float(p["MAP"]), float(p["Ra"]), float(p["Re"])
    Pbs, Kf, pi_gc, Hct = float(p["Pbs"]), float(p["Kf"]), float(p["pi_gc"]), float(p["Hct"])

    eff_ratio = Re / max(1e-6, (Ra + Re))
    Pgc = 48.0 + 12.0 * eff_ratio + 0.12 * (MAP - 100.0)
    Pgc = min(max(Pgc, 40.0), 80.0)

    denom = max(0.1, Ra + 1.5 * Re)
    RPF = (MAP / denom) * 26.0  # ≈650 mL/min at baseline

    NFP = Pgc - Pbs - pi_gc
    GFR = max(0.0, Kf * NFP)

    RBF = RPF / max(1e-6, (1.0 - Hct / 100.0))
    FF = (GFR / RPF) * 100.0 if RPF > 0 else 0.0
    return {"GFR": GFR, "RPF": RPF, "RBF": RBF, "FF": FF, "Pgc": Pgc, "NFP": NFP}

def compute_outputs(p: dict) -> dict:
    return _physio_compute(p) if HAVE_PHYSIO else _fallback_compute(p)

# ---------------- Controls ----------------
st.markdown("### Hemodynamic Parameter Manipulation")

c1, c2, c3 = st.columns(3)
st.session_state["MAP"] = c1.slider("Mean Arterial Pressure (MAP) [mmHg]", 40.0, 220.0, float(st.session_state["MAP"]), 1.0)
st.session_state["Ra"]  = c2.slider("Afferent Arteriolar Resistance (Ra) [relative units]", 0.5, 5.0, float(st.session_state["Ra"]), 0.1)
st.session_state["Re"]  = c3.slider("Efferent Arteriolar Resistance (Re) [relative units]", 0.5, 6.0, float(st.session_state["Re"]), 0.1)

c4, c5, c6 = st.columns(3)
st.session_state["Pbs"]   = c4.slider("Bowman's Capsule Pressure (Pbs) [mmHg]", 5.0, 40.0, float(st.session_state["Pbs"]), 1.0)
st.session_state["Kf"]    = c5.slider("Ultrafiltration Coefficient (Kf) [mL/min/mmHg]", 2.0, 12.0, float(st.session_state["Kf"]), 0.5)
st.session_state["pi_gc"] = c6.slider("Plasma Oncotic Pressure (πgc) [mmHg]", 15.0, 35.0, float(st.session_state["pi_gc"]), 1.0)

st.session_state["Hct"] = st.slider("Hematocrit (%)", 20.0, 60.0, float(st.session_state["Hct"]), 1.0)

col_reset, col_norm = st.columns([1,1])
with col_reset:
    if st.button("↩️ Reset to Baseline", use_container_width=True):
        for k, v in BASELINE.items():
            st.session_state[k] = v
        _rerun()
with col_norm:
    if st.button("✅ Set Normal Defaults", use_container_width=True):
        for k, v in BASELINE.items():
            st.session_state[k] = v
        _rerun()

# ---------------- Compute ----------------
params = {k: st.session_state[k] for k in BASELINE.keys()}
out = compute_outputs(params)

# ---------------- Results ----------------
st.markdown("### Calculated Results")
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("GFR", f"{out['GFR']:.1f} mL/min")
m2.metric("RPF", f"{out['RPF']:.1f} mL/min")
m3.metric("RBF", f"{out['RBF']:.1f} mL/min")
m4.metric("FF", f"{out['FF']:.1f} %")
m5.metric("Pgc", f"{out['Pgc']:.1f} mmHg")
m6.metric("NFP", f"{out['NFP']:.1f} mmHg")

st.divider()

# ---------------- Interpretation Guide ----------------
st.markdown("### Interpretation Guide")
left, right = st.columns(2)

with left:
    st.markdown("""
**GFR Interpretation**
- **> 90 mL/min**: Normal kidney function  
- **60–89 mL/min**: Mild decrease (Stage 2 CKD)  
- **30–59 mL/min**: Moderate decrease (Stage 3 CKD)  
- **15–29 mL/min**: Severe decrease (Stage 4 CKD)  
- **< 15 mL/min**: Kidney failure (Stage 5 CKD)

**Filtration Fraction (FF)**
- **Normal**: ~16–20%  
- **Increased FF**: Often **efferent constriction (↑Re)**  
- **Decreased FF**: Often **afferent constriction (↑Ra)**
""")

with right:
    st.markdown("""
**Key Relationships**
- **GFR = Kf × NFP**
- **NFP = Pgc − Pbs − πgc**
- **FF = (GFR / RPF) × 100%**
- **RBF = RPF / (1 − Hct)**

**Clinical Pearls**
- **↑Re** raises **Pgc** → may preserve or raise **GFR** while **RPF** falls → **FF↑**  
- **↑Ra** lowers **Pgc** and **RPF** → **GFR↓**, **FF↓**  
- **Obstruction (↑Pbs)** reduces **NFP** → **GFR↓**  
- **↓Kf** (membrane/area loss) reduces **GFR** even with normal pressures  
""")


