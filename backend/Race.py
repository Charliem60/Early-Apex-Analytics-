# First we need to import the necessary libraries. We will use matplotlib for plotting and fastf1 for accessing the Formula 1 data.
from matplotlib import pyplot as plt
import fastf1 as fastf1
from fastf1 import plotting
import seaborn as sns
from matplotlib.ticker import MultipleLocator

# Enables patches for plotting time values and loads dark colour theme.
fastf1.plotting.setup_mpl(mpl_timeddelta_support=True, color_scheme='fastf1')
# finding the user inputed session, year and so on for the race and loading it. Creating the quick laps and setting the frames up for the strategy plot.
def create_race_traces(year, event, session_type, drivers=None):
    race = fastf1.get_session(year, event, session_type)
    race.load()
    strategy_laps = race.laps
    laps = race.laps.pick_quicklaps()
    fig, ax = plt.subplots(figsize=(11,7))

# First graph - Showing position changes during a race.
    for driver in race.drivers:
        driver_laps = race.laps.pick_drivers(driver)
        # If a driver has no laps...
        if driver_laps.empty:
            continue
        # Getting the driver style and finding the position of each driver every lap and plotting it.
        abb = driver_laps["Driver"].iloc[0]
        style = fastf1.plotting.get_driver_style(identifier = abb,
                                             style=["color", "linestyle"],
                                             session = race)
        ax.plot(driver_laps["LapNumber"], driver_laps["Position"], label = abb, **style)

# Setting up the axis in the style of the app.
    ax.set_ylim(20.5,0.5)
    ax.set_yticks(range(1,23))
    ax.set_xlabel("Lap")
    ax.set_ylabel("Position")
    ax.set_title(f"{event} {year} - Race Position Changes", fontsize=22, pad=30, color="#D62839")
# Add legend of all the drivers participating in the race.
    ax.legend(bbox_to_anchor=(1.02,1), loc="upper left", title="Drivers", fontsize=10,ncol=1)
    plt.tight_layout()
    plt.grid(linewidth = 0.5, color = "#4BA3C3", alpha = 0.5, linestyle="--")

# Now a tyre stragedy plot. Getting all the stints and the information from fastf1 about the data throughout the race. Grouping the stints and the infromation.
    race_drivers = [race.get_driver(driver)["Abbreviation"] for driver in race.drivers]
    strategy_laps = race.laps
    stints = strategy_laps[["Driver", "Stint", "Compound", "LapNumber", "FreshTyre"]]
    stints=stints.dropna(subset=["Compound", "Stint"])
    stints = stints.groupby(["Driver", "Stint", "Compound", "FreshTyre"]).count().reset_index()
    stints = stints.rename(columns={"LapNumber": "StintLength"})
# Now we can plot the stragedies and get ready to display it on a bar chart form.
    fig1, ax1, = plt.subplots(figsize=(12,8))
    for driver in race.results["Abbreviation"].dropna():
        driver_stints = stints[stints["Driver"] == driver]
        previous_stint_end = 0  
        for _, row in driver_stints.iterrows():

            compound_color = fastf1.plotting.get_compound_color(
            row["Compound"],
            session=race
        )
        # Giving different styles if drivers are on fresh or old tyres.
            hatch = "" if row["FreshTyre"] else "xx"
        # Setting up the bar chart highlightin the length of each stint.
            ax1.barh(
            y=driver,
            width=row["StintLength"],
            left=previous_stint_end,
            color=compound_color,
            edgecolor="black",
            hatch=hatch
        )
        # Setting up the text of the stints and the size of the stints and the length, the colour and so on.
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
# Adding a legend.
    from matplotlib.patches import Patch
    # Giving colours for each type of tyre that can be used in each race and fetching that data,
    legend_elements = [
        Patch(
        facecolor=fastf1.plotting.get_compound_color("SOFT", session=race),
        edgecolor="black",
        label="Soft"
    ),
        Patch(
        facecolor=fastf1.plotting.get_compound_color("MEDIUM", session=race),
        edgecolor="black",
        label="Medium"
    ),
        Patch(
        facecolor=fastf1.plotting.get_compound_color("HARD", session=race),
        edgecolor="black",
        label="Hard"
    ),
        Patch(
        facecolor=fastf1.plotting.get_compound_color("INTERMEDIATE", session=race),
        edgecolor="black",
        label="Intermediate"
    ),
        Patch(
        facecolor=fastf1.plotting.get_compound_color("WET", session=race),
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
# Now giving the title, setting up the general style of the plot and making the plot more readable.
    fig1.suptitle(f"{event} {year} - Race Strategies", fontsize=20, y=0.96, fontweight="bold", color = "#D62839")
    ax1.legend(handles=legend_elements, title="Tyre Compounds", loc="upper center", bbox_to_anchor=(0.5, 1.04), ncol=7, frameon=False)
    ax1.invert_yaxis()
    ax1.set_xlabel("Lap Number")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax1.set_xlim(0, race.total_laps)
    ax1.xaxis.set_major_locator(MultipleLocator(10))
    ax1.xaxis.set_minor_locator(MultipleLocator(1))
    plt.grid(linewidth = 0.5, color = "#4BA3C3", alpha = 0.5, linestyle="--")


# Now for a pace comparison between every different team to see which teams were quicker in the race. Copying the race laps from before.
    race_laps = laps.copy()
# Removing pitstops that alter the data to be displayed.
    race_laps = race_laps[~race_laps["PitInTime"].notna() & ~race_laps["PitOutTime"].notna()]
    race_laps["LapTime"] = race_laps["LapTime"].dt.total_seconds()
# Ordering from fastest to slowest teams by the pace of their two drivers as they are averaged out.
    team_order = (race_laps.groupby("Team")["LapTime"]
              .median().sort_values().index)
# Making color pallet by fetching the colours of each time.
    teams_colors = {team: fastf1.plotting.get_team_color(team, session=race) for team in team_order}

# Now for the graph. Setting up the labels, the data, all the colours and so on.
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    sns.boxplot(
    data = race_laps,
    x = "Team",
    y = "LapTime",
    order = team_order,
    hue = "Team",
    palette = teams_colors,
    whiskerprops=dict(color="#4BA3C3"),
    boxprops=dict(edgecolor = "black"),
    medianprops=dict(color="#4BA3C3"),
    capprops=dict(color = "#4BA3C3"),
    showfliers=False
    )
# Setting axises and titles and so on.
    ax2.set_title(f"{event} {year} - Team Race Pace Distribution", fontsize=22, pad=30, color="#D62839")
    ax2.set(xlabel=None)
    ax2.set_ylabel("Lap Times (seconds)")
    plt.grid(linewidth = 0.5, color = "#4BA3C3", alpha = 0.5, linestyle="--")

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
        drive["Gap"] = (drive["Time"] - drive["RefTime"]).dt.total_seconds()
        abb = drive["Driver"].iloc[0]

        style = fastf1.plotting.get_driver_style(abb,session=race, style=["color", "linestyle"])
        ax3.plot(drive["LapNumber"], drive["Gap"], linewidth=2, label=abb, **style)

    ax3.set_title(f"Race Gaps to leader during the {year} {event}", color = "#D62839")
    ax3.set_xlabel("Lap")
    ax3.set_ylabel("Gap (s)")
    ax3.grid(linewidth = 0.5, color = "#4BA3C3", alpha = 0.5, linestyle="--")
    ax3.legend(bbox_to_anchor=(1.02,1), loc="upper left")

    # Returning all the four plots to display them onto the app.
    fig.tight_layout()
    fig1.tight_layout()
    fig2.tight_layout()
    fig3.tight_layout()
    return fig, fig1, fig2, fig3
