import streamlit as st

from backend.fastf1data import get_races, get_drivers
from backend.Driveranalysis import create_driver_lap_data
from backend.Quali import create_quali_plots


# -----------------------------------
# Page configuration
# -----------------------------------

st.set_page_config(
    page_title="F1 Dashboard",
    page_icon="🏎️",
    layout="wide"
)

st.title("F1 Dashboard")


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


# -----------------------------------
# Race
# -----------------------------------

races = get_races(year)

selected_race = st.selectbox(
    "Select race",
    races
)


# -----------------------------------
# Session
# -----------------------------------

session_type = st.selectbox(
    "Select session",
    ["R", "S"]
)


# -----------------------------------
# Drivers
# -----------------------------------

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
# Driver Analysis
# -----------------------------------

if selected_drivers:

    generate = st.button("Generate Analysis")

    if generate:

        with st.spinner("Loading F1 session data..."):

            fig1, fig2 = create_driver_lap_data(
                year,
                selected_race,
                session_type,
                selected_drivers
            )

        st.subheader("Lap Time Analysis")
        st.pyplot(fig1)

        st.subheader("Lap Time Scatterplot")
        st.pyplot(fig2)
# -----------------------------------
# Qualifying Analysis
# -----------------------------------

st.header("Qualifying Analysis")

if st.button("Generate Qualifying Report"):

    with st.spinner("Loading qualifying data..."):

        quali_fig, quali_fig1, quali_fig2, quali_fig3 = create_quali_plots(
            year,
            selected_race,
            "Q",
            selected_drivers
        )

    st.subheader("Qualifying Results")
    st.pyplot(quali_fig)

    st.subheader("Q1, Q2 & Q3 Results")
    st.pyplot(quali_fig1)

    st.subheader("Sector Results")
    st.pyplot(quali_fig2)

    st.subheader("Actual vs Ideal Lap Times")
    st.pyplot(quali_fig3)