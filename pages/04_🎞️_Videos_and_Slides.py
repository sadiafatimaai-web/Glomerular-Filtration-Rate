# pages/04_Videos_and_Slides.py
import streamlit as st
from utils_nav import render_sidebar

st.set_page_config(page_title="GFR — Videos & Slides", layout="wide")
render_sidebar()

st.title("🎞️ Videos and Slides")

# ── Paste your links here ─────────────────────────────────────────────
# Example formats (leave as None until you have them):
VIDEO_URLS = [
    # "https://www.youtube.com/watch?v=SVqSqPOcahY&t=1321s",
    # "https://youtu.be/8Mn0IUCTg3U?si=k0_nwQowIMuMFKvY",
]
SLIDES_URL = None  # e.g., "https://docs.google.com/presentation/d/XXXXXXXX"
# ─────────────────────────────────────────────────────────────────────

st.subheader("Lecture Videos")
if VIDEO_URLS:
    for i, url in enumerate(VIDEO_URLS, start=1):
        st.markdown(f"**Video {i}**")
        st.video(url)
        st.markdown("---")
else:
    st.info("No videos added yet. Share your video link(s) with me and I’ll insert them here.")

st.subheader("Slides")
if SLIDES_URL:
    st.markdown(f"[Open Slides]({SLIDES_URL})")
    st.caption("Tip: keep the slides open while using the simulator for reference.")
else:
    st.info("No slide deck added yet. Send me your slide link and I’ll add it.")
