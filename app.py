import fastf1


def get_races(year):
    """
    Return all race names for a given F1 season.
    """
    schedule = fastf1.get_event_schedule(year)

    races = schedule[
        schedule["EventFormat"] != "testing"
    ]["EventName"].tolist()

    return races


def get_drivers(year, event, session_name):
    """
    Return driver abbreviations for a session.
    Example:
    ['VER', 'HAM', 'NOR']
    """

    session = fastf1.get_session(
        year,
        event,
        session_name
    )

    session.load(
        laps=False,
        telemetry=False,
        weather=False,
        messages=False
    )

    drivers = []

    for driver_number in session.drivers:
        driver = session.get_driver(driver_number)

        drivers.append(
            driver["Abbreviation"]
        )

    return sorted(drivers)