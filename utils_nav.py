# utils_nav.py
import streamlit as st
import os

# Page label and path pairs (ASCII paths to avoid OS issues)
PAGES = [
    ("🏠 Home", "gfr_app.py"),
    ("📘 Introduction", "pages/01_Intro.py"),
    ("🧮 Parameter Simulator", "pages/02_Parameter_Simulator.py"),
    ("🧠 Autoregulation", "pages/03_Autoregulation.py"),
    ("⚡ Quick Scenarios", "pages/06_Quick_Scenarios.py"),
    ("📝 Cases & Worksheet", "pages/05_Cases_and_Worksheet.py"),
    ("🎞️ Videos & Slides", "pages/04_Videos_and_Slides.py"),
]

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🧭 Navigation")

        # Buttons + switch_page (reliable on Streamlit Cloud)
        for label, path in PAGES:
            if not os.path.exists(path):
                # show once on missing file to help diagnose
                st.error(f"Missing file: {path}")
                continue
            if st.button(label, use_container_width=True):
                try:
                    st.switch_page(path)
                except Exception as e:
                    st.warning(
                        f"Could not open **{label}** at `{path}`.\n\n"
                        "Please use Streamlit’s Pages menu on the left."
                    )

        st.markdown("---")
        st.caption("Developed by **Dr Sadia Fatima**")
