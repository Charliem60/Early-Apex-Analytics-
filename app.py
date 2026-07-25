import streamlit as st
from backend.Telemetrydashboard  import create_tele_dashboard
st.title("*Early Apex Analytics*")
st.write("Welcome to Early Apex Analytics!")
st.title("*Telemetry Dashboard*")
year = st.selectbox("Year", [2018,2019,2020,2021,2022,2023,2024,2025,2026])
event = st.selectbox("Race",[ "Italian Grand Prix", "Spanish Grand Prix","Belgian Grand Prix"])
session = st.selectbox("Session", ["Q", "FP1", "R"])
drivers = st.multiselect("Drivers", ["VER", "HAM", "ALO"])
if st.button("Generate Telemetry Dashboard"):
    if len(drivers) < 2:
        st.warning("Please select at least 2 drivers")
    else:
        fig = create_tele_dashboard(year,event,session,drivers)
        st.plotly_chart(fig, use_container_width=True)

