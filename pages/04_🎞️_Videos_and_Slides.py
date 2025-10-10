import streamlit as st
from utils_nav import render_sidebar
import base64
from pathlib import Path

st.set_page_config(page_title="GFR — Videos & Slides", layout="wide")
render_sidebar()

st.title("🎞️ GFR Videos & Slides")

# ---- Videos (as before) ----
st.markdown("### Lecture Videos")
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=SVqSqPOcahY&t=1321s",
    "https://youtu.be/8Mn0IUCTg3U?si=k0_nwQowIMuMFKvY",
]
for i, url in enumerate(VIDEO_URLS, start=1):
    st.markdown(f"#### ▶️ Video {i}")
    st.video(url)
    st.markdown("---")

# ---- Slides (verify + embed) ----
st.subheader("Slides")

PDF_PATH = Path("assets/GFR_slides.pdf")  # <- single .pdf here

def embed_pdf(pdf_bytes: bytes, height: int = 700):
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    # Use <object> with <iframe> fallback for better browser compatibility
    st.markdown(
        f"""
        <object data="data:application/pdf;base64,{b64}" type="application/pdf" width="100%" height="{height}px">
            <iframe src="data:application/pdf;base64,{b64}" width="100%" height="{height}px">
                <p>Your browser can't display PDFs inline. Please use the download link above.</p>
            </iframe>
        </object>
        """,
        unsafe_allow_html=True,
    )

if PDF_PATH.exists():
    pdf_bytes = PDF_PATH.read_bytes()
    size_mb = len(pdf_bytes) / (1024 * 1024)
    st.success(f"Loaded: **{PDF_PATH}**  •  Size: {size_mb:.2f} MB")

    # Validate header
    if not pdf_bytes.startswith(b"%PDF-"):
        st.error(
            "This file does not look like a valid PDF (missing `%PDF-` header). "
            "Please re-export your slide deck as a real PDF and replace the file."
        )
    else:
        # Download + open in new tab
        st.download_button(
            "📥 Download slides (PDF)",
            data=pdf_bytes,
            file_name=PDF_PATH.name,
            mime="application/pdf",
            use_container_width=True,
        )
        b64 = base64.b64encode(pdf_bytes).decode("utf-8")
        st.markdown(
            f'<a href="data:application/pdf;base64,{b64}" target="_blank">🔗 Open in new tab</a>',
            unsafe_allow_html=True,
        )

        st.markdown("#### Preview")
        embed_pdf(pdf_bytes, height=700)
else:
    st.warning(
        "Slides not found at **assets/GFR_slides.pdf**. "
        "Ensure the file exists and has a single `.pdf` extension."
    )

        "or another `.pdf` inside the `assets/` folder."
    )

   
