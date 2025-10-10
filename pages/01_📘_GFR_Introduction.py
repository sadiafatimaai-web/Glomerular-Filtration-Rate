# pages/01_Intro.py
import streamlit as st
from utils_nav import render_sidebar

st.set_page_config(page_title="GFR — Introduction", layout="wide")
render_sidebar()

st.title("💧 Glomerular Filtration Rate — Concepts and Interactive Simulator")
st.markdown("#### Developed by **Dr Sadia Fatima**")

st.divider()
st.header("📖 Introduction")

st.markdown("""
**Glomerular Filtration Rate (GFR)** is the volume of plasma filtered from glomerular capillaries into Bowman's capsule per minute.  
It is a primary indicator of kidney function.

**Normal GFR:** ~120–125 mL/min (≈180 L/day)  
**Clinical significance:** Indicates filtration efficiency and nephron integrity  
**Measurement:** eGFR (creatinine), creatinine clearance, or inulin clearance
""")

st.subheader("🧠 Basic Physiological Concepts")
st.markdown("""
**The Nephron**
- ~1 million per kidney  
- **Glomerulus:** filtration  
- **Bowman’s capsule:** collects filtrate  
- **Tubules:** modify filtrate  

**Blood Flow Pathway**  
Renal artery → Afferent arteriole → Glomerular capillaries → Efferent arteriole → Peritubular capillaries

**Typical Values**
- **RBF:** ~1200 mL/min  
- **RPF:** ~650 mL/min  
- **FF:** ~20%
""")

st.subheader("⚙️ Starling Forces in Filtration")
st.markdown("""
| Force | Symbol | Direction | Typical | Effect |
|------|--------|-----------|---------|--------|
| Glomerular capillary pressure | Pgc | → Filtration | 45–60 mmHg | Favors |
| Bowman’s capsule pressure | Pbs | ← Filtration | ~10 mmHg | Opposes |
| Glomerular oncotic pressure | πgc | ← Filtration | ~25 mmHg | Opposes |
| Bowman’s oncotic pressure | πbs | → Filtration | ≈ 0 mmHg | Favors |

**Net Filtration Pressure (NFP):**  
`NFP = (Pgc - Pbs) - (πgc - πbs)`

Example: `NFP = 55 - 10 - 25 = 20 mmHg` → `GFR = Kf × NFP = 12 × 10 = 120 mL/min`
""")

st.subheader("🔬 Factors Affecting Filtration")
st.markdown("""
- **↑ Pgc:** ↑ arterial pressure, afferent dilation, efferent constriction  
- **↓ Pgc:** afferent constriction, efferent dilation  
- **↑ Pbs:** obstruction → ↓NFP → ↓GFR  
- **↑ πgc:** dehydration → ↓GFR  
- **↓ Kf:** glomerulonephritis/diabetic nephropathy → ↓GFR  
""")

st.divider()
st.subheader("📚 References")
st.markdown("""
1. **Guyton and Hall Textbook of Medical Physiology**, 15th Ed., John E. Hall, Elsevier, 2021.  
2. **Ganong’s Review of Medical Physiology**, 26th Ed., William F. Ganong, McGraw-Hill, 2020.  
3. **Human Physiology: From Cells to Systems**, 10th Ed., Lauralee Sherwood, Cengage, 2023.  
""")


