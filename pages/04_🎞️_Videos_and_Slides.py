import streamlit as st
from utils_nav import render_sidebar
from pathlib import Path

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="GFR — Videos & Slides", layout="wide")
render_sidebar()

# ---------------- HEADER ---------------- #
st.title("🎞️ GFR Videos & Slides")

# ---------------- VIDEOS ---------------- #
st.markdown("### 🎬 Lecture Videos")

col1, col2 = st.columns(2)  # Two videos side by side

with col1:
    st.video("https://www.youtube.com/watch?v=SVqSqPOcahY&t=1321s")
    st.markdown("<p style='text-align:center;'>Video 1: GFR Lecture Part 1</p>", unsafe_allow_html=True)

with col2:
    st.video("https://youtu.be/8Mn0IUCTg3U?si=k0_nwQowIMuMFKvY")
    st.markdown("<p style='text-align:center;'>Video 2: GFR Lecture Part 2</p>", unsafe_allow_html=True)

st.divider()
# Podcast
st.subheader("🎧 Podcast")
st.audio("assets/gfr_podcast.mp3")

# ---------------- SLIDES ---------------- #
st.subheader("📑 Lecture Slides")

# Define PDF path
pdf_path = Path("assets/GFR_slides.pdf")

if pdf_path.exists():
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()

    # Download button only (no inline preview)
    st.download_button(
        label="📥 Download GFR Slides (PDF)",
        data=pdf_data,
        file_name=pdf_path.name,
        mime="application/pdf",
        use_container_width=True
    )
else:
    st.warning("Slides not found at **assets/GFR_slides.pdf**. Please ensure the file exists.")
