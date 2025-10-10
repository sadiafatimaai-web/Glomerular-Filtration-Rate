# utils_nav.py
import streamlit as st

PAGES = [
    ("gfr_app.py", "🏠 Home"),
    ("pages/01_📘_GFR_Introduction.py", "📘 Introduction"),
    ("pages/02_🧮_Parameter_Simulator.py", "🧮 Parameter Simulator"),
    ("pages/03_🧠_Autoregulation.py", "🧠 Autoregulation"),
    ("pages/06_⚡_Quick_Scenarios.py", "⚡ Quick Scenarios"),
    ("pages/05_📝_Cases_and_Worksheet.py", "📝 Cases & Worksheet"),
    ("pages/04_🎞️_Videos_and_Slides.py", "🎞️ Videos & Slides"),
]

def render_sidebar():
    """Left-side, clickable navigation that actually switches pages."""
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        # Try modern API: st.page_link (if available)
        used_page_link = False
        try:
            # Streamlit >= 1.25 has st.page_link
            for path, label in PAGES:
                st.page_link(path, label=label)
            used_page_link = True
        except Exception:
            used_page_link = False

        # Fallback: Buttons + st.switch_page
        if not used_page_link:
            for path, label in PAGES:
                if st.button(label, use_container_width=True):
                    try:
                        st.switch_page(path)
                    except Exception:
                        # Last resort: tell user which file to open if running old Streamlit
                        st.warning(f"Please open **{path}** from the sidebar Pages menu.")

        st.markdown("---")
        st.caption("Developed by **Dr Sadia Fatima** • October 2025")
