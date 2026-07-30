import fastf1


def get_races(year):
    schedule = fastf1.get_event_schedule(year)

    return schedule["EventName"].dropna().tolist()


def get_drivers(year, event, session_type):

    session = fastf1.get_session(
        year,
        event,
        session_type
    )

    # Only load the session information we need
    # to identify the drivers.
    session.load(
        laps=False,
        telemetry=False,
        weather=False,
        messages=False
    )

    return session.drivers