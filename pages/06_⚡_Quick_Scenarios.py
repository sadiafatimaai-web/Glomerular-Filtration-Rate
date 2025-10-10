# pages/06_Quick_Scenarios.py
import streamlit as st
import pandas as pd
from utils_nav import render_sidebar
from physiology import nfp, gfr

st.set_page_config(page_title="GFR — Quick Scenarios", layout="wide")
render_sidebar()

st.title("⚡ Quick Scenarios")

st.write("Explore preconfigured parameter sets and compare **GFR / RPF / FF** quickly.")

scenarios = [
    {"Scenario": "Normal", "MAP": 100, "Ra": 1.0, "Re": 2.0, "Pbs": 10, "Kf": 12.0, "πgc": 25},
    {"Scenario": "Increased Ra", "MAP": 100, "Ra": 2.5, "Re": 2.0, "Pbs": 10, "Kf": 12.0, "πgc": 25},
    {"Scenario": "Mild Re Increase", "MAP": 100, "Ra": 1.0, "Re": 3.5, "Pbs": 10, "Kf": 12.0, "πgc": 25},
    {"Scenario": "Severe Re Increase", "MAP": 100, "Ra": 1.0, "Re": 5.0, "Pbs": 10, "Kf": 12.0, "πgc": 25},
    {"Scenario": "Decreased Kf", "MAP": 100, "Ra": 1.0, "Re": 2.0, "Pbs": 10, "Kf": 6.0, "πgc": 25},
    {"Scenario": "Increased Bowman", "MAP": 100, "Ra": 1.0, "Re": 2.0, "Pbs": 25, "Kf": 12.0, "πgc": 25},
    {"Scenario": "Decreased MAP", "MAP": 70,  "Ra": 1.0, "Re": 2.0, "Pbs": 10, "Kf": 12.0, "πgc": 25},
]

def compute_row(row):
    # Very simple derived values to illustrate differences
    Pgc = min(110, 0.99*row["MAP"] * (row["Re"]/(row["Ra"]+row["Re"])) + 10)
    NFP = nfp(Pgc, row["Pbs"], row["πgc"], 0.0)
    GFR = gfr(row["Kf"], NFP)
    # keep RPF & FF illustrative only (not shown in table here)
    return GFR

df = pd.DataFrame(scenarios)
df["GFR (mL/min)"] = df.apply(compute_row, axis=1).round(1)

st.dataframe(df[["Scenario","MAP","Ra","Re","Pbs","Kf","GFR (mL/min)"]], use_container_width=True)

