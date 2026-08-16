# First we need to import the necessary libraries. We will use matplotlib for plotting and fastf1 for accessing the Formula 1 data.
# Pandas will organise it into DataFrames. Plotly makes it interactive and NumPy is used for numerical operations such as race results and so on.
import fastf1 as fastf1
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
# Loading the season data from whatever the user chose.
def create_championship_plots(SEASON):
# Season Summery Visiual DRIVERS CHAMPIONSHIP
# Storing championship information after fetching the schedule. Don't include testing results!
    schedule = fastf1.get_event_schedule(SEASON, include_testing=False)
    standings = []
    short_race_names = []
    # Going through every event in selected season and shortening the race names
    for _, event in schedule.iterrows():
        event_name, round_number = event["EventName"], event["RoundNumber"]
        short_race_names.append(event_name.replace("Grand Prix", "").strip())
    # Getting the results from each race and disabling telemetry, weather and data we don't need.
        race = fastf1.get_session(SEASON, event_name, "R")
        race.load(laps=False, telemetry=False, weather=False, messages=False)
    # Checking if the race has a sprint race and calculating the points required.
        sprint = None
        if event["EventFormat"] == "sprint_qualifying":
            sprint = fastf1.get_session(SEASON, event_name, "S")
            sprint.load(laps=False, telemetry=False, weather=False, messages=False)
    # Storing the championship results for  each driver in the championship
        for _, driver_row in race.results.iterrows():
            abbreviation, race_points, race_position = ( driver_row["Abbreviation"], driver_row["Points"], driver_row["Position"],)
            race_points = driver_row["Points"]
            sprint_points = 0
            if sprint is not None:
             sprint_driver = sprint.results[sprint.results["Abbreviation"] == abbreviation]
             if not sprint_driver.empty:
                 sprint_points = sprint_driver.iloc[0]["Points"]
        # Store the drivers race and sprint points together with their finishing position
            standings.append(
                {
            "EventName": event_name,
            "RoundNumber": round_number,
            "Driver": abbreviation,
            "Points": race_points + sprint_points,
            "Position" :  race_position,
            }
        )
# Converting all these dictionaries into a Pandas Dataframe to organise the data
    df = pd.DataFrame(standings)
# Positining the championship order and the columns to be displayed in the dataframe
    heatmap_data = df.pivot(index="Driver", columns="RoundNumber", values="Points").fillna(0)
    heatmap_data["total_points"] = heatmap_data.sum(axis=1)
    heatmap_data = heatmap_data.sort_values(by="total_points", ascending=True)
    total_points = heatmap_data["total_points"].values
    heatmap_data = heatmap_data.drop(columns=["total_points"])
    position_data = df.pivot(index="Driver", columns="RoundNumber", values="Position").fillna("N/A")
# Setting up the information for when you hover your curser over the graph
    hover_info=[
        [
            {
                "position": position_data.at[driver, race],
            }
            for race in schedule["RoundNumber"]
        ]
        for driver in heatmap_data.index
    ]
# Creating the figure for the actual graph that will display both the season summery and final championship standings. Creating the layout and the visuals
    fig = make_subplots(rows=1, cols=2, column_widths=[0.90, 0.20], subplot_titles=(f"F1 {SEASON} Drivers Championship Standings", "Total Points"))
    fig.update_layout(width=1300, height=800, template="plotly_dark")
# Adding the race by race heat map and the information in each cell, linking it to the hover display and so on.
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
    # This is a near enough identical heatmap as above but this time it is for the final championship graph.
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
    # Identifies the champion
    champion = len(heatmap_data.index)-1
    fig.add_shape(type="rect", x0=-0.5, x1 = len(short_race_names)-0.5, y0=champion-0.5, y1=champion+0.5, line=dict(color="gold", width=4), fillcolor="rgba(0,0,0,0)")
    fig.update_layout(
        font=dict(color="#4BA3C3")
    )
    #Store the completed graph
    fig2=fig


# Season Summery Visiual but for the constructers championship
    # Reset the standings so that the same process can occur for this new graph. Most of this process is the same as before.
    standings = []
    short_race_names = []
    # Going through the results again, adding sprint points, shortening the race names, storing all the points, just as before.
    for _, event in schedule.iterrows():
        event_name, round_number = event["EventName"], event["RoundNumber"]
        short_race_names.append(event_name.replace("Grand Prix", "").strip())
        race = fastf1.get_session(SEASON, event_name, "R")
        race.load(laps=False, telemetry=False, weather=False, messages=False)

        sprint = None
        if event["EventFormat"] == "sprint_qualifying":
            sprint = fastf1.get_session(SEASON, event_name, "S")
            sprint.load(laps=False, telemetry=False, weather=False, messages=False)

        for _, driver_row in race.results.iterrows():
            abbreviation = (driver_row["Abbreviation"])
            team = driver_row["TeamName"]
            race_points = driver_row["Points"]
            sprint_points = 0
            if sprint is not None:
                sprint_driver = sprint.results[sprint.results["Abbreviation"] == abbreviation]
                if not sprint_driver.empty:
                    sprint_points = sprint_driver.iloc[0]["Points"]
        
            standings.append(
                {
                "EventName": event_name,
                "RoundNumber": round_number,
                "Team": team,
                "Points": race_points + sprint_points,
                }
        )
# Converting all these dictionaries into a Pandas Dataframe to organise the data
    df = pd.DataFrame(standings)
# Sum drivers points for each race because each team has two drivers so their points have to added after each race.
    df = (df.groupby(["RoundNumber", "EventName", "Team"], as_index=False)["Points"].sum())
# Positining the championship order and the columns to be displayed
    heatmap_data = df.pivot(index="Team", columns="RoundNumber", values="Points").fillna(0)
    heatmap_data["total_points"] = heatmap_data.sum(axis=1)
    heatmap_data = heatmap_data.sort_values(by="total_points", ascending=True)
    total_points = heatmap_data["total_points"].values
    heatmap_data = heatmap_data.drop(columns=["total_points"])
#Creating the figure for the actual graph that will display both the season summery and final championship standings. Creating the layout and the visuals
    fig = make_subplots(rows=1, cols=2, column_widths=[0.90, 0.20], subplot_titles=(f"F1 {SEASON} Constructers Championship Standings", "Total Points"))
    fig.update_layout(width=1300, height=800, template="plotly_dark")
# Adding the race by race heat map and the information in each cell, linking it to the hover display and so on.
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
# This is a near enough identical heatmap as above but this time it is for the final championship graph
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
    # Highlighting the champion oncemore
    champion = len(heatmap_data.index)-1
    fig.add_shape(type="rect", x0=-0.5, x1 = len(short_race_names)-0.5, y0=champion-0.5, y1=champion+0.5, line=dict(color="gold", width=4), fillcolor="rgba(0,0,0,0)")
    fig.update_layout(
        font=dict(color="#4BA3C3")
    )
    fig3 = fig
    #Displaying the charts on the app
    return fig2, fig3
