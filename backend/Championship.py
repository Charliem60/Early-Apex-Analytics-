# First we need to import the necessary libraries. We will use matplotlib for plotting and fastf1 for accessing the Formula 1 data.
import backend.fastf1 as fastf1
import fastf1.plotting
from fastf1.ergast import Ergast
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.io import show
from plotly.subplots import make_subplots


# Enables patches for plotting time values and loads dark colour theme.
fastf1.plotting.setup_mpl(mpl_timeddelta_support=True, color_scheme='fastf1')
# Loading the session data and inmputing the season you want to investigate
SEASON = int(input("Enter the season you want to inspect: "))
ROUND = int(input("Enter the Round you are investigating from: "))
# Setting everything ip
def get_drivers_standings():
    ergast = Ergast()
    standings = ergast.get_driver_standings(season=SEASON, round=ROUND)
    return standings.content[0]

def calculate_max_points_for_rest_of_season():
    Points_Sprint = 33
    Points_Conventional = 25

    events = fastf1.events.get_event_schedule(SEASON, backend = "ergast")
    print(events[["RoundNumber", "EventName", "EventFormat"]])
    print(events["EventFormat"].unique())
    events = events[events['RoundNumber'] > ROUND]

    sprint_events = len(events.loc[events["EventFormat"] == "sprint_qualifying"])
    conventional_event = len(events.loc[events["EventFormat"]== "conventional"])

    sprint_points = Points_Sprint * sprint_events
    conventional_points = conventional_event * Points_Conventional
    return sprint_points + conventional_points

def calculate_who_can_win(drivers_standings, max_points):
    Leader_Points = int(drivers_standings.loc[0]['points'])
    for i, _ in enumerate(drivers_standings.iterrows()):
        driver = drivers_standings.loc[i]
        driver_max_points = int(driver["points"]) + max_points
        can_Win = "No" if driver_max_points < Leader_Points else "Yes"
        
        print(f"{driver['position']}:{driver['givenName']} {driver['familyName']},"
          f"Current Points: {driver['points']},"
          f"Theoretical maximum points: {driver_max_points},"
          f"Can win: {can_Win}"
        )   
# Current driver standings
driver_stands = get_drivers_standings()
# Get maximum amount of points
points = calculate_max_points_for_rest_of_season()
print(points)
# Print which drivers can still win
calculate_who_can_win(driver_stands, points)
# Plotting a graph about this
drivers = []
current = []
colors = []
status = []

leader_points = int(driver_stands.loc[0]["points"])
                    
for i in range(len(driver_stands)):
    driver = driver_stands.loc[i]
    current_points = int(driver["points"])
    drivers.append(driver["familyName"])
    current.append(current_points)

    # Dealng with the colour current bars
    if current_points + points >= leader_points:
        colors.append("green")
        status.append("Alive")
    else:
        colors.append("gold")
        status.append("Eliminated")

# Remaining points
maximum = [p + points for p in current]
plt.figure(figsize=(12, 8))

plt.bar(drivers, maximum, color = "grey", alpha=0.45, label="Maximum Points Availible")
plt.bar(drivers, current, color=colors, label = "Current Points")
for i, (max_points, state) in enumerate(zip(maximum, status)):
    plt.text(i, max_points + 5, state, ha="center", fontsize=9, color = "white")
plt.axhline(leader_points, color = "gold", linestyle = "--", linewidth=4, label = "Leader's Current Points")
plt.xticks(rotation=45)
plt.ylabel("Championship Points")
plt.xlabel("Drivers")
plt.title(f"{SEASON} Drivers Championship Standings - Who can still write history?", color = "red")
plt.legend()
plt.tight_layout()
plt.show()


# Season Summery Visiual
season =  int(input("Enter an F1 season here: "))
schedule = fastf1.get_event_schedule(season, include_testing=False)

standings = []
short_race_names = []

for _, event in schedule.iterrows():
    event_name, round_number = event["EventName"], event["RoundNumber"]
    short_race_names.append(event_name.replace("Grand Prix", "").strip())
    # Getting the results from each race
    race = fastf1.get_session(season, event_name, "R")
    race.load(laps=False, telemetry=False, weather=False, messages=False)
    # Adding sprint points
    sprint = None
    if event["EventFormat"] == "sprint_qualifying":
        sprint = fastf1.get_session(season, event_name, "S")
        sprint.load(laps=False, telemetry=False, weather=False, messages=False)
    
    for _, driver_row in race.results.iterrows():
        abbreviation, race_points, race_position = ( driver_row["Abbreviation"], driver_row["Points"], driver_row["Position"],)
        sprint_points = 0
        if sprint is not None:
            driver_row = sprint.results[sprint.results["Abbreviation"] == abbreviation]
            if not driver_row.empty:
                sprint_points = driver_row["Points"].values[0]
        
        standings.append(
            {
            "EventName": event_name,
            "RoundNumber": round_number,
            "Driver": abbreviation,
            "Points": race_points + sprint_points,
            "Position" :  race_position,
            }
        )
# Dealing with the dataframe
df = pd.DataFrame(standings)
# Positining the championship order and the columns to be displayed
heatmap_data = df.pivot(index="Driver", columns="RoundNumber", values="Points").fillna(0)
heatmap_data["total_points"] = heatmap_data.sum(axis=1)
heatmap_data = heatmap_data.sort_values(by="total_points", ascending=True)
total_points = heatmap_data["total_points"].values
heatmap_data = heatmap_data.drop(columns=["total_points"])
position_data = df.pivot(index="Driver", columns="RoundNumber", values="Position").fillna("N/A")
hover_info=[
    [
        {
            "position": position_data.at[driver, race],
        }
        for race in schedule["RoundNumber"]
    ]
    for driver in heatmap_data.index
]
# Creating the subplots for the headings created
fig = make_subplots(rows=1, cols=2, column_widths=[0.90, 0.20], subplot_titles=(f"F1 {season} Drivers Championship Standings", "Total Points",))
fig.update_layout(width=1300, height=800, template="plotly_dark")
# Crafting the plot
fig.add_trace(
    go.Heatmap(
        x = short_race_names,
        y = heatmap_data.index,
        z = heatmap_data.values,
        text = heatmap_data.values,
        texttemplate="%{text}",
        textfont={"size": 14},
        customdata=hover_info,
        hovertemplate=(
            "Driver: %{y}<br>"
            "Race Name: %{x}<br>"
            "Points: %{z}<br>"
            "Position: %{customdata.position}<extra></extra>" 
        ),
        colorscale="Turbo",
        showscale=False,
        zmin=0,
        zmax=heatmap_data.values.max(),
    ),
    row=1,
    col=1,
)
# Heatmap for the season summery
fig.add_trace(
    go.Heatmap(
        x=["Total Points"]*len(total_points),
        y = heatmap_data.index,
        z= total_points,
        text=total_points,
        texttemplate="%{text}",
        textfont={"size": 14},
        colorscale="Turbo",
        zmin=0,
        showscale=False,
        zmax=total_points.max(),
    ),
    row=1,
    col=2,
)
champion = len(heatmap_data.index)-1
fig.add_shape(type="rect", x0=-0.5, x1 = len(short_race_names)-0.5, y0=champion-0.5, y1=champion+0.5, line=dict(color="gold", width=4), fillcolor="rgba(0,0,0,0)")
show(fig)


# Season Summery Visiual but for the constructers championship
standings = []
short_race_names = []

for _, event in schedule.iterrows():
    event_name, round_number = event["EventName"], event["RoundNumber"]
    short_race_names.append(event_name.replace("Grand Prix", "").strip())
    # Getting the results from each race
    race = fastf1.get_session(season, event_name, "R")
    race.load(laps=False, telemetry=False, weather=False, messages=False)
    # Adding sprint points
    sprint = None
    if event["EventFormat"] == "sprint_qualifying":
        sprint = fastf1.get_session(season, event_name, "S")
        sprint.load(laps=False, telemetry=False, weather=False, messages=False)
    # Storing all the points for each driver in each team
    for _, driver_row in race.results.iterrows():
        abbreviation = (driver_row["Abbreviation"])
        team = driver_row["TeamName"]
        race_points = driver_row["Points"]
        sprint_points = 0
        if sprint is not None:
            sprint_driver = sprint.results[sprint.results["Abbreviation"] == abbreviation]
            if not sprint_driver.empty:
                sprint_points = sprint_driver["Points"].values[0]
        
        standings.append(
            {
            "EventName": event_name,
            "RoundNumber": round_number,
            "Team": team,
            "Points": race_points + sprint_points,
            }
        )
# Dealing with the dataframe
df = pd.DataFrame(standings)
# Sum drivers points for each time
df = (df.groupby(["RoundNumber", "EventName", "Team"], as_index=False)["Points"].sum())
# Positining the championship order and the columns to be displayed
heatmap_data = df.pivot(index="Team", columns="RoundNumber", values="Points").fillna(0)
heatmap_data["total_points"] = heatmap_data.sum(axis=1)
heatmap_data = heatmap_data.sort_values(by="total_points", ascending=True)
total_points = heatmap_data["total_points"].values
heatmap_data = heatmap_data.drop(columns=["total_points"])
#Creating the subplots for the headings created
fig = make_subplots(rows=1, cols=2, column_widths=[0.90, 0.20], subplot_titles=(f"F1 {season} Constructers Championship Standings", "Total Points",))
fig.update_layout(width=1300, height=800, template="plotly_dark")
# Crafting the plot
fig.add_trace(
    go.Heatmap(
        x = short_race_names,
        y = heatmap_data.index,
        z = heatmap_data.values,
        text = heatmap_data.values,
        texttemplate="%{text}",
        textfont={"size": 14},
        hovertemplate=(
            "Constructer: %{y}<br>"
            "Race Name: %{x}<br>"
            "Points: %{z}<br>" 
        ),
        colorscale="Turbo",
        showscale=False,
        zmin=0,
        zmax=heatmap_data.values.max(),
    ),
    row=1,
    col=1,
)
# Heatmap for the season summery
fig.add_trace(
    go.Heatmap(
        x=["Total Points"]*len(total_points),
        y = heatmap_data.index,
        z= total_points,
        text=total_points,
        texttemplate="%{text}",
        textfont={"size": 14},
        colorscale="Turbo",
        zmin=0,
        showscale=False,
        zmax=total_points.max(),
        hovertemplate=(
            "Constructer: %{y}<br>"
            "Total Points: %{z}<extra></extra>"
        ),
    ),
    row=1,
    col=2,
)
champion = len(heatmap_data.index)-1
fig.add_shape(type="rect", x0=-0.5, x1 = len(short_race_names)-0.5, y0=champion-0.5, y1=champion+0.5, line=dict(color="gold", width=4), fillcolor="rgba(0,0,0,0)")
show(fig)
