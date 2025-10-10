# utils_nav.py
from pathlib import Path
import streamlit as st

# Hide Streamlit's built-in Pages menu so we only show our custom nav
st.sidebar.markdown(
    """
    <style>
      /* Hide the default multipage sidebar block */
      div[data-testid="stSidebarNav"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

PAGE_LINKS = [
    ("gfr_app.py", "🏠 Home"),
    ("pages/01_📘_GFR_Introduction.py", "📘 Introduction"),
    ("pages/02_📊_Parameter_Simulator.py", "📊 Parameter Simulator"),
    ("pages/03_🧠_Autoregulation.py", "🧠 Autoregulation"),
    ("pages/06_⚡_Quick_Scenarios.py", "⚡ Quick Scenarios"),
    ("pages/05_🧪_Cases_and_Worksheet.py", "🧪 Cases & Worksheet"),
    ("pages/04_📚_Videos_and_Slides.py", "📚 Videos & Slides"),
]

def _exists(p: str) -> bool:
    try:
        return Path(p).exists()
    except Exception:
        return False

def render_sidebar():
    sb = st.sidebar
    sb.markdown("### 🧭 Navigation")

    for path, label in PAGE_LINKS:
        if _exists(path):
            sb.page_link(path, label=label, use_container_width=True)
        else:
            sb.button(label, disabled=True, use_container_width=True)

    sb.divider()
    # Acknowledgements (edited per your request—no Ninja Nerd/Armando line)
    sb.markdown(
        """
        <div style="
            font-size:12.5px;
            color:#334155;
            background:#f1f5f9;
            border:1px solid #e2e8f0;
            border-radius:10px;
            padding:10px 12px;">
          <div style="font-weight:600; margin-bottom:4px;">Acknowledgements</div>
          <div style="line-height:1.35;">
            • Built with <b>Streamlit</b>. Content and code developed by Dr. Sadia Fatima with assistance from an AI coding/copilot (OpenAI).
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

