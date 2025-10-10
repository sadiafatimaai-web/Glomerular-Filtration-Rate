import streamlit as st
from pathlib import Path

# ---- custom sidebar (keep only if you use utils_nav) ----
try:
    from utils_nav import render_sidebar
    render_sidebar()
except Exception:
    pass

st.set_page_config(page_title="Cases & Worksheet — GFR", layout="wide")

st.header("🧪 Cases & Worksheet")
st.write(
    "Use this worksheet to practice key concepts before class. "
    "Answer in the boxes below and bring your reasoning to discuss."
)

# ---------------------------------------------------------------------
# Optional: downloadable PDF worksheet if you add it later at assets/GFR_Worksheet.pdf
# ---------------------------------------------------------------------
pdf_path = Path("assets/GFR_Worksheet.pdf")
with st.expander("📄 Download a printable PDF (optional)", expanded=False):
    if pdf_path.exists():
        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download Worksheet (PDF)",
                data=f,
                file_name="GFR_Worksheet.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        st.caption("If you update the PDF, keep the same path: `assets/GFR_Worksheet.pdf`.")
    else:
        st.info("Add your PDF at `assets/GFR_Worksheet.pdf` to enable downloads.")

st.divider()

# ---------------------------------------------------------------------
# Section 1 — Quick Refresher + Self-check calculator
# ---------------------------------------------------------------------
st.subheader("Section 1 — Refresher & Self-Check Calculator")

with st.expander("Formulae recap", expanded=True):
    st.markdown(
        """
- **Net Filtration Pressure (NFP)** = `Pgc − Pbs − πgc`  
- **GFR** = `Kf × NFP`  
- **Filtration Fraction (FF)** = `GFR / RPF × 100%`
        """
    )

colA, colB, colC = st.columns(3)
with colA:
    Pgc = st.number_input("Pgc (mmHg)", 20.0, 120.0, 60.0, step=1.0)
    Pbs = st.number_input("Pbs (mmHg)", 0.0, 40.0, 15.0, step=1.0)
with colB:
    pi_gc = st.number_input("πgc (mmHg)", 5.0, 45.0, 30.0, step=1.0)
    Kf = st.number_input("Kf (mL/min/mmHg)", 1.0, 30.0, 12.0, step=0.5)
with colC:
    RPF = st.number_input("RPF (mL/min) (optional, for FF)", 100.0, 1500.0, 650.0, step=10.0)

NFP = Pgc - Pbs - pi_gc
GFR = Kf * NFP
FF = (GFR / RPF) * 100 if RPF else None

st.markdown(
    f"""
**Calculated:**  
- NFP = `{NFP:.1f}` mmHg  
- GFR = `{GFR:.1f}` mL/min  
- FF = `{FF:.1f}%` (using RPF = {RPF:.0f} mL/min)
"""
)

st.caption("Targets: normal GFR ≈ 120 mL/min; FF ≈ 16–20% in typical physiology.")

st.divider()

# ---------------------------------------------------------------------
# Section 2 — Basic Calculations
# ---------------------------------------------------------------------
st.subheader("Section 2 — Basic Calculations")

st.markdown(
    """
1) **Compute GFR** for: Pgc=60 mmHg, Pbs=15 mmHg, πgc=30 mmHg, Kf=12 mL/min/mmHg.  
   (Show your work.)
"""
)
st.text_area("Your answer (mL/min) & steps:", key="calc_q1", height=80)

st.markdown(
    """
2) **Effect of Afferent Constriction**  
   Predict the qualitative change in **GFR** and **RPF** when **afferent resistance increases**.
"""
)
st.radio(
    "Choose the best option:",
    [
        "Both increase",
        "Both decrease",
        "GFR decreases, RPF decreases",
        "GFR increases, RPF decreases",
    ],
    key="calc_q2",
)

st.markdown(
    """
3) **Effect of Efferent Constriction** (mild–moderate)  
   Predict the change in **GFR** and **FF** with **efferent constriction** (assume RPF falls).
"""
)
st.radio(
    "Choose the best option:",
    [
        "GFR ↑, FF ↑",
        "GFR ↓, FF ↓",
        "GFR ↔, FF ↓",
        "GFR ↑, FF ↓",
    ],
    key="calc_q3",
)

st.divider()

# ---------------------------------------------------------------------
# Section 3 — Conceptual Short-Answer
# ---------------------------------------------------------------------
st.subheader("Section 3 — Conceptual Short-Answer")

st.markdown("4) **Dehydration** raises plasma oncotic pressure (πgc). Predict changes in **GFR** and **FF** and explain why.")
st.text_area("Your reasoning:", key="sa_q4", height=100)

st.markdown("5) **Urinary tract obstruction** elevates **Pbs**. Explain the impact on **NFP** and **GFR**.")
st.text_area("Your reasoning:", key="sa_q5", height=100)

st.markdown(
    "6) **ACE inhibitors** reduce angiotensin II. Predict their effect on **efferent tone**, **GFR**, and **FF** in a patient with high RAAS activity."
)
st.text_area("Your reasoning:", key="sa_q6", height=100)

st.markdown(
    "7) **NSAIDs** inhibit prostaglandins. In a volume-depleted patient, how might this change **afferent tone** and **GFR**?"
)
st.text_area("Your reasoning:", key="sa_q7", height=100)

st.markdown(
    "8) **Severe hypoalbuminemia** lowers πgc. Predict the primary direction of change in **NFP** and **GFR**, with reasoning."
)
st.text_area("Your reasoning:", key="sa_q8", height=100)

st.divider()

# ---------------------------------------------------------------------
# Section 4 — Clinical Vignettes
# ---------------------------------------------------------------------
st.subheader("Section 4 — Clinical Cases")

with st.expander("Case A — Renal Artery Stenosis", expanded=True):
    st.markdown(
        """
A 65-year-old with long-standing hypertension and renal artery stenosis presents with rising creatinine.  
**Question A1.** Which compensatory mechanism most helps maintain GFR?  
**Question A2.** What happens to RPF and FF?
        """
    )
    st.text_area("A1 (mechanism):", key="caseA1", height=60)
    st.text_area("A2 (RPF/FF):", key="caseA2", height=60)

with st.expander("Case B — Post-renal Obstruction", expanded=False):
    st.markdown(
        """
A 72-year-old male with BPH has acute urinary retention with bilateral hydronephrosis.  
**Question B1.** Which Starling term changes first and in what direction?  
**Question B2.** Net effect on NFP and GFR?
        """
    )
    st.text_area("B1:", key="caseB1", height=60)
    st.text_area("B2:", key="caseB2", height=60)

with st.expander("Case C — Early Diabetic Nephropathy", expanded=False):
    st.markdown(
        """
A 40-year-old with new-onset T2DM shows glomerular **hyperfiltration**.  
**Question C1.** Which arteriolar change is most likely?  
**Question C2.** How do GFR and FF change early?
        """
    )
    st.text_area("C1:", key="caseC1", height=60)
    st.text_area("C2:", key="caseC2", height=60)

with st.expander("Case D — Severe Dehydration", expanded=False):
    st.markdown(
        """
A 24-year-old returns from a desert trek with tachycardia and orthostasis. Labs suggest hemoconcentration.  
**Question D1.** Predict change in πgc and its effect on GFR.  
**Question D2.** Explain what happens to FF.
        """
    )
    st.text_area("D1:", key="caseD1", height=60)
    st.text_area("D2:", key="caseD2", height=60)

st.divider()

# ---------------------------------------------------------------------
# Section 5 — Challenge / Bring to Class
# ---------------------------------------------------------------------
st.subheader("Section 5 — Challenge Problems")

st.markdown(
    """
9) A drug selectively **dilates the afferent arteriole** while keeping efferent tone constant.  
   Predict the changes in **Pgc**, **GFR**, **RPF**, and **FF**. Provide a mechanism-based explanation.
"""
)
st.text_area("Your reasoning:", key="chall_q9", height=120)

st.markdown(
    """
10) A patient with CKD has **decreased Kf** from glomerulosclerosis.  
    What happens to **GFR** even if pressures are normal, and why might the kidney **retain salt/water** as compensation?
"""
)
st.text_area("Your reasoning:", key="chall_q10", height=120)

st.success("✅ Bring these written answers to class — we’ll compare and discuss approaches.")

