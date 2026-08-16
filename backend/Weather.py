# First we need to import the necessary libraries. We will use matplotlib for plotting and fastf1 for accessing the Formula 1 data.
from matplotlib import pyplot as plt
import fastf1 as fastf1
from fastf1 import plotting
# Enables patches for plotting time values and loads dark colour theme.
fastf1.plotting.setup_mpl(mpl_timeddelta_support=True, color_scheme='fastf1')
# Like with all the others, we fetch the user choosen session, year and so on and load the session.
def create_weather_dashboard(year, event, session_type):
    race = fastf1.get_session(year, event, session_type)
    race.load()
#We have to get the weather data
    weather = race.weather_data
# Converting time to minutes
    session_time = weather["Time"].dt.total_seconds()/60
# Creating the figure and sharing the x axis for the dashboard
    fig, axes = plt.subplots(5, 1, figsize=(15 ,12), sharex=True)
# Air and Track Temperature throughout the session. Plot them on the same graph to compare easily.
    axes[0].plot(session_time, weather["AirTemp"], color = "#4BA3C3", linewidth=2, label="Air Temp")
    axes[0].plot(session_time, weather["TrackTemp"], color="#D62839", linewidth=2, label = "Track Temp")
    axes[0].set_ylabel("Temperature (°C)")
    axes[0].set_title(f"{year} {event} {session_type} Weather Report", color = "#4BA3C3", fontweight = "bold")
    axes[0].legend()
    axes[0].grid()
# Humidity. Label as percentage. Add grid to make changes easy.
    axes[1].plot(session_time, weather["Humidity"], color="#D62839", linewidth=2, label="Humidity")
    axes[1].set_ylabel("Humidity (%)")
    axes[1].grid()
# Pressure. Same as before but change it for the different measurement tested.
    axes[2].plot(session_time, weather["Pressure"], color="#BA324F", linewidth=2, label = "Pressure")
    axes[2].set_ylabel("Pressure (hPa)")
    axes[2].grid()
# Wind Speed.
    axes[3].plot(session_time, weather["WindSpeed"], color = "#CCE6F4", linewidth=3, label="Wind Speed")
    axes[3].set_ylabel("Wind Speed (m/s)")
    axes[3].legend()
    axes[3].grid()
# Rainfall. Setting the x label of the dashboard to show the session time throughout.
    axes[4].plot(session_time, weather["Rainfall"].astype(int), color="#4BA3C3", linewidth=3, label="Rainfall")
    axes[4].set_ylabel("Rain")
    axes[4].grid()
    axes[-1].set_xlabel("Session Time (minutes)")

# Displaying the dashboard
    return fig

