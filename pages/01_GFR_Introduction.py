
import streamlit as st
from utils_nav import render_sidebar

st.set_page_config(page_title="GFR Physiology Simulator", page_icon="🫘", layout="wide")
render_sidebar()


st.title("Hemodynamic Parameter Manipulation")

# ← LEFT NAV WORKS
render_sidebar()

# ... rest of your simulator code ...


st.markdown("""
<style>
footer {visibility: hidden;}
div.block-container {
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)


import streamlit as st
import qrcode
from io import BytesIO

# ───────────────────────────────────────────────
# PAGE CONFIG
# ───────────────────────────────────────────────
st.set_page_config(page_title="GFR Physiology Simulator", layout="wide")

# Title and credit
st.title("💧 Glomerular Filtration Rate — Concepts and Interactive Simulator")
st.markdown("#### Developed by **Dr Sadia Fatima** — *October 2025*")

# ───────────────────────────────────────────────
# DYNAMIC QR CODE (for Streamlit Cloud)
# ───────────────────────────────────────────────
try:
    base_url = st.runtime.get_instance()._runtime.hosted_url
except Exception:
    base_url = None

if not base_url:
    base_url = "https://gfrsim.streamlit.app"  # Fallback for local run

# Generate QR code
qr_img = qrcode.make(base_url)
buf = BytesIO()
qr_img.save(buf, format="PNG")

# Display layout with QR
col1, col2 = st.columns([5, 1])
with col2:
    st.image(buf.getvalue(), width=130, caption="📱 Scan to Open")
with col1:
    st.markdown("""
Welcome to the **Glomerular Filtration Rate (GFR) Interactive Simulator** —  
an educational platform to explore **renal hemodynamics**, **Starling forces**, and **clinical physiology**.
""")

st.divider()

# ───────────────────────────────────────────────
# INTRODUCTION CONTENT
# ───────────────────────────────────────────────
st.header("📖 Introduction")

st.markdown("""
**Glomerular Filtration Rate (GFR)** is the volume of plasma filtered from glomerular capillaries into Bowman’s capsule per unit time.  
It is the **primary indicator of renal function**, reflecting the kidneys’ ability to remove metabolic waste and maintain homeostasis.

**Normal GFR:** ~120–125 mL/min (≈180 L/day)  
**Clinical Significance:** Indicates filtration efficiency and nephron integrity  
**Measurement:** Estimated using creatinine clearance, serum creatinine, or direct inulin clearance
""")

st.subheader("🧠 Basic Physiological Concepts")
st.markdown("""
**The Nephron:**
- Each kidney contains ~1 million nephrons  
- **Glomerulus:** Capillary tuft where filtration occurs  
- **Bowman’s Capsule:** Collects the filtrate  
- **Tubular System:** Processes filtrate into urine  

**Blood Flow Pathway:**
Renal artery → Afferent arteriole → Glomerular capillaries → Efferent arteriole → Peritubular capillaries

**Typical Values:**
- **Renal Blood Flow (RBF):** ~1200 mL/min (≈20% of cardiac output)  
- **Renal Plasma Flow (RPF):** ~650 mL/min  
- **Filtration Fraction (FF):** ~20 %
""")

st.subheader("⚙️ Starling Forces in Glomerular Filtration")
st.markdown("""
Filtration is governed by the balance between **hydrostatic** and **oncotic** pressures across the glomerular capillary membrane.

| Force | Symbol | Direction | Typical | Effect |
|--------|---------|------------|----------|---------|
| Glomerular capillary pressure | Pgc | → Filtration | 45–60 mmHg | Favors filtration |
| Bowman’s capsule pressure | Pbs | ← Filtration | ~10 mmHg | Opposes filtration |
| Glomerular oncotic pressure | πgc | ← Filtration | ~25 mmHg | Opposes filtration |
| Bowman’s oncotic pressure | πbs | → Filtration | ≈ 0 mmHg | Favors filtration |

**Net Filtration Pressure (NFP):**
\[
NFP = (P_{gc} - P_{bs}) - (π_{gc} - π_{bs})
\]

Example:  
`NFP = 55 - 10 - 25 = 20 mmHg`  
`GFR = Kf × NFP → 12 × 10 = 120 mL/min`
""")

st.subheader("🔬 Factors Affecting Filtration")
st.markdown("""
- **↑ Pgc:** Increased arterial pressure, afferent dilation, or efferent constriction  
- **↓ Pgc:** Afferent constriction or efferent dilation  
- **↑ Pbs:** Urinary tract obstruction → ↓NFP → ↓GFR  
- **↑ πgc:** Dehydration → ↑oncotic pressure → ↓GFR  
- **↓ Kf:** Glomerulonephritis or diabetic nephropathy → ↓GFR  
""")

st.subheader("🎯 Ready to Explore?")
st.markdown("""
Navigate using the sidebar tabs to explore renal dynamics:

1. **🧮 Parameter Simulator** — manipulate pressures & observe GFR changes  
2. **🧠 Autoregulation** — explore renal stability across MAP range  
3. **⚡ Quick Scenarios** — visualize predefined physiological states  
4. **📝 Cases and Worksheet** — analyze clinical pathophysiology  
5. **🎞️ Videos and Slides** — watch and review core concepts  

💡 *Use all tabs to gain a comprehensive understanding of GFR regulation.*
""")

st.success("💧 Begin by selecting '🧮 Parameter Simulator' from the sidebar to start exploring.")

st.divider()

# ───────────────────────────────────────────────
# REFERENCES SECTION
# ───────────────────────────────────────────────
st.subheader("📚 References")

st.markdown("""
1. **Guyton and Hall Textbook of Medical Physiology**, 15th Edition, John E. Hall, Elsevier, 2021.  
2. **Review of Medical Physiology**, 26th Edition, William F. Ganong, McGraw-Hill Education, 2020.  
3. **Human Physiology: From Cells to Systems**, 10th Edition, Lauralee Sherwood, Cengage Learning, 2023.  
""")

st.caption("These authoritative sources form the foundational reference for the concepts illustrated in this simulator.")

