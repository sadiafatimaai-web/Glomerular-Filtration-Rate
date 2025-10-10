import streamlit as st
from utils_nav import render_sidebar
import base64
from pathlib import Path
import os

st.set_page_config(page_title="GFR — Videos & Slides", layout="wide")
render_sidebar()

st.title("🎞️ GFR Videos & Slides")

# ---------------- 🎥 VIDEOS ---------------- #
st.markdown("### Lecture Videos")

VIDEO_URLS = [
    "https://www.youtube.com/watch?v=SVqSqPOcahY&t=1321s",
    "https://youtu.be/8Mn0IUCTg3U?si=k0_nwQowIMuMFKvY",
]

for i, url in enumerate(VIDEO_URLS, start=1):
    st.markdown(f"#### ▶️ Video {i}")
    st.video(url)
    st.markdown("---")

# ---------------- 📑 SLIDES ---------------- #
st.subheader("Slides")

def show_pdf(pdf_path: Path):
    """Embed and download PDF."""
    pdf_bytes = pdf_path.read_bytes()
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")

    st.download_button(
        "📥 Download slides (PDF)",
        data=pdf_bytes,
        file_name=pdf_path.name,
        mime="application/pdf",
        use_container_width=True,
    )

    st.markdown(
        f'<a href="data:application/pdf;base64,{b64}" target="_blank">🔗 Open in new tab</a>',
        unsafe_allow_html=True
    )

    st.markdown("#### Preview")
    st.markdown(
        f"""
        <iframe src="data:application/pdf;base64,{b64}" width="100%" height="700px"
                style="border:1px solid #e6e6e6;border-radius:8px;"></iframe>
        """,
        unsafe_allow_html=True,
    )

# Locate PDF (works even if name or case differs)
root = Path(".").resolve()
assets_dir = root / "assets"

candidates = []
if assets_dir.exists():
    candidates = list(assets_dir.glob("*.pdf"))
if not candidates:
    candidates = list(root.glob("*.pdf"))

if candidates:
    pdf_path = candidates[0]
    st.success(f"Loaded: **{pdf_path.relative_to(root)}**")
    show_pdf(pdf_path)
else:
    st.warning(
        "Slides not found. Make sure your file is located at `assets/GFR_slides.pdf` "
        "or another `.pdf` inside the `assets/` folder."
    )

    # Diagnostics to help troubleshoot
    with st.expander("🔍 Show diagnostics"):
        st.write("**Current working directory:**", str(root))
        st.write("**Assets folder exists:**", assets_dir.exists())
        if assets_dir.exists():
            st.write("**Files in assets/:**", [p.name for p in assets_dir.glob('*')])
        st.write("**Files in repo root:**", os.listdir(root))
