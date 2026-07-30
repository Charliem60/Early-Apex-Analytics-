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

def create_track_map(year, event, session_type, drivers):
    race = fastf1.get_session(year, event, session_type)
    race.load()
    # Fastest Lap
    driver_tel = {}
    for driver in drivers:
        lap = race.laps.pick_drivers(driver).pick_fastest()
# Fetching the telemetry
        tel = lap.get_telemetry().add_distance()
        driver_tel[driver] = tel
# References
    reference_driver = list(driver_tel.keys())[0]
    reference_tel = driver_tel[reference_driver]
    distance = np.arange(0, reference_tel["Distance"].max(), 25)
# Calculating times at each point
    times = {}
    for driver, tel in driver_tel.items():
        times[driver] = np.interp(distance, tel["Distance"], tel["Time"].dt.total_seconds())
# Getting each mini sector time
    mini_sector = {}
    for driver, t in times.items():
        mini_sector[driver] = np.diff(t)
# Finding fastest driver in each mini sector
    fastest_drivers = []
    for i in range (len(distance)-1):
        fastest_driver = min(mini_sector, key=lambda d:mini_sector[d][i])
        fastest_drivers.append(fastest_driver)
# Building the track line
    x = np.interp(distance,reference_tel["Distance"],reference_tel["X"])
    y= np.interp(distance,reference_tel["Distance"],reference_tel["Y"])
    points = np.array([x,y]).T.reshape(-1,1,2)
    segments=np.concatenate([points[:-1], points[1:]], axis=1)
# Assing driver colors
    driver_colors = {}
    see_colors = {}
    for driver in drivers:
        color = fastf1.plotting.get_driver_color(driver, session=race)
        if color in see_colors:
            driver_colors[driver] = "#{:06x}".format(random.randint(0,0xFFFFFF))
        else:
            driver_colors[driver] = color
            see_colors[color] = driver
# Building the plot
    fig, ax = plt.subplots(figsize=(12, 7))
    base = LineCollection(segments, linewidth=8, alpha = 0.7, colors="white")
    ax.add_collection(base)
# Racing line
    for driver in drivers:
        driver_segments = [segments[i] for i, winner in enumerate(fastest_drivers) if winner == driver]
        line = LineCollection(driver_segments, colors=driver_colors[driver] , linewidth=6, capstyle="round")
        ax.add_collection(line)
    legend_elements =[Line2D([0], [0], color = driver_colors[driver], label=driver, lw=5) for driver in drivers]
# The corner numbers
    circuit = race.get_circuit_info()
    corners = circuit.corners
    for _, corner in corners.iterrows():
        ax.text(corner["X"], corner["Y"], str(corner["Number"]), color="black", fontsize=8, weight="bold", ha="center", va="center")
# Formating everything
    ax.axis("equal")
    ax.axis("off")
    ax.legend(handles=legend_elements, loc="upper left")
    plt.title(f"{year} {event} {session_type} Fastest Lap Track Domination Comparison Plot", color="red", fontsize=16, fontweight="bold")
    fig. tight_layout()
    return fig
