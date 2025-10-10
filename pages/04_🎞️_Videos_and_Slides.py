# pages/04_Videos_and_Slides.py
import streamlit as st
from utils_nav import render_sidebar
import base64
from pathlib import Path

st.set_page_config(page_title="GFR — Videos & Slides", layout="wide")
render_sidebar()

st.title("🎞️ GFR Videos & Slides")

# ─────────────── VIDEOS ─────────────── #
st.markdown("### 🎥 Lecture Videos")

VIDEO_URLS = [
    "https://www.youtube.com/watch?v=SVqSqPOcahY&t=1321s",
    "https://youtu.be/8Mn0IUCTg3U?si=k0_nwQowIMuMFKvY",
]

for i, url in enumerate(VIDEO_URLS, start=1):
    st.markdown(f"#### ▶️ Video {i}")
    st.video(url)
    st.markdown("---")

# ─────────────── PDF FROM assets/ ─────────────── #
st.subheader("📑 Slides")

PDF_PATH = Path("assets/GFR_slides.pdf")   # <-- change name here if needed

def render_pdf_inline(pdf_bytes: bytes, height: int = 700):
    """Embed a PDF in the page via base64 data URI."""
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    st.markdown(
        f"""
        <iframe
            src="data:application/pdf;base64,{b64}"
            width="100%"
            height="{height}px"
            style="border:1px solid #e6e6e6;border-radius:8px;"
        ></iframe>
        """,
        unsafe_allow_html=True,
    )

if PDF_PATH.exists():
    pdf_bytes = PDF_PATH.read_bytes()
    st.success(f"Loaded: **{PDF_PATH.name}** from **assets/**")

    # Download + open in new tab (data URL) options
    st.download_button(
        "📥 Download slides (PDF)",
        data=pdf_bytes,
        file_name=PDF_PATH.name,
        mime="application/pdf",
        use_container_width=True,
    )
    # Open in new tab (use a small base64 link)
    b64link = base64.b64encode(pdf_bytes).decode("utf-8")
    st.markdown(
        f'<a href="data:application/pdf;base64,{b64link}" target="_blank">🔗 Open in new tab</a>',
        unsafe_allow_html=True
    )

    st.markdown("#### Preview")
    render_pdf_inline(pdf_bytes, height=700)
else:
    st.warning(
        "Slides not found at **assets/GFR_slides.pdf**. "
        "Make sure the file exists, or update `PDF_PATH` in this page."
    )
