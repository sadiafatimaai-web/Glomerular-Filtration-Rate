# utils_nav.py
import streamlit as st
import os

# Update labels/paths if you renamed files differently
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
        st.caption(f"Streamlit {st.__version__}")

        # Show a button for each page and verify the target exists
        for label, path in PAGES:
            if not os.path.exists(path):
                st.error(f"Missing: {path}")
                continue

            if st.button(label, use_container_width=True):
                try:
                    # Works on Streamlit Cloud when pages/ is in place
                    st.switch_page(path)
                except Exception as e:
                    st.warning(
                        f"Could not switch to **{label}**.\n"
                        f"Path: `{path}`\nError: {e}\n\n"
                        "Open it from Streamlit's default Pages menu for now."
                    )

        st.markdown("---")
        st.caption("Developed by **Dr Sadia Fatima** • October 2025")


        st.markdown("---")
        st.caption("Developed by **Dr Sadia Fatima** • October 2025")


