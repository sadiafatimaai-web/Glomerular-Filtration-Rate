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

# ───────────────────────────────────────────────
# 🎧 Podcast Section
# ───────────────────────────────────────────────
st.divider()
st.subheader("🎧 Podcast — Understanding GFR Regulation")

from pathlib import Path

podcast_files = [
    Path("assets/gfr_podcast.wav"),
    Path("assets/gfr_podcast.m4a"),
]
podcast_file = next((p for p in podcast_files if p.exists()), None)

if podcast_file:
    with open(podcast_file, "rb") as f:
        ext = podcast_file.suffix.lower()
        audio_format = "audio/wav" if ext == ".wav" else "audio/mp4"
        st.audio(f.read(), format=audio_format)
    st.caption("Listen to this short podcast explaining GFR regulation and Starling forces.")
else:
    st.warning("Podcast file not found in assets/. Please ensure 'gfr_podcast.wav' or 'gfr_podcast.m4a' is uploaded.")


# ───────────────────────────────────────────────
# 🧠 Mind Map Section
# ───────────────────────────────────────────────
st.divider()
st.subheader("🧠 Mind Map — Conceptual Overview of GFR")

mindmap_path = Path("assets/NotebookLM Mind Map-GFR.png")

if mindmap_path.exists():
    st.image(mindmap_path, caption="NotebookLM: Conceptual Mind Map of GFR Regulation", use_container_width=True)
    st.caption("This visual integrates Starling forces, autoregulation, and clinical implications of GFR.")
else:
    st.warning("Mind map image not found in assets/. Please ensure 'NotebookLM Mind Map-GFR.png' is uploaded.")


st.divider()

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
