# pages/06_Quick_Scenarios.py
import streamlit as st
import pandas as pd
import math

# Try to use your physiology module if available; otherwise use a light fallback.
try:
    from physiology import (
        # expected names in your repo (adjust if yours differ)
        compute_outputs as _physio_compute,      # returns dict with keys: GFR,RPF,FF,Pgc,NFP,RBF
        DEFAULT_SCENARIOS as _PHYSIO_SCENARIOS,  # dict of scenarios->param dict
    )
    HAVE_PHYSIO = True
except Exception:
    HAVE_PHYSIO = False

from utils_nav import render_sidebar

st.set_page_config(page_title="GFR — Quick Scenarios", layout="wide")
render_sidebar()

st.title("⚡ Quick Scenarios")
st.caption("Pick a scenario, tweak parameters, and visualize the impact on GFR, RPF, FF, and key pressures.")

# --------------------------
# Baseline + Scenarios
# --------------------------
BASELINE = {
    "MAP": 100.0,   # mmHg
    "Ra": 1.0,      # relative
    "Re": 2.0,      # relative
    "Pbs": 10.0,    # mmHg
    "Kf": 12.0,     # mL/min/mmHg
    "pi_gc": 25.0,  # mmHg
    "Hct": 45.0,    # %
}

# If you have them defined in physiology.py, use those.
if HAVE_PHYSIO:
    SCENARIOS = dict(_PHYSIO_SCENARIOS)  # copy to avoid accidental mutation
else:
    SCENARIOS = {
        "Normal": {**BASELINE},
        "Increased Ra": {**BASELINE, "Ra": 2.5},              # Afferent constriction
        "Mild Re Increase": {**BASELINE, "Re": 3.5},          # Mild efferent constriction
        "Severe Re Increase": {**BASELINE, "Re": 5.0},
        "Decreased Kf": {**BASELINE, "Kf": 6.0},
        "Increased Bowman": {**BASELINE, "Pbs": 25.0},
        "Decreased MAP": {**BASELINE, "MAP": 70.0},
    }

# --------------------------
# Physiology model (fallback)
# --------------------------
def _fallback_compute(params: dict) -> dict:
    """
    Lightweight, teaching-oriented model:
    - NFP = Pgc - Pbs - pi_gc
    - Pgc approximated from MAP and resistances (Ra/Re) with crude scaling
    - RPF scaled inversely with total resistance and hematocrit
    These are intentionally simplified for visualization (not for clinical decisions).
    """
    MAP, Ra, Re = params["MAP"], params["Ra"], params["Re"]
    Pbs, Kf, pi_gc, Hct = params["Pbs"], params["Kf"], params["pi_gc"], params["Hct"]

    # toy mapping of resistances to capillary pressure / flow
    total_R = Ra + 0.8*Re
    total_R = max(total_R, 0.1)

    # Approximate Pgc (kept in physiological-looking range)
    Pgc = max(35.0, min(99.0, MAP * (Re/(Ra+Re)) + 35*(1/total_R - 0.3)))

    # Net filtration pressure
    NFP = Pgc - Pbs - pi_gc

    # Plasma flow (arbitrary scaling to keep values readable)
    RPF = max(50.0, (MAP / total_R) * 4.5)  # mL/min
    # Renal blood flow from hematocrit
    RBF = RPF / max(1e-6, (1 - Hct/100.0))

    # GFR via Kf * NFP; floor at 0 to avoid negatives in display
    GFR = max(0.0, Kf * NFP)

    # Filtration fraction
    FF = (GFR / RPF) * 100.0 if RPF > 0 else 0.0

    return {
        "GFR": GFR,
        "RPF": RPF,
        "RBF": RBF,
        "FF": FF,
        "Pgc": Pgc,
        "NFP": NFP,
    }

def compute_outputs(params: dict) -> dict:
    if HAVE_PHYSIO:
        return _physio_compute(params)  # your authoritative model
    return _fallback_compute(params)

# --------------------------
# Top controls
# --------------------------
left, right = st.columns([1, 2])
with left:
    scenario_name = st.selectbox("Choose a scenario", list(SCENARIOS.keys()), index=0)
with right:
    compare_names = st.multiselect(
        "Compare with (select 1–3 scenarios)", [k for k in SCENARIOS.keys() if k != scenario_name],
        default=[]
    )

# Selected params (editable)
params = dict(SCENARIOS[scenario_name])  # start with scenario defaults
with st.expander("🧪 Tweak parameters (optional)", expanded=False):
    c1, c2, c3 = st.columns(3)
    params["MAP"] = c1.slider("Mean Arterial Pressure (MAP) [mmHg]", 40.0, 220.0, float(params["MAP"]), step=1.0)
    params["Ra"]  = c2.slider("Afferent Resistance (Ra) [rel units]", 0.5, 5.0, float(params["Ra"]), step=0.1)
    params["Re"]  = c3.slider("Efferent Resistance (Re) [rel units]", 0.5, 6.0, float(params["Re"]), step=0.1)

    c4, c5, c6 = st.columns(3)
    params["Pbs"]   = c4.slider("Bowman's Capsule Pressure (Pbs) [mmHg]", 5.0, 40.0, float(params["Pbs"]), step=1.0)
    params["Kf"]    = c5.slider("Ultrafiltration Coefficient (Kf) [mL/min/mmHg]", 2.0, 20.0, float(params["Kf"]), step=0.5)
    params["pi_gc"] = c6.slider("Plasma Oncotic Pressure (πgc) [mmHg]", 15.0, 35.0, float(params["pi_gc"]), step=1.0)

    params["Hct"]   = st.slider("Hematocrit (%)", 20.0, 60.0, float(params["Hct"]), step=1.0)
    st.caption("Tip: tweak values to mimic drugs or pathology, then see changes below.")

# --------------------------
# Compute + Metrics row
# --------------------------
out_sel = compute_outputs(params)
out_base = compute_outputs(BASELINE)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("GFR (mL/min)", f"{out_sel['GFR']:.1f}", delta=f"{out_sel['GFR']-out_base['GFR']:+.1f}")
m2.metric("RPF (mL/min)", f"{out_sel['RPF']:.1f}", delta=f"{out_sel['RPF']-out_base['RPF']:+.1f}")
m3.metric("FF (%)", f"{out_sel['FF']:.1f}", delta=f"{out_sel['FF']-out_base['FF']:+.1f}")
m4.metric("Pgc (mmHg)", f"{out_sel['Pgc']:.1f}", delta=f"{out_sel['Pgc']-out_base['Pgc']:+.1f}")
m5.metric("NFP (mmHg)", f"{out_sel['NFP']:.1f}", delta=f"{out_sel['NFP']-out_base['NFP']:+.1f}")

st.divider()

# --------------------------
# Visual: Selected vs Baseline
# --------------------------
import matplotlib.pyplot as plt

def bar_compare(selected: dict, baseline: dict):
    labels = ["GFR (mL/min)", "RPF (mL/min)", "FF (%)", "Pgc (mmHg)", "NFP (mmHg)"]
    s_vals = [selected["GFR"], selected["RPF"], selected["FF"], selected["Pgc"], selected["NFP"]]
    b_vals = [baseline["GFR"], baseline["RPF"], baseline["FF"], baseline["Pgc"], baseline["NFP"]]

    fig, ax = plt.subplots(figsize=(8, 4))
    x = range(len(labels))
    ax.bar([i-0.2 for i in x], b_vals, width=0.4, label="Baseline")
    ax.bar([i+0.2 for i in x], s_vals, width=0.4, label="Selected")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_ylabel("Value")
    ax.set_title("Selected Scenario vs Baseline")
    ax.legend()
    st.pyplot(fig, clear_figure=True)

colA, colB = st.columns([1.2, 1])
with colA:
    st.subheader("📊 Selected vs Baseline")
    bar_compare(out_sel, out_base)

# --------------------------
# Comparison table (multi-select)
# --------------------------
def row_for(name, p):
    o = compute_outputs(p)
    return {
        "Scenario": name,
        "MAP": p["MAP"], "Ra": p["Ra"], "Re": p["Re"], "Pbs": p["Pbs"], "Kf": p["Kf"], "πgc": p["pi_gc"], "Hct": p["Hct"],
        "GFR (mL/min)": o["GFR"], "RPF (mL/min)": o["RPF"], "RBF (mL/min)": o["RBF"],
        "FF (%)": o["FF"], "Pgc (mmHg)": o["Pgc"], "NFP (mmHg)": o["NFP"],
    }

rows = [row_for("Baseline", BASELINE), row_for(scenario_name+" (edited)", params)]
for nm in compare_names[:3]:
    rows.append(row_for(nm, SCENARIOS[nm]))

compare_df = pd.DataFrame(rows)

with colB:
    st.subheader("🔁 Compare")
    st.dataframe(compare_df, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Download comparison (CSV)",
        data=compare_df.to_csv(index=False).encode("utf-8"),
        file_name="gfr_quick_scenarios_compare.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()

# --------------------------
# Teaching notes (accordion)
# --------------------------
with st.expander("🧠 Teaching Notes", expanded=False):
    st.markdown("""
- **Afferent constriction (↑Ra)** ⟶ ↓Pgc → ↓NFP → ↓GFR and ↓RPF → **FF tends to fall**.
- **Efferent constriction (↑Re)** ⟶ initial ↑Pgc → may preserve/raise **GFR** while **RPF falls** → **FF rises**.
- **Obstruction (↑Pbs)** ⟶ ↓NFP → **↓GFR**.
- **Decreased Kf** (e.g., membrane damage/scarring) ⟶ **↓GFR** even if pressures are normal.
- **Hematocrit (Hct)** affects **RBF** via plasma fraction: RBF = RPF/(1−Hct).
""")


