# pages/04_Videos_and_Slides.py
import streamlit as st
from utils_nav import render_sidebar
import base64
from pathlib import Path
import os

st.set_page_config(page_title="GFR — Videos & Slides", layout="wide")
render_sidebar()

st.title("🎞️ GFR Videos & Slides")

# ---------------- Videos ---------------- #
st.markdown("### 🎥 Lecture Videos")
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=SVqSqPOcahY&t=1321s",
    "https://youtu.be/8Mn0IUCTg3U?si=k0_nwQowIMuMFKvY",
]
for i, url in enumerate(VIDEO_URLS, start=1):
    st.markdown(f"#### ▶️ Video {i}")
    st.video(url)
    st.markdown("---")

# ---------------- Slides (auto-detect) ---------------- #
st.subheader("📑 Slides")

def _pdf_iframe(pdf_bytes: bytes, height: int = 700):
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    st.markdown(
        f"""
        <iframe src="data:application/pdf;base64,{b64}"
                width="100%" height="{height}px"
                style="border:1px solid #e6e6e6;border-radius:8px;"></iframe>
        """,
        unsafe_allow_html=True,
    )

root = Path(".").resolve()
assets = root / "assets"

# Try common locations in order:
candidates = [
    assets / "GFR_slides.pdf",                   # your intended path
    assets / "gfr_slides.pdf",                   # case variation
    *sorted(assets.glob("*.pdf")) if assets.exists() else [],  # any pdf in assets/
    root / "GFR_slides.pdf",                     # if placed at repo root
    *sorted(root.glob("*.pdf")),                 # any pdf at root (fallback)
]

chosen = next((p for p in candidates if p.exists()), None)

if chosen:
    pdf_bytes = chosen.read_bytes()
    st.success(f"Loaded: **{chosen.relative_to(root)}**")
    st.download_button("📥 Download slides (PDF)", pdf_bytes, file_name=chosen.name,
                       mime="application/pdf", use_container_width=True)
    st.markdown("#### Preview")
    _pdf_iframe(pdf_bytes, height=700)
else:
    st.warning(
        "Slides not found. I looked for:\n\n"
        "- `assets/GFR_slides.pdf`\n"
        "- any `*.pdf` inside `assets/`\n"
        "- `GFR_slides.pdf` in the repo root\n"
        "\nAdd your PDF to **assets/** (e.g., `assets/GFR_slides.pdf`) and rerun."
    )

    # --- Diagnostics to help you see what's deployed ---
    with st.expander("Show diagnostics"):
        st.write("**Working directory:**", str(root))
        st.write("**Exists assets/**:", assets.exists())
        st.write("**Files in assets/**:", [p.name for p in assets.glob("*")] if assets.exists() else "assets/ missing")
        st.write("**Files in repo root:**", os.listdir(root))
