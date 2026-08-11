import streamlit as st
import fastf1
# Cacheing the data so Streamlit doesn't have to reload it over and over and over and over again.
@st.cache_data(show_spinner=False)
def get_races(year):
    schedule = fastf1.get_event_schedule(year)
    return schedule["EventName"].dropna().tolist()

# Caching the driver data to stop loading the same session over and over.
@st.cache_data(show_spinner=False)
def get_drivers(year, event, session_type):
    # Getting the session and so on and loading everything that has been selected by the user.
    session = fastf1.get_session(
        year,
        event,
        session_type
    )
    # Load the simplistic results
    session.load(
        laps=False,
        telemetry=False,
        weather=False,
        messages=False
    )
    # Checking that the results are not emty and that the driver names are there in it.
    if not session.results.empty and "Abbreviation" in session.results.columns:
        return (
            session.results["Abbreviation"]
            .dropna()
            .unique()
            .tolist()
        )
    # Return the empty list if here are no driver results.
    return []

# Caching the session data for the selected race.
@st.cache_data(show_spinner=False)
def get_sessions(year, event):
    """
    Return only the sessions that exist for the selected event.
    """
    # Loading the schedule, finding the race and creating an empty list to store the sessions.
    schedule = fastf1.get_event_schedule(year)
    race = schedule[schedule["EventName"] == event].iloc[0]
    sessions = []
    # Check the session slots.
    for i in range(1, 6):
        session_name = race.get(f"Session{i}")
        # Ignore te empty session slots.
        if session_name is None:
            continue
        #Convert the fastf1 full session names into shorter names for the website.
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
    # Return the list and sessions for the selected race.
    return sessions