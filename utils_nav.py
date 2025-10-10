# utils_nav.py
from __future__ import annotations
import streamlit as st
from pathlib import Path

# Point to your actual page files (these labels appear on the buttons)
PAGE_LINKS = [
    ("gfr_app.py", "🏠 Home"),
    ("pages/01_📘_GFR_Introduction.py", "📘 Introduction"),
    ("pages/02_📊_Parameter_Simulator.py", "📊 Parameter Simulator"),
    ("pages/03_🧠_Autoregulation.py", "🧠 Autoregulation"),
    ("pages/06_⚡_Quick_Scenarios.py", "⚡ Quick Scenarios"),
    ("pages/05_🧪_Cases_and_Worksheet.py", "🧪 Cases & Worksheet"),
    ("pages/04_📚_Videos_and_Slides.py", "📚 Videos & Slides"),
]

def _file_exists(p: str) -> bool:
    # Works whether running from repo root or Streamlit's tmp runner
    try:
        return Path(p).exists()
    except Exception:
        return False

def render_sidebar():
    sb = st.sidebar
    sb.markdown("### 🧭 Navigation")

    # Navigation buttons (use page_link when file exists; otherwise fall back to no-op)
    for path, label in PAGE_LINKS:
        if _file_exists(path):
            sb.page_link(path, label=label, use_container_width=True)
        else:
            # Render a disabled-looking button if file missing (prevents KeyErrors)
            sb.button(label, disabled=True, use_container_width=True)

    sb.divider()

    # ---------- Acknowledgements box (footer) ----------
    sb.markdown(
        """
        <div style="
            font-size:12.5px;
            color:#334155;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 10px 12px;">
            <div style="font-weight:600; margin-bottom:4px;">Acknowledgements</div>
            <div style="line-height:1.35;">
                • Educational videos and figures inspired by <b>Ninja Nerd</b> and <b>Armando Hasudungan</b> (YouTube).<br/>
                • Built with <b>Streamlit</b>. Content and code developed by Dr. Sadia Fatima with assistance from an AI coding/copilot (OpenAI).
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
