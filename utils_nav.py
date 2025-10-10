import streamlit as st
import os

# Page label and path pairs (ASCII paths to avoid OS issues)
# 👉 Edit these paths to match your actual filenames
PAGES = [
    ("🏠 Home", "gfr_app.py"),
    ("📘 Introduction", "pages/01_Intro.py"),
    ("🧮 Parameter Simulator", "pages/02_Parameter_Simulator.py"),
    ("🧠 Autoregulation", "pages/03_Autoregulation.py"),
    ("⚡ Quick Scenarios", "pages/06_Quick_Scenarios.py"),
    ("📝 Cases & Worksheet", "pages/05_Cases_and_Worksheet.py"),
    ("🎞️ Videos & Slides", "pages/04_Videos_and_Slides.py"),
    # If your file is emoji-named, use the emoji path on the next line:
    ("📘 Introduction", "pages/01_📘_GFR_Introduction.py"),
    ("🧮 Parameter Simulator", "pages/02_🧮_Parameter_Simulator.py"),
    ("🧠 Autoregulation", "pages/03_🧠_Autoregulation.py"),
    ("⚡ Quick Scenarios", "pages/06_⚡_Quick_Scenarios.py"),
    ("📝 Cases & Worksheet", "pages/05_📝_Cases_and_Worksheet.py"),
    ("🎞️ Videos & Slides", "pages/04_🎞️_Videos_and_Slides.py"),
]

def render_sidebar():
    # 🔒 Hide Streamlit's default "Pages" section
    st.markdown(
        """
        <style>
        /* Hide default Pages list */
        div[data-testid="stSidebarNav"] { display: none !important; }
        /* tighten spacing a bit */
        section[data-testid="stSidebar"] { padding-top: 0.5rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### 🧭 Navigation")

        # Buttons + switch_page (reliable on Streamlit Cloud)
        # Our custom buttons + switch_page (robust on Cloud)
        for label, path in PAGES:
            if not os.path.exists(path):
                # show once on missing file to help diagnose
                st.error(f"Missing file: {path}")
                continue
            if st.button(label, use_container_width=True):
                try:
                    st.switch_page(path)
                except Exception as e:
                except Exception:
                    st.warning(
                        f"Could not open **{label}** at `{path}`.\n\n"
                        "Please use Streamlit’s Pages menu on the left."
                        f"Could not open **{label}** at `{path}`. "
                        "Use the sidebar’s Pages menu if visible."
                    )

        st.markdown("---")
