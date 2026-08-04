import streamlit as st
import fastf1


@st.cache_data(show_spinner=False)
def get_races(year):
    schedule = fastf1.get_event_schedule(year)
    return schedule["EventName"].dropna().tolist()


@st.cache_data(show_spinner=False)
def get_drivers(year, event, session_type):

    session = fastf1.get_session(
        year,
        event,
        session_type
    )

    session.load(
        laps=False,
        telemetry=False,
        weather=False,
        messages=False
    )

    if not session.results.empty and "Abbreviation" in session.results.columns:
        return (
            session.results["Abbreviation"]
            .dropna()
            .unique()
            .tolist()
        )

    return []