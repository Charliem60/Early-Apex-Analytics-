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

    # Only load session information needed to identify drivers
    session.load(
        laps=False,
        telemetry=False,
        weather=False,
        messages=False
    )

    # Get driver abbreviations rather than driver numbers
    if not session.results.empty and "Abbreviation" in session.results.columns:
        return (
            session.results["Abbreviation"]
            .dropna()
            .unique()
            .tolist()
        )

    return []