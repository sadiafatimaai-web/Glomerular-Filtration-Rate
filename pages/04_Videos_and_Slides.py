# pages/04_Videos_and_Slides.py
import streamlit as st
from utils_nav import render_sidebar

st.set_page_config(page_title="GFR — Videos & Slides", layout="wide")
render_sidebar()

st.title("🎞️ Videos and Slides")

st.subheader("Lecture Videos")
st.video("https://www.youtube.com/watch?v=7J-5TtC1i5o")  # example; replace with your link

st.subheader("Slides")
st.markdown(
    "[Open Slides](https://docs.google.com/presentation/)  \n"
    "_Keep slides open while using the simulator for reference._"
)
