import streamlit as st
from backend.Telemetrydashboard  import create_tele_dashboard
from backend.fastf1data import get_drivers, get_races
st.set_page_config(page_title="Early Apex Analytics", layout="wide")
#The titles
st.write("Welcome to Early Apex Analytics!")
st.title("*Telemetry Dashboard*")
year = st.selectbox("Year",list(range(2018,2026)))
#selecting the races
events= get_races(year)
events= st.selectbox("Race",events)
session = st.selectbox("Session", ["FP1", "FP2", "FP3", "SQ", "S", "Q", "R"])
#Selecting the drivers
drivers_inseason = get_drivers(year, events, session)
drivers = st.multiselect("Drivers", drivers_inseason)
# Now generating the buttons
if st.button("Generate Telemetry Dashboard"):
    if len(drivers) < 2:
        st.warning("Please select at least 2 drivers")
    else:
        with st.spinner("Loading FastF1 data for the early apex..."):
            fig = create_tele_dashboard(year,events,session,drivers)
        st.success("Apex hit!")
        st.plotly_chart(fig, use_container_width=True)

