import streamlit as st
import fastf1

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
    page_title="F1 Dashboard",
    page_icon="🏎️",
    layout="wide"
)
tab1, tab2, tab3, tab4 = st.tabs(["🏎️ F1 Dashboard", "📊 Qualifying Analysis", "🌦️ Weather Analysis", "📊 Race Analysis"])
with tab1:
    st.title("🏎️ F1 Dashboard")
    st.write("Welcome to Early Apex Analytics! This dashboard provides insights into Formula 1 races, drivers, and telemetry data." \
        "Use the naviagation menu to choose a section of analytics")

# -----------------------------------
# Race Selection
# -----------------------------------

    st.header("Race Selection")

    year = st.number_input(
    "Select season",
    min_value=2018,
    max_value=2026,
    value=2025,
    step=1
)

    races = get_races(year)

    selected_race = st.selectbox(
    "Select race",
    races
)

    session_type = st.selectbox(
    "Select session",
    ["R", "S"]
)

    drivers = get_drivers(
    year,
    selected_race,
    session_type
)

    selected_drivers = st.multiselect(
    "Select drivers",
    drivers
)

# -----------------------------------
# Generate Dashboard
# -----------------------------------

    if st.button("Generate Dashboard"):

    # ==========================================
    # Driver Analysis
    # ==========================================

        if selected_drivers:

            st.header("Driver Analysis")

            with st.spinner("Generating driver analysis..."):

                fig1, fig2 = create_driver_lap_data(
                year,
                selected_race,
                session_type,
                selected_drivers
            )

            if fig1 is not None:
                st.pyplot(fig1)

            if fig2 is not None:
                st.pyplot(fig2)

    # ==========================================
    # Championship Analysis
    # ==========================================

        st.header("Championship Analysis")

        schedule = fastf1.get_event_schedule(year)

        round_number = int(
            schedule.loc[
            schedule["EventName"] == selected_race,
            "RoundNumber"
        ].iloc[0]
        )

        st.write(f"Championship after Round {round_number}")

        try:

            champ_fig1, champ_fig2, champ_fig3 = create_championship_plots(
            year,
            round_number
            )

            st.pyplot(champ_fig1)
            st.plotly_chart(champ_fig2, use_container_width=True)
            st.plotly_chart(champ_fig3, use_container_width=True)

        except Exception as e:
            st.error(f"Championship analysis failed:\n\n{e}")
    ####################################
    #Telemetry Analysis
    ####################################
        st.header("Telemetry Analysis")
        with st.spinner("Generating telemetry analysis..."):
            telemetry_fig, telemetry_fig1, = create_track_visuals(
            year,
            selected_race,
            "Q",
            selected_drivers
            )
        st.pyplot(telemetry_fig, use_container_width=True)
        st.pyplot(telemetry_fig1, use_container_width=True)
    #####################################
    #Telemetry Dashboard
    #####################################
        st.header("Telemetry Dashboard")
        with st.spinner("Generating telemetry dashboard..."):
            tele_dashboard_fig = create_tele_dashboard(
            year,
            selected_race,
            "Q",
            selected_drivers
            )
        st.plotly_chart(tele_dashboard_fig, use_container_width=True)
    ######################################
    #Track Map
    ######################################
        st.header("Track Map")
        with st.spinner("Generating Track Map..."):
            map_track_fig = create_track_map(
            year, selected_race, "Q", selected_drivers
        )
        st.pyplot(map_track_fig, use_container_width=True)


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
    if st.button("Generate Qualifying Analysis"):
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
    if st.button("Generate Race Charts"):
        with st.spinner("Generating race charts..."):
            race_fig1, race_fig2, race_fig3, race_fig4 = create_race_traces(race_year, race_race, race_session)
        st.pyplot(race_fig1, use_container_width=True)
        st.pyplot(race_fig2, use_container_width=True)
        st.pyplot(race_fig3, use_container_width=True)
        st.pyplot(race_fig4, use_container_width=True)