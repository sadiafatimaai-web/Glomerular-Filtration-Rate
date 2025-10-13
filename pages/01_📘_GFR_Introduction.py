# pages/01_📘_GFR_Introduction.py
import streamlit as st
from utils_nav import render_sidebar

st.set_page_config(page_title="GFR — Introduction", layout="wide")
render_sidebar()

st.title("💧 Glomerular Filtration Rate — Concepts and Interactive Simulator")
st.divider()

# ─────────────────────────────
# 📖 Introduction
# ─────────────────────────────
st.header("📖 Introduction")
st.markdown(
    """
**Glomerular Filtration Rate (GFR)** is the volume of plasma filtered from glomerular capillaries into Bowman's capsule per minute.  
It’s the primary indicator of kidney filtration function.

**Normal GFR:** ~120–125 mL/min (≈180 L/day)  
**Clinical significance:** Reflects filtration efficiency and nephron integrity  
**Measurement:** eGFR (creatinine-based), creatinine clearance, or inulin clearance
"""
)

# ─────────────────────────────
# 🧠 Basic Physiological Concepts
# ─────────────────────────────
st.subheader("🧠 Basic Physiological Concepts")

st.markdown(
    """
**The Nephron (functional unit)**
- **Glomerulus:** capillary tuft where filtration occurs  
- **Bowman’s capsule:** collects filtrate  
- **Tubular system:** modifies filtrate (reabsorption/secretion)

**Blood Flow Pathway**  
Renal artery → **Afferent arteriole** → **Glomerular capillaries** → **Efferent arteriole** → Peritubular capillaries/vasa recta

**Typical Values**
- **Renal Blood Flow (RBF):** ~1200 mL/min (≈20% of cardiac output)  
- **Renal Plasma Flow (RPF):** ~650 mL/min  
- **Filtration Fraction (FF):** `GFR / RPF × 100` ≈ **~20%**
"""
)

# ─────────────────────────────
# ⚙️ Starling Forces in Filtration
# ─────────────────────────────
st.subheader("⚙️ Starling Forces in Filtration")

st.markdown(
    """
| Force                          | Symbol | Direction      | Typical       | Effect    |
|-------------------------------:|:------:|:---------------|:--------------|:----------|
| Glomerular capillary pressure  |  Pgc   | → Filtration   | 45–60 mmHg    | Favors    |
| Bowman’s capsule pressure      |  Pbs   | ← Filtration   | ~10 mmHg      | Opposes   |
| Glomerular oncotic pressure    |  πgc   | ← Filtration   | ~25 mmHg      | Opposes   |
| Bowman’s oncotic pressure      |  πbs   | → Filtration   | ≈ 0 mmHg      | (neglig.) |
"""
)

# ─────────────────────────────
# 🧮 The Starling Equation
# ─────────────────────────────
st.subheader("🧮 The Starling Equation")

st.markdown(
    r"""
**Net Filtration Pressure (NFP)**  
\[
\text{NFP} = (P_{gc} - P_{bs}) - (\pi_{gc} - \pi_{bs})
\]
Since \(\pi_{bs} \approx 0\) in normal conditions:
\[
\text{NFP} = P_{gc} - P_{bs} - \pi_{gc}
\]

**Example:** \( \text{NFP} = 55 - 10 - 25 = 20\ \text{mmHg} \)

**Glomerular Filtration Rate (GFR)**  
\[
\text{GFR} = K_f \times \text{NFP}
\]
**Example:** \( \text{GFR} = 12\ \text{mL/min/mmHg} \times 10\ \text{mmHg} \approx 120\ \text{mL/min} \)
"""
)

# ─────────────────────────────
# 🔬 Factors Affecting Each Starling Force
# ─────────────────────────────
st.subheader("🔬 Factors Affecting Each Starling Force")

with st.container():
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
**Pgc (Glomerular Capillary Pressure)**  
**↑ Increased by**
- Increased arterial pressure
- **Afferent dilation**
- **Efferent constriction**

**↓ Decreased by**
- Decreased arterial pressure
- **Afferent constriction**
- **Efferent dilation**
"""
        )

    with c2:
        st.markdown(
            """
**Pbs (Bowman’s Capsule Pressure)**  
**↑ Increased by**
- Urinary tract obstruction
- Bladder outlet obstruction
- Ureteral stones
- Prostatic hyperplasia

**Normal:** ~10 mmHg
"""
        )

st.markdown(
    """
**πgc (Glomerular Oncotic Pressure)**  
**↑ Increased by**
- Dehydration
- Decreased renal plasma flow
- Hyperproteinemia

**↓ Decreased by**
- Hypoalbuminemia
- Nephrotic syndrome
- Liver disease
"""
)

# ─────────────────────────────
# 🧱 The Ultrafiltration Coefficient (Kf)
# ─────────────────────────────
st.subheader("🧱 The Ultrafiltration Coefficient (Kf)")

st.markdown(
    """
**Kf** reflects the **permeability** and **surface area** of the filtration barrier.

**Structural components**
- Fenestrated capillary endothelium  
- Glomerular basement membrane  
- Podocyte foot processes (filtration slits)

**Normal Kf:** ~12 mL/min/mmHg

**Kf is decreased in**
- Glomerulonephritis  
- Diabetic nephropathy (late stages)  
- Chronic kidney disease  
- Glomerular sclerosis  

**Result:** Lower **GFR** even when pressures are normal.
"""
)

# ─────────────────────────────
# 🧭 Study Tips
# ─────────────────────────────
st.divider()
st.markdown(
    """
**Study tips**
- Keep the identities straight: **Pgc** pushes out, **Pbs** and **πgc** push back.  
- **FF ≈ 20%** at baseline; **↑FF** suggests **efferent constriction**, **↓FF** suggests **afferent constriction**.  
- If **Kf** falls (membrane damage/scar), **GFR** drops despite normal pressures.
"""
)

# ─────────────────────────────
# 📚 References
# ─────────────────────────────
st.subheader("📚 References")
st.markdown(
    """
- *Guyton and Hall Textbook of Medical Physiology*, 14th ed.  
- *Ganong’s Review of Medical Physiology*, 26th ed.  
- *Sherwood’s Human Physiology: From Cells to Systems*, 10th ed.
"""
)



