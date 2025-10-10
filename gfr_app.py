# gfr_app.py  (Landing page / Home)
import base64
from io import BytesIO

import streamlit as st

# If you use the custom sidebar from earlier:
try:
    from utils_nav import render_sidebar
    USE_CUSTOM_SIDEBAR = True
except Exception:
    USE_CUSTOM_SIDEBAR = False

# ---------- CONFIG ----------
APP_TITLE = "GFR Physiology Simulator"
APP_TAGLINE = "Interactive learning platform for medical students"
APP_URL = "https://YOUR-DEPLOYED-APP-URL"   # <-- put your Streamlit Cloud URL here

PAGES = [
    ("pages/01_📘_GFR_Introduction.py", "📘 Introduction"),
    ("pages/02_📊_Parameter_Simulator.py", "📊 Parameter Simulator"),
    ("pages/03_🧠_Autoregulation.py", "🧠 Autoregulation"),
    ("pages/06_⚡_Quick_Scenarios.py", "⚡ Quick Scenarios"),
    ("pages/05_🧪_Cases_and_Worksheet.py", "🧪 Cases & Worksheet"),
    ("pages/04_📚_Videos_and_Slides.py", "📚 Videos & Slides"),
]

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Home — GFR Simulator", layout="wide")
if USE_CUSTOM_SIDEBAR:
    render_sidebar()

# ---------- QR CODE (clickable) ----------
def make_qr_bytes(url: str) -> bytes:
    # local import so app still runs if qrcode isn't installed yet
    import qrcode
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def qr_img_tag(url: str, width_px: int = 120) -> str:
    qr_bytes = make_qr_bytes(url)
    b64 = base64.b64encode(qr_bytes).decode("ascii")
    return f'<a href="{url}" target="_blank"><img src="data:image/png;base64,{b64}" width="{width_px}" style="border-radius:10px"/></a>'

# ---------- HEADER ----------
left, right = st.columns([3.5, 1])
with left:
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, #3a7bd5 0%, #4ca7ff 50%, #00d2ff 100%);
            border-radius: 14px; padding: 22px 26px; color: white;">
            <h1 style="margin:0; font-weight:800;">🫘 {APP_TITLE}</h1>
            <div style="opacity:0.95; font-size:16px; margin-top:6px;">{APP_TAGLINE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown(
        f"""
        <div style="text-align:center; padding-top:6px;">
            {qr_img_tag(APP_URL, 128)}
            <div style="font-size:12px; color:#666; margin-top:6px;">🔗 Click or Scan to open</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")  # small spacing
st.markdown("**Developed by Dr Sadia Fatima**")

# ---------- NAVIGATION SHORTCUTS ----------
st.markdown("### Navigate")
nav_cols = st.columns(3)
for i, (path, label) in enumerate(PAGES):
    col = nav_cols[i % 3]
    with col:
        try:
            # Works only if the file truly exists in /pages with that exact name.
            st.page_link(path, label=label, use_container_width=True)
        except Exception:
            # If a file is renamed/missing, show a non-breaking button that opens the app root.
            st.link_button(label, APP_URL, use_container_width=True)

st.divider()

# ---------- WELCOME / OVERVIEW ----------
c1, c2 = st.columns([1.3, 1])
with c1:
    st.markdown(
        """
        ### Welcome to GFR Physiology!
        This interactive simulator helps you understand **Glomerular Filtration Rate (GFR)** by exploring
        Starling forces, renal autoregulation, and clinical applications.

        **What you’ll learn:**
        - ✅ Starling forces and their effects on GFR  
        - ✅ Renal autoregulation mechanisms  
        - ✅ Clinical applications in real patient scenarios  
        - ✅ Hemodynamic parameter interactions
        """
    )
with c2:
    st.markdown("### Quick Stats")
    k1, k2, k3 = st.columns(3)
    k1.metric("Clinical Cases", "4")
    k2.metric("Scenarios", "7")
    k3.metric("Parameters", "6")
    st.caption("Jump into the tabs to start exploring!")

st.divider()

# ---------- LEARNING PATH ----------
st.markdown(
    """
    ### Suggested Learning Path
    1. **Introduction** → Review nephron basics & Starling forces  
    2. **Parameter Simulator** → Manipulate MAP, Ra, Re, Kf, Pbs, πgc and see effects  
    3. **Autoregulation** → See how kidneys stabilize GFR across MAP range  
    4. **Quick Scenarios** → Compare common clinical/pathologic patterns  
    5. **Cases & Worksheet** → Apply concepts to real-style clinical vignettes  
    6. **Videos & Slides** → Watch the lecture and download slides
    """
)

# ---------- REFERENCES ----------
st.divider()
st.markdown(
    """
    ### References (Textbooks)
    - **Guyton and Hall Textbook of Medical Physiology**, 14th ed.  
    - **Ganong's Review of Medical Physiology**, 26th ed.  
    - **Sherwood's Human Physiology: From Cells to Systems**, 10th ed.  
    """
)

# ---------- FOOTER HINT ----------
st.caption("Tip: use the left sidebar Pages menu or the buttons above to navigate.")

