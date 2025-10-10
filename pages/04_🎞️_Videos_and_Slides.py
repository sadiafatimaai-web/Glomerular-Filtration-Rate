# pages/04_Videos_and_Slides.py
import streamlit as st
from utils_nav import render_sidebar
import base64

st.set_page_config(page_title="GFR — Videos & Slides", layout="wide")
render_sidebar()

st.title("🎞️ GFR Videos & Slides")

# ─────────────── VIDEOS SECTION ─────────────── #
st.markdown("""
### 🎥 Lecture Videos
""")

VIDEO_URLS = [
    "https://www.youtube.com/watch?v=SVqSqPOcahY&t=1321s",
    "https://youtu.be/8Mn0IUCTg3U?si=k0_nwQowIMuMFKvY",
]

for i, url in enumerate(VIDEO_URLS, start=1):
    st.markdown(f"#### ▶️ Video {i}")
    st.video(url)
    st.markdown("---")

# ─────────────── PDF SLIDES (UPLOAD + EMBED) ─────────────── #
st.subheader("📑 Slides (Upload PDF)")

uploaded = st.file_uploader(
    "Upload a PDF of your slides", type=["pdf"], accept_multiple_files=False
)

def _pdf_viewer(pdf_bytes: bytes, height: int = 700):
    """
    Render a PDF inside the app using a base64 data URI.
    """
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_data_uri = f"data:application/pdf;base64,{b64}"
    st.markdown(
        f"""
        <iframe
            src="{pdf_data_uri}"
            width="100%"
            height="{height}px"
            style="border: 1px solid #e6e6e6; border-radius: 8px;"
        ></iframe>
        """,
        unsafe_allow_html=True,
    )

if uploaded is None:
    st.info("No PDF uploaded yet. Drag & drop your **.pdf** above to preview it here.")
else:
    pdf_bytes = uploaded.getvalue()
    st.success(f"Loaded: **{uploaded.name}**")
    # Download button
    st.download_button(
        "📥 Download this PDF",
        data=pdf_bytes,
        file_name=uploaded.name,
        mime="application/pdf",
        use_container_width=True,
    )
    st.markdown("#### Preview")
    _pdf_viewer(pdf_bytes, height=700)
