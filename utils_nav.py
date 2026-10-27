# utils_nav.py  (replace with this)
import streamlit as st
import os

# 👉 Edit these paths to match your actual filenames
PAGES = [
    ("🏠 Home", "gfr_app.py"),
    # If your file is emoji-named, use the emoji path on the next line:
    ("📘 Introduction", "pages/01_📘_GFR_Introduction.py"),
    ("🎞️ Videos & Slides", "pages/04_🎞️_Videos_and_Slides.py"),
    ("🧮 Parameter Simulator", "pages/02_🧮_Parameter_Simulator.py"),
    ("🧠 Autoregulation", "pages/03_🧠_Autoregulation.py"),
    ("⚡ Quick Scenarios", "pages/06_⚡_Quick_Scenarios.py"),
    ("📝 Cases & Worksheet", "pages/05_📝_Cases_and_Worksheet.py"),
   ]

def render_sidebar():
  st.markdown(
    """
    <style>
    /* Hide Streamlit's built-in navigation */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Keep the custom sidebar neat */
    section[data-testid="stSidebar"] {
        padding-top: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

    with st.sidebar:
        st.markdown("### 🧭 Navigation")

        # Our custom buttons + switch_page (robust on Cloud)
        for label, path in PAGES:
            if not os.path.exists(path):
                st.error(f"Missing file: {path}")
                continue
            if st.button(label, use_container_width=True):
                try:
                    st.switch_page(path)
                except Exception:
                    st.warning(
                        f"Could not open **{label}** at `{path}`. "
                        "Use the sidebar’s Pages menu if visible."
                    )

        st.markdown("---")
        st.caption("Built with Streamlit. Content and code developed by Dr. Sadia Fatima with assistance from an AI coding/copilot (OpenAI)")
