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


@st.cache_data(show_spinner=False)
def get_sessions(year, event):
    """
    Return only the sessions that exist for the selected event.
    """

    schedule = fastf1.get_event_schedule(year)

    race = schedule[schedule["EventName"] == event].iloc[0]

    sessions = []

    for i in range(1, 6):
        session_name = race.get(f"Session{i}")

        if session_name is None:
            continue

        if session_name == "Practice 1":
            sessions.append("FP1")
        elif session_name == "Practice 2":
            sessions.append("FP2")
        elif session_name == "Practice 3":
            sessions.append("FP3")
        elif session_name == "Qualifying":
            sessions.append("Q")
        elif session_name == "Sprint":
            sessions.append("S")
        elif session_name == "Sprint Qualifying":
            sessions.append("SQ")
        elif session_name == "Sprint Shootout":
            sessions.append("SS")
        elif session_name == "Race":
            sessions.append("R")

    return sessions