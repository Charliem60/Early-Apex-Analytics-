import fastf1
import fastf1.plotting
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.collections import LineCollection
import matplotlib as mpl
from matplotlib.lines import Line2D
import random
# Enables patches for plotting time values and loads dark colour theme.
fastf1.plotting.setup_mpl(mpl_timeddelta_support=True, color_scheme='fastf1')
# Get the user inputed data from the app to be displayed on the map. Load the session data
def create_track_map(year, event, session_type, drivers):
    race = fastf1.get_session(year, event, session_type)
    race.load()
    # Getting the fastest lap of the selected drivers from the session.
    driver_tel = {}
    for driver in drivers:
        lap = race.laps.pick_drivers(driver).pick_fastest()
# Fetching the telemetry
        tel = lap.get_telemetry().add_distance()
        driver_tel[driver] = tel
# Now we are creating a reference using the first selected driver as the reference for the circuit's coordinates and lap distace. Important!
    reference_driver = list(driver_tel.keys())[0]
    reference_tel = driver_tel[reference_driver]
    # Creating the spaced points as explained below to show which driver is quicker and where
    distance = np.arange(0, reference_tel["Distance"].max(), 25)
# Calculating times at every point. In this case we have done so every 25 metres. This can be adjusted.
    times = {}
    for driver, tel in driver_tel.items():
        times[driver] = np.interp(distance, tel["Distance"], tel["Time"].dt.total_seconds())
# Getting each mini sector time, ie how quick the drivers past from point to point
    mini_sector = {}
    for driver, t in times.items():
        mini_sector[driver] = np.diff(t)
# Finding fastest driver in each mini sector
    fastest_drivers = []
    for i in range (len(distance)-1):
        fastest_driver = min(mini_sector, key=lambda d:mini_sector[d][i])
        fastest_drivers.append(fastest_driver)
# Building the track line using the x and y coordinates
    x = np.interp(distance,reference_tel["Distance"],reference_tel["X"])
    y= np.interp(distance,reference_tel["Distance"],reference_tel["Y"])
    points = np.array([x,y]).T.reshape(-1,1,2)
    # Joining all the points together to create the line segments. One segment = one mini sector
    segments=np.concatenate([points[:-1], points[1:]], axis=1)
# Assing driver colors fromt the fastf1 libary. 
    driver_colors = {}
    # The below keeps track of colours used. Ensures that teammates selected don't have the same colour and can be distingued using a random colour later.
    see_colors = {}
    for driver in drivers:
        color = fastf1.plotting.get_driver_color(driver, session=race)
        if color in see_colors:
            driver_colors[driver] = "#{:06x}".format(random.randint(0,0xFFFFFF))
        else:
            driver_colors[driver] = color
            see_colors[color] = driver
# Building the plot and the base of the track
    fig, ax = plt.subplots(figsize=(11, 7))
    base = LineCollection(segments, linewidth=8, alpha = 0.7, colors="white")
    ax.add_collection(base)
# This is where and how we colour the track by the colour of the fastest driver through each segment and style it that way. Also creates custom legend for the map
    for driver in drivers:
        driver_segments = [segments[i] for i, winner in enumerate(fastest_drivers) if winner == driver]
        line = LineCollection(driver_segments, colors=driver_colors[driver] , linewidth=6, capstyle="round")
        ax.add_collection(line)
    legend_elements =[Line2D([0], [0], color = driver_colors[driver], label=driver, lw=5) for driver in drivers]
# The corner numbers. Fetches information of the circuit and the corners from the libary and adds the corner lables using the coordinates of said corners.
    circuit = race.get_circuit_info()
    corners = circuit.corners
    for _, corner in corners.iterrows():
        ax.text(corner["X"], corner["Y"], str(corner["Number"]), color="#4BA3C3", fontsize=8, weight="bold", ha="center", va="center")
# Formating everything, giving it a title and displaying it
    ax.axis("equal")
    ax.axis("off")
    ax.legend(handles=legend_elements, loc="upper left")
    plt.title(f"{year} {event} {session_type} Fastest Lap Track Domination Comparison Plot", color="#D62839", fontsize=16, fontweight="bold")
    plt.tight_layout()
    return fig
