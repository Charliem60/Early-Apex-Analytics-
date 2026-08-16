import os
import streamlit as st
import fastf1
import base64
from pathlib import Path
# Setting up the config of the streamlit page
st.set_page_config(
    page_title="Early Apex Analytics",
    layout="wide"
)

# Creating FastF1 cache
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
# Load background image for the app. This image is by Felix Berger on the free image use website Unsplash. A thanks for the use of that photo for the background of the site.
image_path = Path("assets/background_image.jpg")

if image_path.exists():
    image_base64 = base64.b64encode(
        image_path.read_bytes()
    ).decode()
else:
    image_base64 = ""

# Now we are building a custom css for the website. I have randomly chosen a variety of colours that are the branding colours of the site.
# They are Crimson  #D62839  Rosewood  #BA324F  Baltic Blue   #175676  Surf Blue  #4BA3C3   and finally Pale Sky  #CCE6F4

st.markdown(f"""
<style>

/* the main background for the css with the added image  */

[data-testid="stAppViewContainer"] {{
    background:
        linear-gradient(
            rgba(5, 15, 27, 0.72),
            rgba(5, 15, 27, 0.82)
        ),
        url("data:image/jpeg;base64,{image_base64}");

    background-size: cover;
    background-position: center center;
    background-attachment: fixed;
}}

/* making it sort of clear */

[data-testid="stAppViewContainer"] > .main {{
    background: transparent !important;
}}


/* giving the site a header and formatting that to blend in and fixing the navigation. */

[data-testid="stHeader"] {{
    background: rgba(9, 24, 39, 0.30) !important;

    border-bottom:
        1px solid rgba(255, 255, 255, 0.08) !important;
}}

[data-testid="stToolbar"] {{
    background: transparent !important;
}}


/* Now for the main content of the site, this includes formatting the headings, sidebars, the content containers to fuzzy the background image and the select boxes for the graphs and plots */

.block-container {{
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;

    max-width: 1400px !important;
}}

h1, h2, h3, h4, h5, h6 {{
    color: #FFFFFF !important;

    font-weight: 800 !important;

    text-shadow:
        0 2px 8px rgba(0, 0, 0, 0.65);
}}


h1 {{
    font-size: 2.7rem !important;
    letter-spacing: -0.5px;
}}


h2 {{
    font-size: 2rem !important;
}}


h3 {{
    font-size: 1.5rem !important;
}}


p {{
    color: #FFFFFF !important;
}}


label {{
    color: #FFFFFF !important;
    font-weight: 600 !important;
}}


[data-testid="stSidebar"] {{
    background:
        linear-gradient(
            180deg,
            rgba(23, 86, 118, 0.96),
            rgba(9, 24, 39, 0.96)
        ) !important;

    border-right:
        2px solid rgba(75, 163, 195, 0.55) !important;

    box-shadow:
        5px 0 25px rgba(0, 0, 0, 0.25);
}}


[data-testid="stSidebar"] * {{
    color: #FFFFFF !important;
}}


[data-testid="stSidebar"] a {{
    color: #FFFFFF !important;
}}

[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(9, 24, 39, 0.60) !important;

    border: 1px solid rgba(75, 163, 195, 0.30) !important;

    border-radius: 16px !important;

    box-shadow:
        0 8px 30px rgba(0, 0, 0, 0.25);

    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}}

div[data-baseweb="select"] > div {{
    background:
        rgba(23, 86, 118, 0.96) !important;

    border:
        2px solid #4BA3C3 !important;

    border-radius: 10px !important;

    min-height: 42px !important;
}}


div[data-baseweb="select"] span {{
    color: #FFFFFF !important;
}}


div[data-baseweb="select"] svg {{
    fill: #FFFFFF !important;
}}


div[data-baseweb="select"] input {{
    color: #FFFFFF !important;
}}


/* Dropdown for the input clickers */

div[role="listbox"] {{
    background:
        #175676 !important;

    border:
        2px solid #4BA3C3 !important;

    border-radius: 10px !important;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.35);
}}


div[role="option"] {{
    background: #175676 !important;

    color: #FFFFFF !important;
}}


div[role="option"]:hover {{
    background: #4BA3C3 !important;

    color: #FFFFFF !important;
}}


/* Continuining with multi select tags, colouring them with the branding colours of the app. */

div[data-baseweb="tag"] {{
    background:
        #4BA3C3 !important;

    border:
        1px solid #175676 !important;

    border-radius: 6px !important;
}}


div[data-baseweb="tag"] span {{
    color: #FFFFFF !important;
}}

/* Formatting the buttons, and giving them colours of the sites branding same as before. */

.stButton button {{
    background:
        linear-gradient(
            135deg,
            #D62839,
            #BA324F
        ) !important;

    color:
        #FFFFFF !important;

    border:
        2px solid #D62839 !important;

    border-radius:
        10px !important;

    padding:
        0.65rem 1.5rem !important;

    font-weight:
        800 !important;

    box-shadow:
        0 6px 18px rgba(214, 40, 57, 0.38);

    transition:
        all 0.2s ease !important;
}}


.stButton button p {{
    color:
        #FFFFFF !important;

    font-weight:
        800 !important;
}}


.stButton button:hover {{
    background:
        linear-gradient(
            135deg,
            #BA324F,
            #D62839
        ) !important;

    border-color:
        #BA324F !important;

    transform:
        translateY(-2px);

    box-shadow:
        0 10px 25px rgba(214, 40, 57, 0.50);
}}

button[kind="secondary"] {{
    background:
        rgba(23, 86, 118, 0.95) !important;

    border:
        2px solid #4BA3C3 !important;

    color:
        #FFFFFF !important;
}}


button[kind="secondary"] p {{
    color:
        #FFFFFF !important;
}}

/* Formatting the home page so that the deviders and the info text blends into the ui design */

[data-testid="stAlert"] {{
    border-radius:
        12px !important;

    box-shadow:
        0 5px 15px rgba(0, 0, 0, 0.18);
}}

hr {{
    border-color:
        rgba(204, 230, 244, 0.35) !important;

    opacity:
        0.7 !important;
}}


/* This makes sure that it looks good on a phone. Not in use right now, but this section is purely here for future updates. */

@media (max-width: 768px) {{

    h1 {{
        font-size:
            2rem !important;
    }}

    h2 {{
        font-size:
            1.5rem !important;
    }}

    .block-container {{
        padding-top:
            1rem !important;

        padding-left:
            1rem !important;

        padding-right:
            1rem !important;

    }}
    

}}


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
    st.title("Early Apex Analytics")

    st.subheader(
      "Welcome to Early Apex Analytics!"
    )

    st.markdown("""
    Explore Formula One data from 2018 to present from qualifying graphs, race plots, telemetry and weather dashboards and much more.
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
        **Qualifying Analysis**  
        Compare lap times, sectors and ideal vs actual laps.

        **Race Analysis**  
        Examine pace between teammates, rivals, race strategies and position changes.

        **Driver Analysis**  
        Compare driver session plans, runs and laptimes during a session.
        """)

    with col2:
        st.markdown("""
        **Telemetry**  
        Explore braking, throttle and speed traces between different cars over a lap.

        **Weather**  
        A dashboard for understanding weather conditions during any given session.

        **Championship**  
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
    st.write("Use this section to analyze qualifying sessions for a selected race, such as ideal vs actual lap times, sector performance, and more. Pick and choose a season and race using the inputs below.")
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
