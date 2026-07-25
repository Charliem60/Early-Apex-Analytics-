# First we need to import the necessary libraries. We will use matplotlib for plotting and fastf1 for accessing the Formula 1 data.
from matplotlib import pyplot as plt
import backend.fastf1data as fastf1data
from backend.fastf1data import plotting
import seaborn as sns
from matplotlib.ticker import MultipleLocator

# Enables patches for plotting time values and loads dark colour theme.
fastf1data.plotting.setup_mpl(mpl_timeddelta_support=True, color_scheme='fastf1')
# Loading the session data and inmputing the race you want to investigate
year = int(input("Enter the year (eg 2022): "))
event = input("Enter the race name in full (eg 'Austrian Grand Prix'): ")
session_type = "R"
race = fastf1data.get_session(year, event, session_type)
race.load()
strategy_laps = race.laps
laps = race.laps.pick_quicklaps()

fig, ax = plt.subplots(figsize=(9.0, 5.0))

# First graph - Showing position changes during a race
for driver in race.drivers:
    driver_laps = race.laps.pick_drivers(driver)

    if driver_laps.empty:
        continue

    abb = driver_laps["Driver"].iloc[0]
    style = fastf1data.plotting.get_driver_style(identifier = abb,
                                             style=["color", "linestyle"],
                                             session = race)
    ax.plot(driver_laps["LapNumber"], driver_laps["Position"], label = abb, **style)

# Setting up the axis
ax.set_ylim(20.5,0.5)
ax.set_yticks(range(1,23))
ax.set_xlabel("Lap")
ax.set_ylabel("Position")
ax.set_title(f"{event} {year} - Race Position Changes", fontsize=22, pad=30, color="red")
# Add legend
ax.legend(bbox_to_anchor=(1.02,1), loc="upper left", title="Drivers", fontsize=10,ncol=1)
plt.tight_layout()
plt.grid(linewidth = 0.5, color = "yellow", alpha = 0.5, linestyle="--")

# Now a tyre stragedy plot
drivers = race.drivers
drivers = [race.get_driver(driver)["Abbreviation"] for driver in drivers]


stints = strategy_laps[["Driver", "Stint", "Compound", "LapNumber", "FreshTyre"]]
stints=stints.dropna(subset=["Compound", "Stint"])
stints = stints.groupby(["Driver", "Stint", "Compound", "FreshTyre"]).count().reset_index()
stints = stints.rename(columns={"LapNumber": "StintLength"})

# Now we can plot the stragedies
fig1, ax1, = plt.subplots(figsize=(12,8))
for driver in drivers:
    driver_stints = stints[stints["Driver"] == driver]
    if driver_stints.empty:
        continue

    previous_stint_end = 0

    for _, row in driver_stints.iterrows():

        compound_color = fastf1data.plotting.get_compound_color(
            row["Compound"],
            session=race
        )

        hatch = "" if row["FreshTyre"] else "xx"

        ax1.barh(
            y=driver,
            width=row["StintLength"],
            left=previous_stint_end,
            color=compound_color,
            edgecolor="black",
            hatch=hatch
        )

        ax1.text(
            previous_stint_end + row["StintLength"] / 2,
            driver,
            str(row["StintLength"]),
            ha="center",
            va="center",
            fontsize=8,
            fontweight="bold",
            color="black" if row["Compound"] == "HARD" else "white",
            bbox=dict(
                boxstyle="circle, pad=0.2",
                fc = "grey",
                ec="none"
            )
        )

        previous_stint_end += row["StintLength"]
        
# Making the plot more readable
# Adding a legend
from matplotlib.patches import Patch

legend_elements = [
    Patch(
        facecolor=fastf1data.plotting.get_compound_color("SOFT", session=race),
        edgecolor="black",
        label="Soft"
    ),
    Patch(
        facecolor=fastf1data.plotting.get_compound_color("MEDIUM", session=race),
        edgecolor="black",
        label="Medium"
    ),
    Patch(
        facecolor=fastf1data.plotting.get_compound_color("HARD", session=race),
        edgecolor="black",
        label="Hard"
    ),
    Patch(
        facecolor=fastf1data.plotting.get_compound_color("INTERMEDIATE", session=race),
        edgecolor="black",
        label="Intermediate"
    ),
    Patch(
        facecolor=fastf1data.plotting.get_compound_color("WET", session=race),
        edgecolor="black",
        label="Wet"
    ),
    Patch(
        facecolor="white",
        edgecolor="black",
        hatch="xx",
        label="Used tyre"
    )
]


fig1.suptitle(f"{event} {year} - Race Strategies", fontsize=20, y=0.96, fontweight="bold", color = "red")
ax1.legend(handles=legend_elements, title="Tyre Compounds", loc="upper center", bbox_to_anchor=(0.5, 1.04), ncol=7, frameon=False)
ax1.invert_yaxis()
ax1.set_xlabel("Lap Number")

ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax1.set_xlim(0, race.total_laps)
ax1.xaxis.set_major_locator(MultipleLocator(10))
ax1.xaxis.set_minor_locator(MultipleLocator(1))
plt.grid(linewidth = 0.5, color = "yellow", alpha = 0.5, linestyle="--")


# Now for a pace comparison between teammates
race_laps = laps.copy()
# Removing pitstops
race_laps = race_laps[~race_laps["PitInTime"].notna() & ~race_laps["PitOutTime"].notna()]
race_laps["LapTime"] = race_laps["LapTime"].dt.total_seconds()
# Ordering from fastest to slowest
team_order = (race_laps.groupby("Team")["LapTime"]
              .median().sort_values().index)
# Making color pallet
teams_colors = {team: fastf1data.plotting.get_team_color(team, session=race) for team in team_order}

# Now for the graph
fig2, ax2 = plt.subplots(figsize=(12, 8))
sns.boxplot(
    data = race_laps,
    x = "Team",
    y = "LapTime",
    order = team_order,
    hue = "Team",
    palette = teams_colors,
    whiskerprops=dict(color="red"),
    boxprops=dict(edgecolor = "black"),
    medianprops=dict(color="red"),
    capprops=dict(color = "red"),
    showfliers=False
    )
# Setting axises
ax2.set_title(f"{event} {year} - Team Race Pace Distribution", fontsize=22, pad=30, color="red")
ax2.set(xlabel=None)
ax2.set_ylabel("Lap Times (seconds)")
plt.grid(linewidth = 0.5, color = "yellow", alpha = 0.5, linestyle="--")




# Now for a plot that shows the gap to the race leader from all cars across the course of the race
race_winner = race.results.iloc[0]["Abbreviation"]
ref_laps = race.laps.pick_driver(race_winner)[["LapNumber", "Time"]]
ref_laps = ref_laps.rename(columns={"Time": "RefTime"})
# Setting things up
fig3, ax3 = plt.subplots(figsize=(14,10))

for driver in race.drivers:
    drive = race.laps.pick_driver(driver)[["LapNumber", "Driver", "Time"]]
    if drive.empty:
        continue
    drive = drive.merge(ref_laps, on="LapNumber", how="left")
    drive["Gap"] = (drive["RefTime"] - drive["Time"]).dt.total_seconds()
    abb = drive["Driver"].iloc[0]

    style = fastf1data.plotting.get_driver_style(abb,session=race, style=["color", "linestyle"])
    ax3.plot(drive["LapNumber"], drive["Gap"], linewidth=2, label=abb, **style)

ax3.set_title(f"Race Gaps to leader during the {year} {event}", color = "red")
ax3.set_xlabel("Lap")
ax3.set_ylabel("Gap (s)")
ax3.grid(linewidth = 0.5, color = "yellow", alpha = 0.5, linestyle="--")
ax3.legend(bbox_to_anchor=(1.02,1), loc="upper left")


plt.tight_layout()
plt.show()
