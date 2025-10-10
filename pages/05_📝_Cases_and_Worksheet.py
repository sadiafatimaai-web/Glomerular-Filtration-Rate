# pages/05_Cases_and_Worksheet.py
import streamlit as st
import pandas as pd
from utils_nav import render_sidebar

st.set_page_config(page_title="GFR — Cases & Worksheet", layout="wide")
render_sidebar()

st.title("📝 Cases & Worksheet")

case = st.selectbox(
    "Select a clinical case:",
    ["Case 1: Acute Hemorrhage", "Case 2: Post-renal Obstruction", "Case 3: Dehydration"]
)

st.subheader(case)
st.write("Patient presentation and data:")

if case == "Case 1: Acute Hemorrhage":
    labs = pd.DataFrame(
        {"Parameter": ["Hematocrit", "Creatinine", "BUN", "Urine output"],
         "Value": ["28%", "1.8 mg/dL (baseline 1.0)", "45 mg/dL", "15 mL/hr"]}
    )
    vitals = pd.DataFrame(
        {"Parameter": ["BP", "HR", "Temp", "SpO2"],
         "Value": ["85/50 mmHg", "120 bpm", "36.8°C", "94% RA"]}
    )
elif case == "Case 2: Post-renal Obstruction":
    labs = pd.DataFrame(
        {"Parameter": ["Hematocrit", "Creatinine", "BUN", "Urine output"],
         "Value": ["40%", "2.2 mg/dL", "30 mg/dL", "Low, dribbling"]}
    )
    vitals = pd.DataFrame(
        {"Parameter": ["BP", "HR", "Temp", "SpO2"],
         "Value": ["130/80 mmHg", "88 bpm", "36.7°C", "98% RA"]}
    )
else:
    labs = pd.DataFrame(
        {"Parameter": ["Hematocrit", "Creatinine", "BUN", "Urine osmolality"],
         "Value": ["52%", "1.3 mg/dL", "24 mg/dL", "High"]}
    )
    vitals = pd.DataFrame(
        {"Parameter": ["BP", "HR", "Temp", "SpO2"],
         "Value": ["100/65 mmHg", "96 bpm", "37.0°C", "98% RA"]}
    )

c1, c2 = st.columns(2)
with c1:
    st.write("**Laboratory Values**")
    st.dataframe(labs, use_container_width=True)
with c2:
    st.write("**Vital Signs**")
    st.dataframe(vitals, use_container_width=True)

st.divider()
st.subheader("Interactive Questions")
st.write("What is the primary mechanism causing the GFR change in this case?")
st.radio("Select your answer:", [
    "Increased afferent arteriolar resistance",
    "Decreased glomerular capillary pressure due to hypotension",
    "Increased Bowman’s capsule pressure",
    "Decreased ultrafiltration coefficient",
], index=None)

st.write("Which compensatory mechanism is likely activated?")
st.radio("Choose one:", [
    "Tubuloglomerular feedback inhibition",
    "Myogenic autoregulation",
    "Sympathetic nervous system activation",
    "Prostaglandin-mediated vasodilation",
], index=None)

