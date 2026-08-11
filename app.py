import os
import streamlit as st
import fastf1
# Create FastF1 cache
cache_app = "cache"

if not os.path.exists(cache_app):
    os.makedirs(cache_app)
fastf1.Cache.enable_cache(cache_app)  # Enable caching for FastF1 data
# Connecting the backend to the frontend and importing everything.
from backend.fastf1data import get_races, get_drivers, get_sessions
from backend.Driveranalysis import create_driver_lap_data
from backend.Quali import create_quali_plots
from backend.Championship import create_championship_plots
from backend.Race import create_race_traces
from backend.Telemetryanalysis import create_track_visuals
from backend.Telemetrydashboard import create_tele_dashboard
from backend.TrackMap import create_track_map
from backend.Weather import create_weather_dashboard

# Setting up the configuration of the streamlit app.

st.set_page_config(
    page_title="Early Apex Analytics",
    page_icon="🏎️",
    layout="wide"
)
# Building a yellow and partly black css for the website.
st.markdown("""
<style>

[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background: #FFF4B8 !important;
}

h1, h2, h3, h4, h5, h6,
p, label {
    color: #000000 !important;
}

[data-testid="stNumberInput"] input {
    background: white !important;
    color: black !important;
}
div[data-baseweb="select"] > div {
    background: white !important;
    border-radius: 10px !important;
    border: 2px solid black !important;
}

div[data-baseweb="select"] span {
    color: black !important;
}

.stButton button {
    background: black !important;
    border-radius: 10px !important;
    border: 2px solid black !important;
    padding: 0.6rem 1.5rem !important;
}

.stButton button p {
    color: #FFD700 !important;
    font-weight: bold !important;
}


[data-testid="metric-container"] {
    background: white !important;
    border: 2px solid black !important;
    border-radius: 12px !important;
}


div[data-baseweb="select"] > div {
    background-color: #000000 !important;
    border: 2px solid #000000 !important;
    border-radius: 10px !important;
}

/* Selected text */
div[data-baseweb="select"] span {
    color: #FFD700 !important;
}

/* Dropdown arrow */
div[data-baseweb="select"] svg {
    fill: #FFD700 !important;
}

/* Dropdown menu */
div[role="listbox"] {
    background-color: #000000 !important;
}

/* Dropdown options */
div[role="option"] {
    background-color: #000000 !important;
    color: #FFD700 !important;
}

/* Hover option */
div[role="option"]:hover {
    background-color: #FFD700 !important;
    color: #000000 !important;
}

div[data-baseweb="select"] input {
    color: #FFD700 !important;
}

/* Selected driver tags */
div[data-baseweb="tag"] {
    background-color: #FFD700 !important;
    color: #000000 !important;
}

div[data-baseweb="tag"] span {
    color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)
# Setting up the tabs to move between the different pages of analysis.
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [
        "🏠 Home Page",
        "⏱ Qualifying",
        "🏁 Race Pace",
        "👤 Driver Analysis",
        "📡 Telemetry",
        "🌦 Weather",
        "🏆 Championship",
        "📊 Telemetry Dashboard"
    ]
)
# Setting up tab one, the home page, the title, the headers, explaining what the app can do and so on.
with tab1:
    st.title("🏎️ Early Apex Analytics")

    st.subheader(
      "Welcome to Early Apex Analytics!"
    )

    st.markdown("""
    This is a web app that with the help of FastF1 API data, allows you to explore F1 data from 2018 to present. The types of data you can explore is explained below.
    <br>

    ⚠️ 
    Please note that this app is very much in early development, and there will be bugs and issues that I haven't ironed out just yet. There will be updates gradually across the coming months and years.
    ⚠️
    <br>

    Thank you for your support.
    """, unsafe_allow_html=True
    )
    st.divider()
    st.subheader("What data you can explore:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **⏱ Qualifying Analysis**  
        Compare lap times, sectors and ideal vs actual laps.

        **🏁 Race Analysis**  
        Examine pace between teammates, rivals, race strategies and position changes.

        **👤 Driver Analysis**  
        Compare driver session plans, runs and laptimes during a session.
        """)

    with col2:
        st.markdown("""
        **📡 Telemetry**  
        Explore braking, throttle and speed traces between different cars over a lap.

        **🌦 Weather**  
        A dashboard for understanding weather conditions during any given session.

        **🏆 Championship**  
        Examine past season standings and trends.
        """)

    st.divider()

    st.info(
        "Select a tab above to begin exploring Formula 1 data."
    )
################################
#Quali Page
################################
with tab2:
    st.header("Qualifying Analysis")
    # Choosing the race and the year and so on.
    st.write("Use this section to analyze qualifying sessions for a selected race, such as ideal vs actual lap times, sector performance, and more. Pick and Choose a season and race using the inputs below.")
    quali_year = st.selectbox("Season", list(range(2018, 2027)), index=8, key="quali_year")
    quali_races= get_races(quali_year)
    quali_race = st.selectbox("Race", quali_races, key="quali_race")
    quali_drivers = get_drivers(quali_year, quali_race,"Q")
    #Generating the plots
    if st.button("Generate Qualifying Analysis", key="quali_analysis_button"):
        with st.spinner("Generating qualifying analysis..."):
            quali_fig, quali_fig1, quali_fig2, quali_fig3 = create_quali_plots(
            quali_year,
            quali_race,
            "Q",
            quali_drivers
            )
        # Displaying the plots
        st.pyplot(quali_fig)
        st.write("The two following charts show the complete results across the session and the sector times for each driver in the qualifying session.")
        st.pyplot(quali_fig1)
        st.pyplot(quali_fig2)
        st.write("The following chart shows the ideal lap time vs the actual lap time for each driver in the qualifying session. The ideal lap time is calculated by taking the best sector times from all drivers and combining them to create a theoretical 'perfect' lap. The actual lap time is the time that each driver actually achieved during their qualifying laps.")
        st.pyplot(quali_fig3)

    #######################################
    # Weather Dashboard
    #######################################
with tab6:
    st.header("Weather Dashboard")
    #Choosing the race and the year and so on.
    st.write("Use this section to analyze weather conditions for a selected race and session, including temperature, humidity, wind speed, and more to understand their impact on a given session.")
    weather_year = st.selectbox("Season", list(range(2018, 2027)), index=8, key="weather_year")
    weather_race = st.selectbox("Race", get_races(weather_year), key="weather_race")
    weather_session = st.selectbox("Session", get_sessions(weather_year, weather_race), key="weather_session")
    # Gemerating and displaying it.
    if st.button("Generate Weather Dashboard"):
        with st.spinner("Generating weather dashboard..."):
            weather_fig = create_weather_dashboard(weather_year,weather_race,weather_session)
        st.plotly_chart(weather_fig, use_container_width=True)
#######################################
#RACE Charts
#######################################
with tab3:
    st.header("Race Charts and Analysis")
    #Choosing the race and the year and so on.
    st.write("Use this section to analyze a race including position changes, strategy, and other key metrics.")
    race_year = st.selectbox("Season", list(range(2018, 2027)), index=8, key="race_year")
    race_race = st.selectbox("Race", get_races(race_year), key="race_race")
    race_session = "R"
    # Gemerating and displaying all the plots and giving information on them.
    if st.button("Generate Race Charts", key="race_charts_button"):
        with st.spinner("Generating race charts..."):
            race_fig1, race_fig2, race_fig3, race_fig4 = create_race_traces(race_year, race_race, race_session)
        st.pyplot(race_fig1)
        st.write("The following chart shows the strategy used by each driver during the race.")
        st.pyplot(race_fig2)
        st.write("The following charts show the race pace distribution for each team and how the gap to the race leader changed over the course of the race.")
        st.pyplot(race_fig3)
        st.pyplot(race_fig4)

#######################################
# DRIVER CHARTS
######################################
with tab4:
    st.header("Driver Charts and Analysis")
    #Choosing the race and the year and so on.
    st.write("Use this section to compare drivers over the course of race stints and other metrics. You can select multiple drivers to compare their performance during any session. Investigate their lap times over the course of a session on a lap-by-lap basis, and compare their performance against each other.")
    driver_year = st.selectbox("Season", list(range(2018, 2027)), index=8, key="driver_year")
    driver_race = st.selectbox("Race", get_races(driver_year), key="driver_race")
    driver_session = st.selectbox("Session", get_sessions(driver_year, driver_race), key="driver_session")
    driver_drivers = get_drivers(driver_year, driver_race, driver_session)
    selected_driver_drivers = st.multiselect("Select drivers", driver_drivers, key="selected_driver_drivers")   
    if st.button("Generate Charts", key="driver_charts_button"):
    # Generating and displaying all the plots and giving information on them.
        with st.spinner("Generating driver charts..."):
            driver_fig1, driver_fig2 = create_driver_lap_data(driver_year, driver_race, driver_session, selected_driver_drivers)
        st.pyplot(driver_fig1)
        st.pyplot(driver_fig2)
#######################################
# Telemetry Graphics
######################################
with tab5:
    st.header("Telemetry Graphics")
    #Choosing the race and the year and so on.
    st.write("Use this section to visualize telemetry data for any selected drivers in a session of your choice. Please pick four drivers!")
    telemetry_year = st.selectbox("Season", list(range(2018, 2027)), index=8, key="telemetry_year")
    telemetry_race = st.selectbox("Race", get_races(telemetry_year), key="telemetry_race")
    telemetry_session = st.selectbox("Session", get_sessions(telemetry_year, telemetry_race), key="telemetry_session")
    telemetry_drivers = get_drivers(telemetry_year, telemetry_race, telemetry_session)
    selected_telemetry_drivers = st.multiselect("Select drivers", telemetry_drivers, key="selected_telemetry_drivers")   
    # Generating and displaying all the plots and giving information on them.
    if st.button("Generate Charts", key="telemetry_charts_button"):
        with st.spinner("Generating telemetry charts..."):
            telemetry_fig1, telemetry_fig2 = create_track_visuals(telemetry_year, telemetry_race, telemetry_session, selected_telemetry_drivers)
        st.write("The first visual plots the gears used across the track, highlighting deployment tactics and the differing gear ratios of different teams." \
        " The second visual shows the speed across the track, again highlighting deployment tactics. Please pick four drivers so that the graphs don't crash!")
        st.pyplot(telemetry_fig1)
        st.pyplot(telemetry_fig2)

#######################################
# Championship Standings
######################################
with tab7:
    st.header("Championship Standings")
    st.write("Use this section to view the championship standings across past seasons and how a title fight develops.")
    champ_year = st.selectbox("Season", list(range(2018, 2027)), index=8, key="champ_year")
    if st.button("Generate Championship Standings", key="champ_standings_button"):
        with st.spinner("Generating championship standings..."):
            champ_fig2, champ_fig3 = create_championship_plots(champ_year)
        st.plotly_chart(champ_fig2, use_container_width=True)
        st.plotly_chart(champ_fig3, use_container_width=True)
#######################################
# Telemetry Dashboard
######################################
with tab8:
    st.header("Telemetry Dashboard")
    st.write("Use this section to inspect telemetry data for selected drivers in any session in a dashboard format.")
    tele_dash_year = st.selectbox("Season", list(range(2018, 2027)), index=8, key="tele_dash_year")
    tele_dash_race = st.selectbox("Race", get_races(tele_dash_year), key="tele_dash_race")
    tele_dash_session = st.selectbox("Session", get_sessions(tele_dash_year, tele_dash_race), key="tele_dash_session")
    tele_dash_drivers = get_drivers(tele_dash_year, tele_dash_race, tele_dash_session)
    selected_tele_dash_drivers = st.multiselect("Select drivers", tele_dash_drivers, key="selected_tele_dash_drivers") 
    if st.button("Generate Telemetry Dashboard", key="tele_dash_button"):
          with st.spinner("Generating telemetry dashboard..."):
                tele_dash_fig = create_tele_dashboard(tele_dash_year, tele_dash_race, tele_dash_session, selected_tele_dash_drivers)
                map_track_fig = create_track_map(tele_dash_year, tele_dash_race, tele_dash_session, selected_tele_dash_drivers)
          st.plotly_chart(tele_dash_fig, use_container_width=True)
          st.write("In the above dashboard you can investigate differing gear changes, identify differing battery deployment rates, where drivers are braking, and find out where time is won and lost." \
          "In the track map below, it plots the fastest laps of your selected drivers in the given session, and shows who is quicker and where.")
          st.pyplot(map_track_fig)
# That is everything sorted as far as the website looks and connecting all the data and so on.
