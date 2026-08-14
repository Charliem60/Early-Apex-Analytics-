## Early-Apex-Analytics-
Early Apex Analytics is a GUI based app that is designed to give users insights into Formula One Telemetry Data along with creating graphs for other useful metrics. With the help of theOehrly's [FastF1](https://github.com/theOehrly/Fast-F1) python API you can explore data from the 2018 to 2026 Formula One seasons. With a [Streamlit](https://github.com/streamlit/streamlit) GUI the interface is built with simplicity in mind, making it easy to view desired graphs and dashboards.

Formula One generates a titanic amount of data during each race weekend. The goal of this project was to turn that data into something tangible and something that could be easily understood.
Project objectives such as the ability to analyse race and qualifying data, weather chart information, strategic variation, telemetry data and championship trends are all achieved with the results presented through the simple Streamlit interface. 


## Installation
- Download the latest release [here](https://github.com/Charliem60/Early-Apex-Analytics-/releases)
- Unzip the file. Then using cmd and pip, go to the directory of this repository and run the following commands. This has to be run to install the packages needed: `[ythom -m pip install -r requirements.txt`. Then also run `python -m pip install streamlit` which installs the streamlit to display the GUI used for the app.
- Run `python -m streamlit run app.py` to start the streamlit app
- The streamlit app will open onto the homepage with a brief explanation about the application.
- Other useful information:
  - Each time you want to launch the application run `streamlit run app.py`.
  - This application uses a cache system. You can find all this data in the cache folder and clear it should you wish. You can also do this on the site itself.
  - Works with python v3.14
  - Yes, the site is that yellow.


## Navigating the site
The site has a very user friendly design, as seen in the gif below. There are a variety of different tabs which when clicked bring you to different sections of the site. To begin click a header related to the topic you want to investigate as seen in the example below.

<img width="800" height="352" alt="ui 1" src="https://github.com/user-attachments/assets/ac78ff02-a746-4fda-91b6-a0e43edc4f13" />

Using the select boxes, pick whatever season you want to investigate followed by the race. In the below example the user wants to generate graphs related to qualifying for the 2026 Hungarian Grand Prix. After you have selected you season and race, press the generate qualifying analysis button

<img width="1203" height="496" alt="image" src="https://github.com/user-attachments/assets/6231e318-2bff-43c4-a0fe-4f4db9b6df25" />

Once that is complete, and the session has loaded you will see a variety of displayed graphs. Scroll down to see each of the graphs, followed by brief explanations of what they show. As seen in the example below, if the graph doesn't fit in your screen, press the window icon at the top right corner of the graph to blow it up. It can be easier to view graphs and plots that way.

<img width="800" height="383" alt="navigation gif" src="https://github.com/user-attachments/assets/b79ed525-8b5b-484b-a19c-e4a753e90c26" />

In other tabs such as Telemetry Analysis or Weather, you will have to input a session for more options. In the example below, the user is investigating the traces of the top three of the Hungarian Grand Prix qualifying session. The dashboard seen below can also be viewed by itself when pressing the window icon in the top right corner. Use your curser to hover over the traces to view further information. 
<img width="800" height="362" alt="telem2" src="https://github.com/user-attachments/assets/6607d4c3-46b0-4b2e-a303-9aceed74821d" />

That is all you need to know in navigating the site. Please be aware that for the Championship tab the plots will take longer to generate as Plotly is gathering data for the full season. 

## What the site can do
-⏱ Qualifying Analysis:

Compare lap times, sectors and ideal vs actual laps.

-🏁 Race Analysis:

Examine pace between teammates, rivals, race strategies and position changes.

-👤 Driver Analysis:

Compare driver session plans, runs and laptimes during a session.

-📡 Telemetry:

Explore braking, throttle and speed traces between different cars over a lap.

-🌦 Weather:

A dashboard for understanding weather conditions during any given session.

-🏆 Championship:
Examine past season standings and trends

## Future updates
⚠️  This project is in very early development and this current version is version 1.0 ⚠️

Over the course of the next few months and years the aim is to built Early Apex Analytics into a fully functional website with more developed features such as advanced telemetry comparisons, race simulations, live race data, increased graphs and championship standings tables and an improved UI.

There is bound to be mistakes with this app, and errors that have slipped through the cracks, so keep in mind that this app is in very early development. If you do run into any errors or have any advice for future improvements, don't hesitate to let me know.

Thank you for testing out the project.

## Notice

Early Apex Analytics and this application are unofficial and are not associated in any way with
the Formula 1 companies. F1, FORMULA ONE, FORMULA 1, FIA FORMULA ONE WORLD
CHAMPIONSHIP, GRAND PRIX and related marks are trade marks of Formula One
Licensing B.V.

