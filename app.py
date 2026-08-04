import os
import streamlit as st
import fastf1
# Create FastF1 cache
cache_app = "cache"

if not os.path.exists(cache_app):
    os.makedirs(cache_app)
fastf1.Cache.enable_cache(cache_app)  # Enable caching for FastF1 data
from backend.fastf1data import get_races, get_drivers
from backend.Driveranalysis import create_driver_lap_data
from backend.Quali import create_quali_plots
from backend.Championship import create_championship_plots
from backend.Race import create_race_traces
from backend.Telemetryanalysis import create_track_visuals
from backend.Telemetrydashboard import create_tele_dashboard
from backend.TrackMap import create_track_map
from backend.Weather import create_weather_dashboard
# -----------------------------------
# Page configuration
# -----------------------------------
st.set_page_config(
    page_title="Early Apex Analytics",
    page_icon="🏎️",
    layout="wide"
)
# Custom UI
import streamlit as st

st.set_page_config(
    page_title="F1 Dashboard",
    page_icon="🏎️",
    layout="wide"
)

# 
# Custom Yellow + Black Theme CSS
# 

st.markdown("""
<style>


[data-testid="stAppViewContainer"] {
    background-color: #FFF4B8;
}

[data-testid="stHeader"] {
    background-color: #FFF4B8;
}



[data-testid="stAppViewContainer"] * {
    color: #000000 !important;
}

/* Number input */
div[data-testid="stNumberInput"] input {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}


/* Select boxes */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}


/* Dropdown selected text */
div[data-baseweb="select"] span {
    color: #000000 !important;
}


/* Multiselect */
div[data-baseweb="select"] input {
    color: #000000 !important;
}


.stButton > button {
    background-color: #000000 !important;
    color: #FFD700 !important;
    border-radius: 10px;
    border: 2px solid #000000;
    font-weight: bold;
}


.stButton > button p {
    color: #FFD700 !important;
}


.stButton > button:hover {
    background-color: #FFD700 !important;
}


.stButton > button:hover p {
    color: #000000 !important;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 2px solid black;
    border-radius: 12px;
}


[data-testid="stSidebar"] {
    background-color: #000000;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["🏎️ F1 Dashboard", "📊 Qualifying Analysis", "🌦️ Weather Analysis", "📊 Race Analysis", "Driver Analysis", "Lap Analysis", "Championship Standings", "Telemetry Dashboard" ])
with tab1:
    st.title("🏎️ Early Apex Analytics")
    st.write("Welcome to Early Apex Analytics! Explore F1 data, analyze race performance, telemetry, weather, championship trends and more." \
    "Use the tabs above to navigate through different sections of the dashboard.")
################################
#Quali Page
################################
with tab2:
    st.header("Qualifying Analysis")
    st.write("Use this section to analyze qualifying sessions for a selected race, such as ideal vs actual lap times, sector performance, and more.")
    quali_year = st.number_input("Season", min_value=2018, max_value=2026, value=2026, key="quali_year")
    quali_races= get_races(quali_year)
    quali_race = st.selectbox("Race", quali_races, key="quali_race")
    quali_drivers = get_drivers(quali_year, quali_race,"Q")
    #Generating
    if st.button("Generate Qualifying Analysis", key="quali_analysis_button"):
        with st.spinner("Generating qualifying analysis..."):
            quali_fig, quali_fig1, quali_fig2, quali_fig3 = create_quali_plots(
            quali_year,
            quali_race,
            "Q",
            quali_drivers
            )

        st.pyplot(quali_fig)
        st.pyplot(quali_fig1)
        st.pyplot(quali_fig2)
        st.pyplot(quali_fig3)

    #######################################
    # Weather Dashboard
    #######################################
with tab3:
    st.header("Weather Dashboard")
    st.write("Use this section to analyze weather conditions for a selected race and session, including temperature, humidity, wind speed, and more.")
    weather_year = st.number_input("Season", min_value=2018, max_value=2026, value=2026, key="weather_year")
    weather_race = st.selectbox("Race", get_races(weather_year), key="weather_race")
    weather_session = st.selectbox("Session", ["FP1", "FP2", "FP3", "SQ", "S", "Q","R",], key="weather_session")
    if st.button("Generate Weather Dashboard"):
        with st.spinner("Generating weather dashboard..."):
            weather_fig = create_weather_dashboard(weather_year,weather_race,weather_session)
        st.plotly_chart(weather_fig, use_container_width=True)
#######################################
#RACE Charts
#######################################
with tab4:
    st.header("Race Charts and Analysis")
    st.write("Use this section to analyze a race including position changes, strategy, and other key metrics.")
    race_year = st.number_input("Season", min_value=2018, max_value=2026, value=2026, key="race_year")
    race_race = st.selectbox("Race", get_races(race_year), key="race_race")
    race_session = "R"
    if st.button("Generate Race Charts", key="race_charts_button"):
        with st.spinner("Generating race charts..."):
            race_fig1, race_fig2, race_fig3, race_fig4 = create_race_traces(race_year, race_race, race_session)
        st.pyplot(race_fig1, use_container_width=True)
        st.pyplot(race_fig2, use_container_width=True)
        st.pyplot(race_fig3, use_container_width=True)
        st.pyplot(race_fig4, use_container_width=True)

#######################################
# DRIVER CHARTS
######################################
with tab5:
    st.header("Driver Charts and Analysis")
    st.write("Use this section to compare drivers over the course of race stints and other metrics.")
    driver_year = st.number_input("Season", min_value=2018, max_value=2026, value=2026, key="driver_year")
    driver_race = st.selectbox("Race", get_races(driver_year), key="driver_race")
    driver_session = st.selectbox("Session", ["FP1", "FP2", "FP3", "SQ", "S", "Q","R",], key="driver_session")
    driver_drivers = get_drivers(driver_year, driver_race, driver_session)
    selected_driver_drivers = st.multiselect("Select drivers", driver_drivers, key="selected_driver_drivers")   
    if st.button("Generate Charts", key="driver_charts_button"):
        with st.spinner("Generating driver charts..."):
            driver_fig1, driver_fig2 = create_driver_lap_data(driver_year, driver_race, driver_session, selected_driver_drivers)
        st.pyplot(driver_fig1, use_container_width=True)
        st.pyplot(driver_fig2, use_container_width=True)
#######################################
# Telemetry Graphics
######################################
with tab6:
    st.header("Telemetry Graphics")
    st.write("Use this section to visualize telemetry data for selected drivers and sessions.")
    telemetry_year = st.number_input("Season", min_value=2018, max_value=2026, value=2026, key="telemetry_year")
    telemetry_race = st.selectbox("Race", get_races(telemetry_year), key="telemetry_race")
    telemetry_session = st.selectbox("Session", ["FP1", "FP2", "FP3", "SQ", "S", "Q","R",], key="telemetry_session")
    telemetry_drivers = get_drivers(telemetry_year, telemetry_race, telemetry_session)
    selected_telemetry_drivers = st.multiselect("Select drivers", telemetry_drivers, key="selected_telemetry_drivers")   
    if st.button("Generate Charts", key="telemetry_charts_button"):
        with st.spinner("Generating telemetry charts..."):
            telemetry_fig1, telemetry_fig2 = create_track_visuals(telemetry_year, telemetry_race, telemetry_session, selected_telemetry_drivers)
        st.pyplot(telemetry_fig1, use_container_width=True)
        st.pyplot(telemetry_fig2, use_container_width=True)

#######################################
# Championship Standings
######################################
with tab7:
    st.header("Championship Standings")
    st.write("Use this section to view the championship standings for a selected season and round.")
    champ_year = st.number_input("Season", min_value=2018, max_value=2026, value=2026, key="champ_year")
    champ_round = st.number_input("Round", min_value=1, max_value=23, value=1, key="champ_round")
    if st.button("Generate Championship Standings", key="champ_standings_button"):
        with st.spinner("Generating championship standings..."):
            champ_fig1, champ_fig2, champ_fig3 = create_championship_plots(champ_year, champ_round)
        st.pyplot(champ_fig1)
        st.plotly_chart(champ_fig2, use_container_width=True)
        st.plotly_chart(champ_fig3, use_container_width=True)
#######################################
# Telemetry Dashboard
######################################
with tab8:
    st.header("Telemetry Dashboard")
    st.write("Use this section to visualize telemetry data for selected drivers and sessions in a dashboard format.")
    tele_dash_year = st.number_input("Season", min_value=2018, max_value=2026, value=2026, key="tele_dash_year")
    tele_dash_race = st.selectbox("Race", get_races(tele_dash_year), key="tele_dash_race")
    tele_dash_session = st.selectbox("Session", ["FP1", "FP2", "FP3", "SQ", "S", "Q","R",], key="tele_dash_session")
    tele_dash_drivers = get_drivers(tele_dash_year, tele_dash_race, tele_dash_session)
    selected_tele_dash_drivers = st.multiselect("Select drivers", tele_dash_drivers, key="selected_tele_dash_drivers") 
    if st.button("Generate Telemetry Dashboard", key="tele_dash_button"):
          with st.spinner("Generating telemetry dashboard..."):
                tele_dash_fig = create_tele_dashboard(tele_dash_year, tele_dash_race, tele_dash_session, selected_tele_dash_drivers)
                map_track_fig = create_track_map(tele_dash_year, tele_dash_race)
          st.plotly_chart(tele_dash_fig, use_container_width=True)
          st.pyplot(map_track_fig, use_container_width=True)

