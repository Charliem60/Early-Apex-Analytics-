import streamlit as st
import fastf1

from backend.fastf1data import get_races, get_drivers
from backend.Driveranalysis import create_driver_lap_data
from backend.Quali import create_quali_plots
from backend.Championship import create_championship_plots

# -----------------------------------
# Page configuration
# -----------------------------------

st.set_page_config(
    page_title="F1 Dashboard",
    page_icon="🏎️",
    layout="wide"
)

st.title("🏎️ F1 Dashboard")

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
    # Qualifying Analysis
    # ==========================================

    st.header("Qualifying Analysis")

    with st.spinner("Generating qualifying analysis..."):

        quali_fig, quali_fig1, quali_fig2, quali_fig3 = create_quali_plots(
            year,
            selected_race,
            "Q",
            selected_drivers
        )

    st.pyplot(quali_fig)
    st.pyplot(quali_fig1)
    st.pyplot(quali_fig2)
    st.pyplot(quali_fig3)

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

        st.plotly_chart(
            champ_fig2,
            use_container_width=True
        )

        st.plotly_chart(
            champ_fig3,
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Championship analysis failed:\n\n{e}")