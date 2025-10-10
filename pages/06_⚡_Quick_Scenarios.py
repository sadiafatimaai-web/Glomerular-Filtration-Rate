# pages/06_⚡_Quick_Scenarios.py
import streamlit as st
import pandas as pd

# Try to use your physiology module if available; otherwise use our calibrated fallback.
try:
    from physiology import (
        compute_outputs as _physio_compute,      # should return dict: GFR,RPF,FF,Pgc,NFP,RBF
        DEFAULT_SCENARIOS as _PHYSIO_SCENARIOS,  # optional dict of scenarios -> params
    )
    HAVE_PHYSIO = True
except Exception:
    HAVE_PHYSIO = False

from utils_nav import render_sidebar

st.set_page_config(page_title="GFR — Quick Scenarios", layout="wide")
render_sidebar()

st.title("⚡ Quick Scenarios")
st.caption("Pick a scenario, tweak parameters, and visualize the impact on GFR, RPF, FF, and key pressures.")

# ---------------- Baseline (calibrated) ----------------
# Baseline chosen to hit ~GFR 120, RPF 650, FF ~19% with our fallback model below.
BASELINE = {
    "MAP": 100.0,   # mmHg
    "Ra": 1.0,      # relative
    "Re": 2.0,      # relative
    "Pbs": 10.0,    # mmHg
    "Kf": 6.0,      # mL/min/mmHg  (calibrated)
    "pi_gc": 25.0,  # mmHg
    "Hct": 45.0,    # %
}

# Default scenarios (used if physiology.DEFAULT_SCENARIOS not provided)
DEFAULT_SCENARIOS = {
    "Normal": {**BASELINE},
    "Increased Ra": {**BASELINE, "Ra": 2.5},          # Afferent constriction -> ↓RPF, ↓Pgc -> ↓GFR, ↓FF
    "Mild Re Increase": {**BASELINE, "Re": 3.5},      # Mild efferent constriction -> ↑Pgc, ↓RPF -> FF↑ (GFR ≈ preserved)
    "Severe Re Increase": {**BASELINE, "Re": 5.0},    # Strong efferent constriction -> Pgc↑ a lot, RPF↓ -> FF↑↑
    "Decreased Kf": {**BASELINE, "Kf": 3.0},          # Filter coefficient drop -> ↓GFR even if pressures ok
    "Increased Bowman": {**BASELINE, "Pbs": 25.0},    # Obstruction -> backpressure -> ↓NFP -> ↓GFR
    "Decreased MAP": {**BASELINE, "MAP": 70.0},       # Hypotension -> ↓Pgc, ↓RPF -> ↓GFR
}

SCENARIOS = dict(DEFAULT_SCENARIOS)
if HAVE_PHYSIO:
    try:
        # If your physiology file defines scenarios, use them; else keep defaults above.
        SCENARIOS = dict(_PHYSIO_SCENARIOS)
    except Exception:
        pass

# ---------------- Calibrated fallback physiology model ----------------
def _fallback_compute(p: dict) -> dict:
    """
    Calibrated toy model to keep numbers in realistic ranges while preserving causal trends.
    - Pgc is tied to MAP and the Re/(Ra+Re) ratio (efferent → raises Pgc).
    - RPF ~ MAP / (Ra + 1.5*Re) scaled to ~650 mL/min at baseline (MAP=100, Ra=1, Re=2).
    - NFP = Pgc - Pbs - πgc
    - GFR = Kf * NFP (with Kf baseline 6 → GFR ~120 when NFP ~20)
    - RBF = RPF / (1 - Hct)
    """
    MAP, Ra, Re = float(p["MAP"]), float(p["Ra"]), float(p["Re"])
    Pbs, Kf, pi_gc, Hct = float(p["Pbs"]), float(p["Kf"]), float(p["pi_gc"]), float(p["Hct"])

    # 1) Pgc: base + efferent ratio + mild MAP influence; clamp to plausible range.
    #    Baseline (MAP=100, Ra=1, Re=2) -> ratio = 2/3 → Pgc ≈ 56 mmHg
    eff_ratio = Re / max(1e-6, (Ra + Re))
    Pgc = 48.0 + 12.0 * eff_ratio + 0.12 * (MAP - 100.0)
    Pgc = min(max(Pgc, 40.0), 80.0)

    # 2) RPF: scale so baseline ~650 mL/min (MAP=100, Ra=1, Re=2 ⇒ denom = 1 + 1.5*2 = 4)
    denom = max(0.1, Ra + 1.5 * Re)
    RPF = (MAP / denom) * 26.0  # 100/4*26 = 650 baseline

    # 3) NFP and GFR
    NFP = Pgc - Pbs - pi_gc                    # baseline ~56-10-25 = 21
    GFR = max(0.0, Kf * NFP)                  # baseline 6*21 = 126 mL/min

    # 4) RBF via hematocrit
    RBF = RPF / max(1e-6, (1.0 - Hct / 100.0))

    # 5) Filtration fraction
    FF = (GFR / RPF) * 100.0 if RPF > 0 else 0.0

    return {"GFR": GFR, "RPF": RPF, "RBF": RBF, "FF": FF, "Pgc": Pgc, "NFP": NFP}

def compute_outputs(p: dict) -> dict:
    return _physio_compute(p) if HAVE_PHYSIO else _fallback_compute(p)

# ---------------- UI controls ----------------
left, right = st.columns([1, 2])
with left:
    scenario_name = st.selectbox("Choose a scenario", list(SCENARIOS.keys()), index=0)
with right:
    compare_names = st.multiselect(
        "Compare with (select 1–3 scenarios)",
        [k for k in SCENARIOS.keys() if k != scenario_name],
        default=[],
    )

params = dict(SCENARIOS[scenario_name])
with st.expander("🧪 Tweak parameters (optional)", expanded=False):
    c1, c2, c3 = st.columns(3)
    params["MAP"] = c1.slider("MAP [mmHg]", 40.0, 220.0, float(params["MAP"]), 1.0)
    params["Ra"]  = c2.slider("Afferent Resistance (Ra)", 0.5, 5.0, float(params["Ra"]), 0.1)
    params["Re"]  = c3.slider("Efferent Resistance (Re)", 0.5, 6.0, float(params["Re"]), 0.1)

    c4, c5, c6 = st.columns(3)
    params["Pbs"]   = c4.slider("Pbs [mmHg]", 5.0, 40.0, float(params["Pbs"]), 1.0)
    params["Kf"]    = c5.slider("Kf [mL/min/mmHg]", 2.0, 12.0, float(params["Kf"]), 0.5)  # calibrated range
    params["pi_gc"] = c6.slider("πgc [mmHg]", 15.0, 35.0, float(params["pi_gc"]), 1.0)

    params["Hct"]   = st.slider("Hematocrit (%)", 20.0, 60.0, float(params["Hct"]), 1.0)
    st.caption("Tip: tweak values to mimic drugs or pathology, then see changes below.")

# ---------------- Compute + metrics ----------------
out_sel = compute_outputs(params)
out_base = compute_outputs(BASELINE)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("GFR (mL/min)", f"{out_sel['GFR']:.1f}", f"{out_sel['GFR']-out_base['GFR']:+.1f}")
m2.metric("RPF (mL/min)", f"{out_sel['RPF']:.1f}", f"{out_sel['RPF']-out_base['RPF']:+.1f}")
m3.metric("FF (%)", f"{out_sel['FF']:.1f}", f"{out_sel['FF']-out_base['FF']:+.1f}")
m4.metric("Pgc (mmHg)", f"{out_sel['Pgc']:.1f}", f"{out_sel['Pgc']-out_base['Pgc']:+.1f}")
m5.metric("NFP (mmHg)", f"{out_sel['NFP']:.1f}", f"{out_sel['NFP']-out_base['NFP']:+.1f}")

st.divider()

# ---------------- Selected vs Baseline chart ----------------
st.subheader("📊 Selected vs Baseline")

chart_df = pd.DataFrame(
    {
        "Baseline": [out_base["GFR"], out_base["RPF"], out_base["FF"], out_base["Pgc"], out_base["NFP"]],
        "Selected": [out_sel["GFR"], out_sel["RPF"], out_sel["FF"], out_sel["Pgc"], out_sel["NFP"]],
    },
    index=["GFR (mL/min)", "RPF (mL/min)", "FF (%)", "Pgc (mmHg)", "NFP (mmHg)"],
)
st.bar_chart(chart_df)

# ---------------- Comparison table & download ----------------
def row_for(name, p):
    o = compute_outputs(p)
    return {
        "Scenario": name,
        "MAP": p["MAP"], "Ra": p["Ra"], "Re": p["Re"], "Pbs": p["Pbs"], "Kf": p["Kf"], "πgc": p["pi_gc"], "Hct": p["Hct"],
        "GFR (mL/min)": o["GFR"], "RPF (mL/min)": o["RPF"], "RBF (mL/min)": o["RBF"],
        "FF (%)": o["FF"], "Pgc (mmHg)": o["Pgc"], "NFP (mmHg)": o["NFP"],
    }

rows = [row_for("Baseline", BASELINE), row_for(scenario_name + " (edited)", params)]
for nm in compare_names[:3]:
    rows.append(row_for(nm, SCENARIOS[nm]))

compare_df = pd.DataFrame(rows)

st.subheader("🔁 Compare scenarios")
st.dataframe(compare_df, use_container_width=True, hide_index=True)
st.download_button(
    "⬇️ Download comparison (CSV)",
    data=compare_df.to_csv(index=False).encode("utf-8"),
    file_name="gfr_quick_scenarios_compare.csv",
    mime="text/csv",
    use_container_width=True,
)

st.divider()

with st.expander("🧠 Teaching Notes", expanded=False):
    st.markdown("""
- **Afferent constriction (↑Ra)** → ↓Pgc, ↓RPF → **↓NFP → ↓GFR**, **FF falls**.
- **Efferent constriction (↑Re)** → ↑Pgc, ↓RPF → **FF rises**; GFR may be preserved or mildly ↑ at modest Re.
- **Increased Bowman pressure (↑Pbs)** → backpressure → **↓NFP → ↓GFR**.
- **Decreased Kf** → membrane/area loss → **↓GFR** even if pressures are normal.
- **Lower MAP** → ↓Pgc and ↓RPF → **↓GFR**.
- **RBF = RPF/(1−Hct)**; raising Hct lowers RBF at the same RPF.
""")



