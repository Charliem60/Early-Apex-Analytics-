import streamlit as st

from backend.fastf1data import (
    get_races,
    get_drivers
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Early Apex Analytics",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 30px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏎️ Early Apex")

st.sidebar.markdown(
    "### F1 Data Analytics"
)

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "📊 Telemetry",
        "🏁 Qualifying",
        "🏎️ Race Analysis",
        "📈 Driver Analysis",
        "🗺️ Track Analysis",
        "🌦️ Weather"
    ]
)


# ============================================================
# GLOBAL SESSION SETTINGS
# ============================================================

if page != "🏠 Home":

    st.sidebar.divider()

    year = st.sidebar.selectbox(
        "Season",
        list(range(2018, 2026))
    )

    events = get_races(year)

    event = st.sidebar.selectbox(
        "Race",
        events
    )


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">'
        'EARLY APEX ANALYTICS'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Formula 1 performance analysis powered by FastF1'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader(
        "Welcome to Early Apex Analytics 🏁"
    )

    st.write(
        """
        Explore Formula 1 performance through telemetry,
        qualifying, race strategy, driver pace, track analysis
        and weather data.
        """
    )

    st.markdown("### Available Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 📊 Telemetry")

        st.write(
            """
            Compare drivers using:

            - Speed
            - Delta
            - Throttle
            - Brake
            - Gear
            - RPM
            """
        )

    with col2:

        st.markdown("### 🏁 Race")

        st.write(
            """
            Analyse:

            - Race position
            - Tyre strategy
            - Team pace
            - Gap to leader
            """
        )

    with col3:

        st.markdown("### 🗺️ Track")

        st.write(
            """
            Investigate:

            - Speed
            - Gear changes
            - Track domination
            - Racing lines
            """
        )

    st.divider()

    st.info(
        "Select an analysis from the sidebar to get started."
    )


# ============================================================
# TELEMETRY
# ============================================================

elif page == "📊 Telemetry":

    st.title("📊 Telemetry Dashboard")

    st.write(
        "Compare the telemetry of two or more drivers."
    )

    # -----------------------------------------
    # SESSION
    # -----------------------------------------

    session_type = st.selectbox(
        "Session",
        [
            "FP1",
            "FP2",
            "FP3",
            "SQ",
            "S",
            "Q",
            "R"
        ],
        key="telemetry_session"
    )

    # -----------------------------------------
    # DRIVERS
    # -----------------------------------------

    with st.spinner("Finding drivers..."):

        available_drivers = get_drivers(
            year,
            event,
            session_type
        )

    st.write(
        f"Drivers available: {len(available_drivers)}"
    )

    drivers = st.multiselect(
        "Select drivers to compare",
        available_drivers,
        key="telemetry_drivers"
    )

    # -----------------------------------------
    # GENERATE
    # -----------------------------------------

    if st.button(
        "Generate Telemetry Dashboard",
        key="generate_telemetry"
    ):

        if len(drivers) < 2:

            st.warning(
                "Please select at least 2 drivers."
            )

        else:

            from backend.Telemetrydashboard import (
                create_tele_dashboard
            )

            with st.spinner(
                "Loading FastF1 telemetry..."
            ):

                fig = create_tele_dashboard(
                    year,
                    event,
                    session_type,
                    drivers
                )

            st.success(
                "Telemetry loaded!"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
# ============================================================
# QUALIFYING
# ============================================================

elif page == "🏁 Qualifying":

    st.title("🏁 Qualifying Results")

    st.write(
        f"Qualifying results for the {year} {event}"
    )

    if st.button(
        "Load Qualifying Results",
        key="load_qualifying"
    ):

        from backend.Quali import (
            get_qualifying_results
        )

        with st.spinner(
            "Loading qualifying results..."
        ):

            results = get_qualifying_results(
                year,
                event
            )

        st.success("Qualifying results loaded!")

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )
# ============================================================
# RACE ANALYSIS
# ============================================================

elif page == "🏎️ Race Analysis":

    st.title("🏎️ Race Analysis")

    st.write(
        "Explore the major performance factors from the race."
    )

    if st.button(
        "Generate Race Analysis"
    ):

        from backend.Race import (
            create_race_traces
        )

        with st.spinner(
            "Loading race data..."
        ):

            (
                fig_position,
                fig_strategy,
                fig_pace,
                fig_gap
            ) = create_race_traces(
                year,
                event,
                "R"
            )

        st.success(
            "Race analysis generated!"
        )

        st.subheader(
            "🏁 Position Changes"
        )

        st.pyplot(
            fig_position,
            use_container_width=True
        )

        st.subheader(
            "🛞 Tyre Strategy"
        )

        st.pyplot(
            fig_strategy,
            use_container_width=True
        )

        st.subheader(
            "📈 Team Race Pace"
        )

        st.pyplot(
            fig_pace,
            use_container_width=True
        )

        st.subheader(
            "⏱️ Gap to Race Leader"
        )

        st.pyplot(
            fig_gap,
            use_container_width=True
        )


# ============================================================
# DRIVER ANALYSIS
# ============================================================

elif page == "📈 Driver Analysis":

    st.title("📈 Driver Analysis")

    st.write(
        "Investigate driver lap-time performance."
    )

    session_type = st.selectbox(
        "Session",
        [
            "FP1",
            "FP2",
            "FP3",
            "SQ",
            "Q",
            "R"
        ],
        key="driver_session"
    )

    available_drivers = get_drivers(
        year,
        event,
        session_type
    )

    drivers = st.multiselect(
        "Drivers",
        available_drivers,
        key="driver_selection"
    )

    if st.button(
        "Generate Driver Analysis"
    ):

        if not drivers:

            st.warning(
                "Please select at least one driver."
            )

        else:

            from backend.Driveranalysis import (
                create_driver_traces
            )

            with st.spinner(
                "Loading driver data..."
            ):

                (
                    fig1,
                    fig2
                ) = create_driver_traces(
                    year,
                    event,
                    session_type,
                    drivers
                )

            st.success(
                "Driver analysis generated!"
            )

            st.subheader(
                "Lap Time Progression"
            )

            st.pyplot(
                fig1,
                use_container_width=True
            )

            st.subheader(
                "Lap Time & Tyre Compound"
            )

            st.pyplot(
                fig2,
                use_container_width=True
            )


# ============================================================
# TRACK ANALYSIS
# ============================================================

elif page == "🗺️ Track Analysis":

    st.title("🗺️ Track Analysis")

    st.write(
        "Compare driver performance around the circuit."
    )

    session_type = st.selectbox(
        "Session",
        [
            "FP1",
            "FP2",
            "FP3",
            "SQ",
            "Q",
            "R"
        ],
        key="track_session"
    )

    available_drivers = get_drivers(
        year,
        event,
        session_type
    )

    drivers = st.multiselect(
        "Drivers",
        available_drivers,
        key="track_drivers"
    )

    if st.button(
        "Generate Track Analysis"
    ):

        if len(drivers) < 2:

            st.warning(
                "Please select at least 2 drivers."
            )

        else:

            st.info(
                "Track analysis module will be connected next."
            )


# ============================================================
# WEATHER
# ============================================================

elif page == "🌦️ Weather":

    st.title("🌦️ Weather Analysis")

    st.write(
        "Analyse the weather conditions throughout the session."
    )

    session_type = st.selectbox(
        "Session",
        [
            "FP1",
            "FP2",
            "FP3",
            "SQ",
            "Q",
            "R"
        ],
        key="weather_session"
    )

    if st.button(
        "Generate Weather Analysis"
    ):

        from backend.Weather import (
            create_weather_dashboard
        )

        with st.spinner(
            "Loading weather data..."
        ):

            fig = create_weather_dashboard(
                year,
                event,
                session_type
            )

        st.success(
            "Weather data loaded!"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )