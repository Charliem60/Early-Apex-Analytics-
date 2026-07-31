#Quali Analysis
# First we need to import the necessary libraries. We will use matplotlib for plotting and fastf1 for accessing the Formula 1 data.
from matplotlib import pyplot as plt
import fastf1 as fastf1
from fastf1 import plotting
from matplotlib.ticker import FuncFormatter, MultipleLocator 
from matplotlib.ticker import PercentFormatter  
import pandas as pd
from timple.timedelta import strftimedelta
from fastf1.core import Laps

# Enables patches for plotting time values and loads dark colour theme.
fastf1.plotting.setup_mpl(mpl_timeddelta_support=True, color_scheme='fastf1')
# Loading the session data and inmputing the race you want to investigate
def create_quali_plots(year, event, session_type, drivers):
    quali = fastf1.get_session(year, event, session_type)
    quali.load()
# Now we get an array of the drivers.
    session_drivers = pd.unique(quali.laps["Driver"])
# Now to find the fastest laps of the session
    lst_fastest_laps = list()
    for driver in session_drivers:
        drivers_fastest_lap = quali.laps.pick_drivers(driver).pick_fastest()
        if drivers_fastest_lap is not None:
            lst_fastest_laps.append(drivers_fastest_lap)
    fastest_laps = Laps(lst_fastest_laps).sort_values(by="LapTime").reset_index(drop=True)
# Dealing with the plots.
    pole_lap = fastest_laps.pick_fastest()
    fastest_laps["Gap"]= (fastest_laps["LapTime"] - pole_lap["LapTime"]).dt.total_seconds()
    pole_in_seconds = pole_lap["LapTime"].total_seconds()
    fastest_laps["GapPercent"]= ((fastest_laps["LapTime"].dt.total_seconds() - pole_in_seconds) / pole_in_seconds)* 100
# Getting the right team colors and names
    team_colors = list()
    for index, lap in fastest_laps.iterlaps():
        color = fastf1.plotting.get_team_color(lap["Team"], session=quali)
        team_colors.append(color)
# Plotting the data
    fig, ax = plt.subplots()
    bars = ax.barh(fastest_laps.index, fastest_laps["Gap"], color=team_colors, edgecolor="black")
    seen_teams = set()
    for bar, (_, lap) in zip(bars, fastest_laps.iterlaps()):
        team = lap["Team"]
        if team in seen_teams:
            bar.set_hatch("\\")
        else:
            seen_teams.add(team)
        
# Celebrating the polesitter!
    bars[0].set_edgecolor("purple")
    bars[0].set_linewidth(4)
# Adding lap time labels
    for i, lap in fastest_laps.iterlaps():

        if i == 0:
            ax.text(0.01, i,
                 strftimedelta(lap["LapTime"], '%m:%s.%ms'), color="white", fontsize=10, va="center", ha="left")
        else:
            ax.text(
            lap["Gap"]+ 0.01,
                i,
                f"+{lap['Gap']:.3f}", va = "center", ha = "left", fontsize=10, color="white")
        
# Setting the y-axis labels to the driver names and inverting the y-axis so that the fastest driver is at the top.
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps["Driver"])
    ax.invert_yaxis()
    def percent_formatter(x, pos):
        return f"{100* x / pole_in_seconds:.2f}%"
    ax.xaxis.set_major_formatter(FuncFormatter(percent_formatter))
    ax.set_xlim(0, fastest_laps["GapPercent"].max() + 0.25)
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="white", linestyle='--', linewidth=1)
    ax.set_xlabel("Gap to Pole Time (Percentage)", fontsize=12, labelpad=20)

# Naming the plot
    poletime = strftimedelta(pole_lap["LapTime"], '%m:%s.%ms')
    ax.set_title(f"{event} {year} - Qualifying Results", fontsize=22, pad=30, color="red")

# Now for a similar bar chat but showing the result of Q1, Q2 and Q3
    results = quali.results.copy()
# Converting the laptimes to seconds 
    for session in ["Q1", "Q2", "Q3"]:
        results[session + "_sec"] = results[session].dt.total_seconds()
    sessions = ["Q1", "Q2", "Q3"]
# Calculating the percentage gaps along the x-axsis.
    max_gap_percent = 0
    for session in sessions:
        data = results.dropna(subset=[session + "_sec"]).copy()
        fastest = data[session + "_sec"].min()
        gap_percent = ((data[session + "_sec"] - fastest)/ fastest) * 100
        max_gap_percent = max(max_gap_percent, gap_percent.max())
#Creating the graph
    fig1, axes = plt.subplots(figsize=(18, 10),ncols=3,sharey=False)
# Plotting each qualifying segment.
    for ax, session in zip(axes, sessions):

        data = results.dropna(subset=[session + "_sec"]).copy()
        data = data.sort_values(session + "_sec")
        fastest_time = data[session + "_sec"].min()
        # Calculating the gaps to and percentages to
        data["GapSeconds"] = (
            data[session + "_sec"] - fastest_time
    )
        data["GapPercent"] = (
        data["GapSeconds"] / fastest_time
    ) * 100
    # Finding the team colors
        colors = [ fastf1.plotting.get_team_color( team, session=quali)for team in data["TeamName"]]
    # Labelling the bars
        bars = ax.barh(data["Abbreviation"],data["GapPercent"],color=colors,edgecolor="black")
    # Hatch second driver
        seen_teams = set()
        for bar, (_, row) in zip(bars, data.iterrows()):
            team = row["TeamName"]
            if team in seen_teams:bar.set_hatch("\\")
            else: seen_teams.add(team)
    # Celebrating the fastest driver.
        bars[0].set_edgecolor("purple")
        bars[0].set_linewidth(3)
    # Adding labels
        for bar, (_, row) in zip(bars, data.iterrows()):
            if row["GapSeconds"] == 0:
                label = strftimedelta(row[session],"%m:%s.%ms")
            else:
                label = f"+{row['GapSeconds']:.3f}s"

            ax.text(
            row["GapPercent"] + 0.02,
            bar.get_y() + bar.get_height()/2,
            label,
            va="center",
            ha="left",
            fontsize=9,
            color="white"
        )

# Formatting the graph and the axises
        ax.set_xlim(0, max_gap_percent + 0.20)
        ax.invert_yaxis()
        ax.set_title(session,fontsize=18,color="red",pad=18)
        ax.set_xlabel("Gap to Session Best (%)",fontsize=10,labelpad=15)
        ax.xaxis.set_major_formatter(PercentFormatter(decimals=1))
        ax.grid(axis="x",linestyle="--",linewidth=0.8,color="white")
        ax.set_axisbelow(True)
        axes[0].set_ylabel("Driver", fontsize=11)
# Giving the plot a title
    fig1.suptitle(f"{event} {year} - Q1, Q2 & Q3 Results",fontsize=20,color="red",y=0.98)
# Compacting it together
    fig1.tight_layout(rect=[0, 0, 1, 0.96])

# Graph of all three sectors and the fastest times
    sector_data = fastest_laps.copy()
# Convering to seconds
    sector_data["S1"] = sector_data["Sector1Time"].dt.total_seconds()
    sector_data["S2"] = sector_data["Sector2Time"].dt.total_seconds()
    sector_data["S3"] = sector_data["Sector3Time"].dt.total_seconds()
# Creating the max percent again
    max_gap_percent_sector = 0
    for col in ["S1", "S2", "S3"]:
        fastest = sector_data[col].min()
        gap_percent_sector = ((sector_data[col] - fastest)/ fastest) * 100
        max_gap_percent_sector= max(max_gap_percent_sector, gap_percent_sector.max())
    sector_data["S3"] = sector_data["Sector3Time"].dt.total_seconds()
#Creating the graph 
    fig2, axes = plt.subplots(figsize=(18, 10),ncols=3,sharey=False)
    sector_names = [("S1", "Sector 1"), ("S2", "Sector 2"), ("S3", "Sector 3")]
# Now to set up the graph similar to before
    for ax, (col, title) in zip(axes, sector_names):
        data = sector_data.sort_values(col).reset_index(drop=True)
        fastest_sector = data[col].min()
        bye_drivers = sector_data.dropna(subset=["S1", "S2", "S3"])

        data["Gap"] = data[col] - fastest_sector
        data["GapPercent"] = ((data[col] - fastest_sector) / fastest_sector) *100
    
     # Finding the team colors
        colors = [ fastf1.plotting.get_team_color( team, session=quali)for team in data["Team"]]
    # Labelling the bars
        bars = ax.barh(data["Driver"],data["GapPercent"],color=colors,edgecolor="black")
    # Hatch second driver
        seen_teams = set()
        for bar, (_, row) in zip(bars, data.iterrows()):
            team = row["Team"]
            if team in seen_teams:bar.set_hatch("\\")
            else: seen_teams.add(team)
    # Celebrating the fastest driver.
        bars[0].set_edgecolor("purple")
        bars[0].set_linewidth(3)
     # Adding labels
        for bar, (_, row) in zip(bars, data.iterrows()):
            if row["Gap"]==0:
                label = f"{row[col]:.3f}s"
            else:
                label = f"+{row['Gap']:.3f}s"
            ax.text(
            row["GapPercent"] + 0.02,
            bar.get_y() + bar.get_height()/2,
            label,
            va="center",
            ha="left",
            fontsize=9,
            color="white"
        )
# Formatting the graph and the axises
        ax.set_xlim(0, max_gap_percent_sector + 0.20)
        ax.invert_yaxis()
        ax.set_title(title,fontsize=18,color="red",pad=18)
        ax.set_xlabel("Gap to Fastest Sector (%)",fontsize=10,labelpad=15)
        ax.xaxis.set_major_formatter(PercentFormatter(decimals=1))
        ax.grid(axis="x",linestyle="--",linewidth=0.8,color="white")
        ax.set_axisbelow(True)
        axes[0].set_ylabel("Driver", fontsize=11)
# Giving the plot a title
    fig2.suptitle(f"{event} {year} - Sector Segment Results",fontsize=20,color="red",y=0.98)
# Compacting it together
    fig2.tight_layout(rect=[0, 0, 1, 0.96])


# Actual vs Best possible laptimes for each driver
    ideal_laps= []
    for driver in drivers:
        laps = quali.laps.pick_drivers(driver)
        laps = laps.dropna(subset=["Sector1Time", "Sector2Time", "Sector3Time"])
        if laps.empty:
            continue
    # Gettng the fastest laps
        fastest_fastest_lap = laps.pick_fastest()
        ideal_time = (laps["Sector1Time"].min() +laps["Sector2Time"].min() +  laps["Sector3Time"].min())
        ideal_laps.append({"Driver": driver, "Team": fastest_fastest_lap["Team"], "Actual": fastest_fastest_lap["LapTime"], "Ideal": ideal_time})

    ideal_df = pd.DataFrame(ideal_laps)
    ideal_df["ActualSec"] = ideal_df["Actual"].dt.total_seconds()
    ideal_df["IdealSec"] = ideal_df["Ideal"].dt.total_seconds()
# Getting the actual fastest laps
    fastest_actual = ideal_df["ActualSec"].min()
    fastest_ideal = ideal_df["IdealSec"].min()
# Gap calculations
    ideal_df["ActualGap"] = ideal_df["ActualSec"] - fastest_actual
    ideal_df["IdealGap"] = ideal_df["IdealSec"] - fastest_ideal
# Time on the table
    ideal_df["TimeLeft"] = (ideal_df["ActualSec"] - ideal_df["IdealSec"])
# Sorting the dataframes
    actual_order = ideal_df.sort_values("ActualGap").reset_index(drop=True)
    ideal_order = ideal_df.sort_values("IdealGap").reset_index(drop=True)
# Colors
    actual_colors = [fastf1.plotting.get_team_color(team, session=quali) for team in actual_order["Team"]]
    ideal_colors = [fastf1.plotting.get_team_color(team, session=quali) for team in ideal_order["Team"]]
# Time to plot the graph hahah!
    fig3,(ax1, ax2) = plt.subplots(1, 2, figsize=(18,10))
# Actual order plot
    bars = ax1.barh(
        actual_order["Driver"],
        actual_order["ActualGap"], color = actual_colors, edgecolor = "black")
# Hatch second driver
    seen_teams = set()
    for bar, team in zip(bars, actual_order["Team"]):
        if team in seen_teams:
            bar.set_hatch("\\")
        else: 
            seen_teams.add(team)
# Celebrating the fastest driver.
    bars[0].set_edgecolor("purple")
    bars[0].set_linewidth(3)
# Adding labels
    for bar, (_, row) in zip(bars, actual_order.iterrows()):
        if row["ActualGap"]==0:
            label = strftimedelta(row["Actual"], "%m:%s.%ms")
        else:
            label = f"+{row['ActualGap']:.3f}s"
        ax1.text(
            row["ActualGap"] + 0.02,
            bar.get_y() + bar.get_height()/2,
            label,
            va="center",
            ha="left",
            fontsize=9,
            color="white"
    )
# Setting up the axies and the titles
    ax1.invert_yaxis()
    ax1.set_xlabel("Gap to Fastest Actual Lap (s)")
    ax1.set_title("Actual LapTime Order", fontsize= 14, color = "red")
    ax1.grid(axis="x",linestyle="--",linewidth=0.8,color="white")
    ax1.set_axisbelow(True)
# Ideal Order Plot
    bars = ax2.barh(
        ideal_order["Driver"],
        ideal_order["IdealGap"], color = ideal_colors, edgecolor = "black")
# Hatch second driver
    seen_teams = set()
    for bar, team in zip(bars, ideal_order["Team"]):
        if team in seen_teams:
            bar.set_hatch("\\")
        else: 
            seen_teams.add(team)
# Celebrating the fastest driver.
    bars[0].set_edgecolor("purple")
    bars[0].set_linewidth(3)

    ax2.barh(ideal_order["Driver"], ideal_order["TimeLeft"], left = ideal_order["IdealGap"], color = "gold", hatch = "//", edgecolor = "black" , label = "Gap To Actual Lap")

# Adding labels
    for i, row in ideal_order.iterrows():
        ax2.text(
            row["IdealGap"] + row["TimeLeft"] + 0.01,
        i, f"{row['TimeLeft']:.3f}s",
        va = "center", color = "gold", fontsize = 9,
        )
# Setting up the axies and the titles
    ax2.invert_yaxis()
    ax2.set_xlabel("Gap to Fastest Ideal Lap (s)")
    ax2.set_title("Ideal LapTime Order", fontsize= 14, color = "red")
    ax2.grid(axis="x",linestyle="--",linewidth=0.8,color="white")
    ax2.set_axisbelow(True)
# Overall title
    fig3.suptitle(f"Actual Versus Ideal Laptimes for the {year} {event} Qualifying", fontsize = 20, color = "red")
# Now to plot all the graphs!
    plt.tight_layout()
    return fig, fig1, fig2, fig3
