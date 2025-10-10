# gfr_app.py  — Landing page (no extra Navigate section)
import base64
from io import BytesIO
import streamlit as st

# Optional: if you’re using the custom sidebar component
try:
    from utils_nav import render_sidebar
    USE_CUSTOM_SIDEBAR = True
except Exception:
    USE_CUSTOM_SIDEBAR = False

# ------------ CONFIG ------------
APP_TITLE = "GFR Physiology Simulator"
APP_TAGLINE = "Interactive learning platform for medical students"

# ⬇️ IMPORTANT: put your deployed URL here (e.g., "https://your-app.streamlit.app")
APP_URL = "https://gfr-physiology-simulator.streamlit.app"


st.set_page_config(page_title="Home — GFR Simulator", layout="wide")
if USE_CUSTOM_SIDEBAR:
    render_sidebar()

# ----- QR utilities -----
def _make_qr_png_bytes(url: str) -> bytes:
    import qrcode
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def _qr_img_tag(url: str, width_px: int = 128) -> str:
    qr_bytes = _make_qr_png_bytes(url)
    b64 = base64.b64encode(qr_bytes).decode("ascii")
    return f'<a href="{url}" target="_blank"><img src="data:image/png;base64,{b64}" width="{width_px}" style="border-radius:10px"/></a>'

# ------------ HEADER ------------
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
    if APP_URL and "YOUR-DEPLOYED-APP-URL" not in APP_URL:
        st.markdown(
            f"""
            <div style="text-align:center; padding-top:6px;">
                {_qr_img_tag(APP_URL, 128)}
                <div style="font-size:12px; color:#666; margin-top:6px;">🔗 Click or Scan</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Add your deployed URL in `APP_URL` to show a clickable QR.")

st.write("")
st.markdown("**Developed by Dr Sadia Fatima**")

# ------------ OVERVIEW + QUICK STATS ------------
c1, c2 = st.columns([1.3, 1])
with c1:
    st.markdown(
        """
        ### Welcome to GFR Physiology!
        This interactive simulator helps you understand **Glomerular Filtration Rate (GFR)** by exploring
        Starling forces, renal autoregulation, and clinical applications.

        **What you’ll learn**
        - ✅ Starling forces and their effects on GFR  
        - ✅ Renal autoregulation mechanisms  
        - ✅ Clinical applications in patient scenarios  
        - ✅ Hemodynamic parameter interactions
        """
    )
with c2:
    st.markdown("### Quick Stats")
    k1, k2, k3 = st.columns(3)
    k1.metric("Clinical Cases", "4")
    k2.metric("Scenarios", "7")
    k3.metric("Parameters", "6")
    if APP_URL and "YOUR-DEPLOYED-APP-URL" not in APP_URL:
        st.link_button("Open app in new tab", APP_URL, use_container_width=True)

st.divider()

# ------------ LEARNING PATH ------------
st.markdown(
    """
    ### Suggested Learning Path
    1. **Introduction** → Nephron basics & Starling forces  
    2. **Parameter Simulator** → Manipulate MAP, Ra, Re, Kf, Pbs, πgc  
    3. **Autoregulation** → How kidneys stabilize GFR across MAP  
    4. **Quick Scenarios** → Compare common clinical/pathologic patterns  
    5. **Cases & Worksheet** → Apply concepts to clinical vignettes  
    6. **Videos & Slides** → Watch the lecture and download slides
    """
)

# ------------ REFERENCES ------------
st.divider()
st.markdown(
    """
    ### References (Textbooks)
    - **Guyton and Hall Textbook of Medical Physiology**, 14th ed.  
    - **Ganong's Review of Medical Physiology**, 26th ed.  
    - **Sherwood's Human Physiology: From Cells to Systems**, 10th ed.  
    """
)

st.caption("Use the left sidebar (Pages) to navigate.")


