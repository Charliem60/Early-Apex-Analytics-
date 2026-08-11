import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import matplotlib as mpl
import mplcursors
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
# Enables patches for plotting time values and loads dark colour theme.
fastf1.plotting.setup_mpl(mpl_timeddelta_support=True, color_scheme='fastf1')
# Loading the information that the user has given through the app. Fetching the circit and corner info for the dashboard later and loading the race.
def create_tele_dashboard(year,event,session_type, drivers): 
    session_names = {"FP1": "Free Practice 1", "FP2": "Free Practice 2", "FP3": "Free Practice 3", "SQ": "Sprint Qualifying", "S": "Sprint Race", "Q" : "Qualifying", "R": "Race"}
    race = fastf1.get_session(year, event, session_type)
    race.load()
    circuit = race.get_circuit_info()
    corners = circuit.corners
# Getting a drivers fastest lap and fetching the telemetry and getting the colors
    tele = {}
    styles = {}
#Find fastest lap in the session and setting the reference delta driver being the fastest driver that the others should be compared against. Getting the telemetry data.
    valid_laps = race.laps[race.laps["LapTime"].notna()]
    reference_delta_lap = valid_laps.pick_fastest()
    reference_delta_driver = reference_delta_lap["Driver"]
    for driver in drivers:
        lap = race.laps.pick_drivers(driver).pick_fastest()
        tele[driver] = lap.get_car_data().add_distance()
#Calculate delta relative across the course of the qualifying or fastest lap found from the given session. Finding the driver style and rounding the delta.
        delta, ref_tel, compare_tel = fastf1.utils.delta_time(lap, reference_delta_lap)
        tele[driver]["Delta"] = delta.round(3)
        styles[driver] = fastf1.plotting.get_driver_style(identifier = driver,style=["color", "linestyle"], session = race)

# Plotting the data and label the suplots, have them share the x axes with the 6 rows.
    fig = make_subplots(rows=6, cols=1, shared_xaxes=True, vertical_spacing=0.04, subplot_titles=("Speed (km/h)",
          "Delta",
          "Throttle",
          "Brake",
          "Gear",
          "RPM"))
# Now we set up the dashboard in a similar way for the weather plot using plotly.
    for driver in drivers:
        tele2 = tele[driver]
#SPEEEEEDDDD. Setting up the first plot of the speed of each car over the lap. Showing the driver name, getting the drive style, and setting up what is going to be displayed when a curser is hovered over the telemetry lines.   
        fig.add_trace(go.Scatter(x=tele2["Distance"], y=tele2["Speed"], name = driver,showlegend=True, line=dict(color=styles[driver]["color"], dash="dash" if len(drivers) >1 and driver == drivers[1] else "solid"),
                              hovertemplate= "<b>%{fullData.name}</b><br>" "Distance: %{x:.1f} m<br>" "Speed: %{y:.1f} km/h<extra></extra>"),
                              row=1, col=1)
# RPM. Display in the same plotly fashion as the speed above, changing the nessacery values.
        fig.add_trace(go.Scatter(x=tele2["Distance"], y=tele2["RPM"], name = driver,showlegend=False,line=dict(color=styles[driver]["color"], dash="dash" if len(drivers) >1 and driver == drivers[1] else "solid"),
                              hovertemplate= "<b>%{fullData.name}</b><br>" "RPM: %{y:.0f}<extra></extra>"),
                              row=6, col=1)
# Gear
        fig.add_trace(go.Scatter(x=tele2["Distance"], y=tele2["nGear"], name = driver,showlegend=False,line=dict(color=styles[driver]["color"], dash="dash" if len(drivers) >1 and driver == drivers[1] else "solid"),
                              hovertemplate= "<b>%{fullData.name}</b><br>" "Gear: %{y:.0f}<extra></extra>"),
                              row=5, col=1)
# Throttle
        fig.add_trace(go.Scatter(x=tele2["Distance"], y=tele2["Throttle"], name = driver,showlegend=False,line=dict(color=styles[driver]["color"],dash="dash" if len(drivers) >1 and driver == drivers[1] else "solid"),
                              hovertemplate= "<b>%{fullData.name}</b><br>" "Throttle: %{y:.1f}<extra></extra>"),
                              row=3, col=1)
# Brake
        fig.add_trace(go.Scatter(x=tele2["Distance"], y=tele2["Brake"].astype(int), name = driver, showlegend=False,line=dict(color=styles[driver]["color"], dash="dash" if len(drivers) >1 and driver == drivers[1] else "solid"),
                              hovertemplate= "<b>%{fullData.name}</b><br>" "Brake: %{y}<extra></extra>"),
                              row=4, col=1)
# Delta time
        fig.add_trace(go.Scatter(x=tele2["Distance"], y=tele2["Delta"], name = driver, showlegend=False,line=dict(color=styles[driver]["color"], dash="dash" if len(drivers) >1 and driver == drivers[1] else "solid"),
                              hovertemplate= "<b>%{fullData.name}</b><br>" "Gap to Fastest Time: %{y:+.3f} s" "<extra></extra>"),
                              row=2, col=1)

# Setting up the dashboard. Getting the corners and displaying them on the plot so that we can understand which corner is where to make the data understandable.
    for _, corner in corners.iterrows():
        for row in range(1,7):
            fig.add_vline(x=corner["Distance"], line_dash="dot",
                        line_width=2, row=row,col=1,
                        line_color="grey")
            fig.add_annotation(x=corner["Distance"], y=1.02, 
                            text= str(corner["Number"]), yref="paper",
                            showarrow=False,
                              font=dict(size=8))
    # Setting up the ui, the title and so on.
    fig.update_layout(template="plotly_dark", height=1300, hovermode="x unified", title =dict(text=f"{year} {event} {session_names.get(session_type, session_type)}<br>Fastest Lap Telemetry Comparison Plot", font=dict(size=22, color="yellow")))
    fig.update_annotations(font=dict(size=10, color="yellow"))
    # Returning the dashboard.
    return fig



