import fastf1 as fastf1
import fastf1.plotting
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.collections import LineCollection
import matplotlib as mpl

# Enables patches for plotting time values and loads dark colour theme.
fastf1.plotting.setup_mpl(mpl_timeddelta_support=True, color_scheme='fastf1')
def create_track_visuals(year, event, session_type, drivers):
    race = fastf1.get_session(year, event, session_type)
    race.load()


    fig, axes = plt.subplots(2, 2, figsize=(10,10))
    axes = axes.flatten()

    for ax, driver in zip(axes, drivers):
        laps = race.laps.pick_drivers(driver).pick_fastest()
        if laps is None:
            print(f"No Data for {driver}")
            continue

        lap_time = laps["LapTime"]
        mins = int(lap_time.total_seconds()//60)
        secs = lap_time.total_seconds()%60
        lap_time = f"{mins}:{secs:06.3f}"
        tel = laps.get_telemetry()
    # Prepare the data for plotting by converting to numpy
        x = tel["X"].to_numpy()
        y = tel["Y"].to_numpy()
        points = np.array([x,y]).T.reshape(-1,1,2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        gear = tel["nGear"].to_numpy().astype(float)
        # Merging the colormap
        cmap = colormaps["Paired"]
        lc_comp = LineCollection(segments, norm=plt.Normalize(1, 8), cmap=cmap)
        lc_comp.set_array(gear)
        lc_comp.set_linewidth(4)

        ax.add_collection(lc_comp)

        ax.axis("equal")
        ax.axis("off")
        ax.set_anchor("C")
        ax.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)
        ax.set_title(f"{laps['Driver']} - {lap_time} - {year} {race.event['EventName']}", color="green", fontsize=10)
# Adding a colorbar to the plot
    active_axes = axes[:len(drivers)]
    for ax in axes[len(drivers):]:
        ax.set_visible(False)

    cbar = fig.colorbar(lc_comp, ax=axes.tolist(), orientation="horizontal", shrink=0.4, pad=0.04)
    cbar.set_label("Gear")
    cbar.set_ticks(np.arange(1.5,9.5))
    cbar.set_ticklabels(np.arange(1,9))
    title = fig.suptitle(f"Fastest Lap Gear Shift Visualisation in Qualifying", color="red", fontsize=16, y=0.98)

# Now for a speed visualization on a track map graph!
    fig1, axes2 = plt.subplots(2, 2, figsize=(10,10))
    axes2 = axes2.flatten()

    for ax, driver in zip(axes2, drivers):
        laps = race.laps.pick_drivers(driver).pick_fastest()
        if laps is None:
            print(f"No Data for {driver}")
            continue

        lap_time = laps["LapTime"]
        mins = int(lap_time.total_seconds()//60)
        secs = lap_time.total_seconds()%60
        lap_time = f"{mins}:{secs:06.3f}"
        tel = laps.get_telemetry()
    # Prepare the data for plotting by converting to numpy
        x = tel["X"].to_numpy()
        y = tel["Y"].to_numpy()
        color = tel['Speed'].to_numpy()
        points = np.array([x,y]).T.reshape(-1,1,2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        gear = tel["nGear"].to_numpy().astype(float)
    # Merging the colormap
        colormap = mpl.cm.plasma
        track_outline = LineCollection(segments, colors="black", linewidth=10, linestyle="--")
        track_outline.set_capstyle("round")
        track_outline.set_joinstyle("round")
        norm = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
        lc = LineCollection(segments, cmap=colormap,norm=norm, linestyle="--", linewidths=8)
        lc.set_array(color)
        outline = ax.add_collection(track_outline)
        line = ax.add_collection(lc)
    # Creating the color bar
        ax.axis("equal")
        ax.axis("off")
        ax.set_anchor("C")
        ax.set_title(f"{laps['Driver']} - {lap_time} - {year} {race.event['EventName']}", color="green", fontsize=10)
# Adding a colorbar to the plot
    active_axes = axes[:len(drivers)]
    for ax in axes[len(drivers):]:
        ax.set_visible(False)
    fig1.colorbar(lc, ax=axes2.tolist(), orientation="horizontal", label = "Speed (km/h)", shrink=0.4, pad=0.04)
    title = fig1.suptitle(f"Fastest Lap Speed Visualisation in Qualifying", color="red", fontsize=16, y=0.98)
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    fig1.subplots_adjust(hspace=0.3, wspace=0.3)

    return fig, fig1 



