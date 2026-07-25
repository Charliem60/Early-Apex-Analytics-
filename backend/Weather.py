# First we need to import the necessary libraries. We will use matplotlib for plotting and fastf1 for accessing the Formula 1 data.
from matplotlib import pyplot as plt
import fastf1
from fastf1 import plotting
# Enables patches for plotting time values and loads dark colour theme.
fastf1.plotting.setup_mpl(mpl_timeddelta_support=True, color_scheme='fastf1')
year = int(input("Enter the year (eg 2022): "))
event = input("Enter the race name in full (eg 'Austrian Grand Prix'): ")
session_type = input("Enter the session (FP1, FP2, FP3, SQ, S, Q, R): ").upper()
session_names = {"FP1": "Free Practice 1", "FP2": "Free Practice 2", "FP3": "Free Practice 3", "SQ": "Sprint Qualifying", "S": "Sprint Race", "Q" : "Qualifying", "R": "Race"}
race = fastf1.get_session(year, event, session_type)
race.load()
#First we have to get the weather data
weather = race.weather_data
# Converting time to minutes
session_time = weather["Time"].dt.total_seconds()/60
# Creating the figure
fig, axes = plt.subplots(5, 1, figsize=(15 ,12), sharex=True)
# Air and Track Temperature
axes[0].plot(session_time, weather["AirTemp"], color = "blue", linewidth=2, label="Air Temp")
axes[0].plot(session_time, weather["TrackTemp"], color="green", linewidth=2, label = "Track Temp")
axes[0].set_ylabel("Temperature (°C)")
axes[0].set_title(f"{year} {event} {session_names.get(session_type, session_type)} Weather Report", color = "red", fontweight = "bold")
axes[0].legend()
axes[0].grid()
# Humidity
axes[1].plot(session_time, weather["Humidity"], color="red", linewidth=2)
axes[1].set_ylabel("Humidity (%)")
axes[1].grid()
# Pressure
axes[2].plot(session_time, weather["Pressure"], color="orange", linewidth=2)
axes[2].set_ylabel("Pressure (hPa)")
axes[2].grid()
# Wind Speed
axes[3].plot(session_time, weather["WindSpeed"], color = "lime", linewidth=3)
axes[3].set_ylabel("Wind Speed (m/s)")
axes[3].legend()
axes[3].grid()
# Rainfall
axes[4].plot(session_time, weather["Rainfall"].astype(int), color="darkblue", linewidth=3)
axes[4].set_ylabel("Rain")
axes[4].grid()
axes[-1].set_xlabel("Session Time (minutes)")

# Setting up the plots
plt.show()

