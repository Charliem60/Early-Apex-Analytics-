import fastf1
def get_races(year):
    schedule = fastf1.get_event_schedule(year)
    return schedule["EventName"].tolist()
def get_drivers(year, event, session_type):
    session=fastf1.get_session(year, event, session_type)
    session.load()
    return session.drivers

