import streamlit as st

st.set_page_config("Early Apex Analytics", layout="wide")

st.write("Formula 1 Data Analytics Dashboard")
page = st.sidebar.selectbox("Choose Analysis Type",
                            ["Race Results", "Qualifying Analysis", "Driver Analysis", "Weather", "Telemetry Dashboard"])
if page == "Qualifying Analysis":
    st.header("Driver Comparison and Results")

elif page == "Race Results":
    st.header("Race Analysis")
elif page == "Driver Analysis":
    st.header("Driver Comparison")
elif page == "Telemetry Dashboard":
    st.header("Telemetry Dashboard")
elif page == "Weather":
    st.header("Weather Dashboard")