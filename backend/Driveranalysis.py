# First we need to import the necessary libraries. We will use matplotlib for plotting and fastf1 for accessing the Formula 1 data.
from matplotlib import pyplot as plt
import fastf1
from fastf1 import plotting
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
year = int(input( "Enter the year (For example, 2021): "))
event = input("Enter the race name in full (eg 'Monaco Grand Prix'): ")
session_type = "R"
race = fastf1.get_session(year, event, session_type)
race.load()

# Select the drivers you want to plot.

driver_list = input("Enter the names of the drivers you want to plot (comma-separated in the form HAM, VER, ALO, etc.): ").split(",")
driver_list = [driver.strip().upper() for driver in driver_list]

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

# Now for a laptime distribution plot.
distribution_laps =driver_laps.copy()
distribution_laps =distribution_laps.dropna(subset=["LapTime"])



# Seaborn doesn't have proper delta support so it has to be converted to seconds.
distribution_laps["LapTimeSeconds"]= distribution_laps["LapTime"].dt.total_seconds()

compound_palette = (fastf1.plotting.get_compound_mapping(session=race))


# Now we have to set up the distribution plot.
fig3, ax3 = plt.subplots(figsize=(12, 6))
fig3.patch.set_facecolor("black")
ax3.set_facecolor("black")

ax3.tick_params(colors = "red")
ax3.xaxis.label.set_color("white")
ax3.yaxis.label.set_color("white")

#Making the violin and swarm shape of plot
sns.violinplot(data=distribution_laps,
               x = "Driver", y = "LapTimeSeconds", 
               ax=ax3, inner ="quartile",
                 order = driver_list, 
                )             

sns.swarmplot(data=distribution_laps,
              x= "Driver", y = "LapTimeSeconds",
              ax=ax3, order = driver_list,
              hue = "Compound", dodge=True,
              size =3, 
               )

sns.boxplot(
    data=distribution_laps,
    x="Driver", y = "LapTimeSeconds",
    ax=ax3, width = 0.3, showcaps=True,
    boxprops={"facecolor":"none"},
    showfliers=False,
    whiskerprops={"linewidth":2}
)

# Set up the labels and title for the distribution plot.
ax3.set_xlabel("Driver")
ax3.set_ylabel("Lap Time (seconds)")
ax3.set_title(f"Lap time distribution of selected drivers during the {year} {event}", color = "orange")

# Remove the duplicate legends
handles,labels = ax3.get_legend_handles_labels()

unique= dict(zip(labels,handles))
ax3.legend(unique.values(), unique.keys(),
           title="Compound", bbox_to_anchor=(1.05,1),
           loc="lower left")

sns.despine(left=True, bottom=True)


plt.tight_layout()
plt.show()

