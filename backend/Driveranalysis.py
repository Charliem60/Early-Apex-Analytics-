# First we need to import the necessary libraries. We will use matplotlib for plotting and fastf1 for accessing the Formula 1 data.
from matplotlib import pyplot as plt
import fastf1 as fastf1
from fastf1data import plotting
import seaborn as sns
import fastf1.plotting

# Enables patches for plotting time values and loads dark colour theme.
fastf1.plotting.setup_mpl(mpl_timeddelta_support=True, color_scheme='fastf1')

# Converting lap times for later
def format_laptime(td):
    total_seconds = td.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:06.3f}"


#Load session data and select the session you want to plot. 
def create_driver_traces(year, event, session_type, drivers):
    race = fastf1.get_session(year, event, session_type)
    race.load()

# Select the drivers you want to plot.
    available_drivers = race.results["Abbreviation"].tolist()
    valid_drivers = []
    
    for driver in driver_list: 
        if driver in available_drivers:
            valid_drivers.append(driver)
        else:
            print(f"Warning: {driver} is not found in this session!")

    if not valid_drivers:
        print("No drivers selected!")
        exit()
        driver_list = valid_drivers

# Set up the colours of the graph and its titles
    fig1, ax1 = plt.subplots(figsize=(11, 7))
    fig1.patch.set_facecolor('black')  
    ax1.set_facecolor('black')

    ax1.tick_params(colors='red')  
    ax1.xaxis.label.set_color('red')
    ax1.yaxis.label.set_color('red')
    ax1.set_title(f"Lap times of selected drivers during the {year} {event}", color="red")

# Picking Drivers for the plot
    for driver in driver_list:
        driver = driver.strip()

        laps = race.laps.pick_drivers(driver).pick_quicklaps().reset_index()

        style = plotting.get_driver_style(
    identifier=driver,
    style=["color", "linestyle"],
    session=race
    )
     # Plotting the lap times of the selected drivers and highlighting their fastest lap with a scatter point and annotation.
        ax1.plot(laps["LapNumber"], laps["LapTime"], **style, linewidth=2.5, label=driver)

    # Finding Fastest Lap of selected drivers
        fastest_lap =laps.loc[laps["LapTime"].idxmin()]
    #Setting up the scatter point and annotation for the fastest lap of each driver.
        ax1.scatter(
        fastest_lap["LapNumber"], fastest_lap["LapTime"], color="purple", edgecolors="black", s=60, zorder=5, label=f"{driver} fastest")

        ax1.annotate(
        format_laptime(fastest_lap["LapTime"]),
       ( fastest_lap["LapNumber"],fastest_lap["LapTime"]),
        xytext=(8,8,),textcoords = "offset points", color = "white", fontsize=12,
    )


# Next we set up the graph with labels, title and legend, and then display it.
    ax1.set_xlabel( "Lap Number")
    ax1.set_ylabel("Lap Time")
    ax1.grid(True, linestyle= "--", alpha=0.4)
    ax1.legend()



# Now to create a scatterplot to display the given laptimes of the drivers in a scatterplot.
# Get laps only for selected drivers.
    driver_laps = race.laps.pick_drivers(driver_list).pick_quicklaps().reset_index()
    driver_palette = {}

    for driver in driver_list:
        try: 
            driver_palette[driver] = fastf1.plotting.get_driver_color(driver, session=race)
        except Exception:
            pass


# Next we set up the scatterplot

    fig2, ax2 = plt.subplots(figsize = (8, 6))
    fig2.patch.set_facecolor("black")
    ax2.set_facecolor("black")

    ax2.tick_params(colors = "red")
    ax2.xaxis.label.set_color("white")
    ax2.yaxis.label.set_color("white")
    ax2.set_title(f"Scatterplot of lap times during the {year} {event}", color ="white")


    sns.scatterplot(data=driver_laps,
                x= "LapNumber",
                y = "LapTime",
                ax=ax2, hue="Driver", style = "Compound",  
                palette = driver_palette,
                s=80, linewidth=0,)
            
# Set labels for the scatterplot.
    ax2.set_xlabel( "Lap Number")
    ax2.set_ylabel("Lap Time")
    ax2.invert_yaxis()
    plt.grid(color="w", which = "major", axis = "both")
    sns.despine(left=True, bottom=True)
    ax2.grid(True, linestyle= "--", alpha=0.4)
    ax2.legend()
    fig2.tight_layout()

    return fig1, fig2

