import streamlit as st
import random

try:
    from utils_nav import render_sidebar
    render_sidebar()
except Exception:
    pass

st.set_page_config(page_title="Cases & Worksheet — GFR", layout="wide")

st.header("🧪 Cases & Worksheet")
st.markdown("""
Practice your understanding of renal hemodynamics and glomerular filtration.  
You can either **download the worksheet** or **generate random cases** to solve!
""")

# --------------------------------------------------
# Optional PDF Worksheet
# --------------------------------------------------
from pathlib import Path
pdf_path = Path("assets/GFR_Worksheet.pdf")
with st.expander("📄 Download a printable worksheet (optional)", expanded=False):
    if pdf_path.exists():
        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download Worksheet (PDF)",
                f,
                file_name="GFR_Worksheet.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    else:
        st.info("Upload your worksheet to `assets/GFR_Worksheet.pdf` to enable this feature.")

st.divider()

# --------------------------------------------------
# Function to simulate physiology
# --------------------------------------------------
def simulate_case():
    """Generate random but physiologically realistic renal parameters"""
    case_types = [
        "Afferent Arteriolar Constriction",
        "Efferent Arteriolar Constriction",
        "Dehydration",
        "ACE Inhibitor Effect",
        "Acute Urinary Obstruction",
        "Early Diabetic Nephropathy",
        "Renal Artery Stenosis",
    ]
    case = random.choice(case_types)

    # Physiological ranges
    MAP = random.uniform(70, 110)
    Ra = random.uniform(0.8, 2.0)
    Re = random.uniform(0.8, 2.5)
    Pbs = random.uniform(10, 18)
    pi_gc = random.uniform(25, 32)
    Kf = random.uniform(10, 14)
    Hct = random.uniform(0.38, 0.48)

    # Derived pressures and flows (simplified physiological relationships)
    Pgc = MAP * (Re / (Ra + Re)) + 10
    NFP = Pgc - Pbs - pi_gc
    GFR = max(0, Kf * NFP)
    RPF = (MAP / (Ra + Re)) * 120
    RBF = RPF / (1 - Hct)
    FF = (GFR / RPF) * 100 if RPF else 0

    return {
        "case": case,
        "MAP": MAP,
        "Ra": Ra,
        "Re": Re,
        "Pbs": Pbs,
        "pi_gc": pi_gc,
        "Kf": Kf,
        "Hct": Hct,
        "Pgc": Pgc,
        "NFP": NFP,
        "GFR": GFR,
        "RPF": RPF,
        "RBF": RBF,
        "FF": FF,
    }

# --------------------------------------------------
# Random Case Generator UI
# --------------------------------------------------
st.subheader("🎲 Generate a Random Case")

if st.button("🔁 Generate Case", use_container_width=True):
    case = simulate_case()
    st.session_state["case"] = case

if "case" in st.session_state:
    c = st.session_state["case"]
    st.markdown(f"### **Case Type:** {c['case']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mean Arterial Pressure (MAP)", f"{c['MAP']:.1f} mmHg")
        st.metric("Bowman's Capsule Pressure (Pbs)", f"{c['Pbs']:.1f} mmHg")
    with col2:
        st.metric("Afferent Resistance (Ra)", f"{c['Ra']:.2f} rel units")
        st.metric("Efferent Resistance (Re)", f"{c['Re']:.2f} rel units")
    with col3:
        st.metric("Oncotic Pressure (πgc)", f"{c['pi_gc']:.1f} mmHg")
        st.metric("Ultrafiltration Coefficient (Kf)", f"{c['Kf']:.2f}")

    st.markdown("---")
    st.markdown("### 🧮 Derived Results")
    colA, colB, colC = st.columns(3)
    with colA:
        st.metric("Glomerular Pressure (Pgc)", f"{c['Pgc']:.1f} mmHg")
        st.metric("Net Filtration Pressure (NFP)", f"{c['NFP']:.1f} mmHg")
    with colB:
        st.metric("GFR", f"{c['GFR']:.1f} mL/min")
        st.metric("Filtration Fraction (FF)", f"{c['FF']:.1f}%")
    with colC:
        st.metric("RPF", f"{c['RPF']:.1f} mL/min")
        st.metric("RBF", f"{c['RBF']:.1f} mL/min")

    st.caption("All parameters are within realistic physiological or mild pathological ranges.")

    st.markdown("---")
    st.subheader("💬 Reflective Questions")

    st.markdown(
        f"""
1. Based on the parameters, describe how this case (“**{c['case']}**”) affects renal hemodynamics.  
2. Which Starling force is primarily altered (Pgc, Pbs, or πgc)?  
3. How does this change influence **NFP** and **GFR**?  
4. Predict what happens to **RPF** and **FF** and explain physiologically.  
5. Suggest one **clinical condition or drug** that could cause a similar pattern.
"""
    )
    st.text_area("🧠 Your Explanation:", height=150, key="reflection")

    st.success("✅ Tip: Compare your reasoning with simulator data on the other tabs!")

else:
    st.info("Click **🔁 Generate Case** to create a random physiological scenario.")

st.divider()
st.caption("Built for renal physiology learning — each case uses realistic GFR and RPF ranges.")


