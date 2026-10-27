
import streamlit as st
import os

PAGES = [
    ("🏠 Home", "gfr_app.py"),
    ("📘 Introduction", "pages/01_📘_GFR_Introduction.py"),
    ("🎞️ Videos & Slides", "pages/04_🎞️_Videos_and_Slides.py"),
    ("🧮 Parameter Simulator", "pages/02_🧮_Parameter_Simulator.py"),
    ("🧠 Autoregulation", "pages/03_🧠_Autoregulation.py"),
    ("⚡ Quick Scenarios", "pages/06_⚡_Quick_Scenarios.py"),
    ("📝 Cases & Worksheet", "pages/05_📝_Cases_and_Worksheet.py"),
]


def render_sidebar():
    # Hide Streamlit's default navigation menu
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        section[data-testid="stSidebar"] {
            padding-top: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display our custom navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")

        for label, path in PAGES:
            if not os.path.exists(path):
                st.error(f"Missing file: {path}")
                continue

            if st.button(label, use_container_width=True):
                st.switch_page(path)

        st.markdown("---")
        st.caption(
            "Built with Streamlit. Content and code developed by "
            "Dr. Sadia Fatima with assistance from an AI coding/copilot (OpenAI)."
        )
    
