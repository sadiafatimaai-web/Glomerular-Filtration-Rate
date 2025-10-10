# utils_nav.py
import streamlit as st

# Adjust labels/paths if you rename files
PAGES = [
    ("🏠 Home", "gfr_app.py"),
    ("📘 Introduction", "pages/01_📘_GFR_Introduction.py"),
    ("🧮 Parameter Simulator", "pages/02_🧮_Parameter_Simulator.py"),
    ("🧠 Autoregulation", "pages/03_🧠_Autoregulation.py"),
    ("⚡ Quick Scenarios", "pages/06_⚡_Quick_Scenarios.py"),
    ("📝 Cases & Worksheet", "pages/05_📝_Cases_and_Worksheet.py"),
    ("🎞️ Videos & Slides", "pages/04_🎞️_Videos_and_Slides.py"),
]

def _has(attr: str) -> bool:
    return hasattr(st, attr)

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        st.caption(f"Streamlit version: **{st.__version__}**")

        # Preferred: Streamlit ≥ 1.26 supports page_link
        if _has("page_link"):
            for label, path in PAGES:
                st.page_link(path, label=label)
            st.markdown("---")
            st.caption("Developed by **Dr Sadia Fatima** • October 2025")
            return

        # Fallback A: radio + switch_page (Streamlit ≥ 1.22)
        labels = [lbl for lbl, _ in PAGES]
        choice = st.radio("Go to:", labels, label_visibility="collapsed")
        target_path = dict(PAGES)[choice]

        if _has("switch_page"):
            if st.button("Go", use_container_width=True):
                st.switch_page(target_path)
        else:
            # Fallback B: show clickable Markdown links (older versions)
            st.warning(
                "Your Streamlit is older, so instant switching isn't available. "
                "Use the default Pages menu or click a link below."
            )
            for label, path in PAGES:
                st.markdown(f"- [{label}]({path})")

        st.markdown("---")
        st.caption("Developed by **Dr Sadia Fatima** • October 2025")


