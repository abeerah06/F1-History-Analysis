import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
results_df = pd.read_csv("results.csv")  
drivers_df = pd.read_csv("drivers.csv")  
races_df = pd.read_csv("races.csv")  

results_with_drivers = results_df.merge(drivers_df, on="driverId", how="left")
results_with_year = results_with_drivers.merge(races_df[["raceId", "year"]], on="raceId", how="left")
total_points_per_driver = results_with_year.groupby(["driverId", "forename", "surname"])['points'].sum().reset_index()
top_driver = total_points_per_driver.sort_values(by="points", ascending=False).iloc[0]

top_per_year = results_with_year.groupby(["year", "driverId", "forename", "surname"])['points'].sum().reset_index()
champions = top_per_year.loc[top_per_year.groupby("year")['points'].idxmax()]
championship_counts = champions.groupby(["driverId", "forename", "surname"]).size().reset_index(name="championships")
most_championships = championship_counts.sort_values(by="championships", ascending=False).iloc[0]
total_races = races_df.shape[0]
total_seasons = races_df["year"].nunique()
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #10132a;  /* Sidebar Dark Gray */
        padding: 20px;
    }

    [data-testid="stSidebar"] h1 {
        color: #FFFFFF !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        margin-bottom: 10px;
    }

    [data-testid="stSidebar"] * {
        color: #DDDDDD !important;  /* Light Gray Text */
        font-size: 20px !important;
        font-weight: bold !important; 
    }

    .metric-box {
        border: 1px solid white;
        border-radius: 10px;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;

    }
    .stApp {
        background-color: #020517;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.image("f1_logo.png")
page = st.sidebar.radio("Menu", [
    "Home", "Race History", "Constructors Standings", "Driver & Constructor Standings", "Performance Trends", 
    "Circuit & Track Analysis","Pole Positions & Qualifying Analysis"
])

if page == "Home":
    st.title("F1 History Summary")
    st.image("pngegg.png")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-box"> <h3>Total Seasons</h3> <h1>' + str(total_seasons) + '</h1> </div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"> <h3>Total Races</h3> <h1>' + str(total_races) + '</h1> </div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="metric-box"> <h3>Most Championships</h3> <h1>' + most_championships['forename'] + ' ' + most_championships['surname'] + '</h1> <p>' + str(most_championships['championships']) + ' titles</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"> <h3>Top Driver (All Time Points)</h3> <h1>' + top_driver['forename'] + ' ' + top_driver['surname'] + '</h1> <p>' + str(top_driver['points']) + ' points</p> </div>', unsafe_allow_html=True)
    
elif page == "Race History":
    import op.Race_History as r
    r.show()
elif page == "Constructors Standings":
    import op.constructors as c1 
    c1.show()
elif page == "Driver & Constructor Standings":
    import op.Driver_and_Constructor_Standings as c
    c.show()
elif page == "Performance Trends":
    import op.performance as p
    p.show()
elif page == "Circuit & Track Analysis":
    import op.CircuitTrackAnalysis as t
    t.show()
elif page == "Pole Positions & Qualifying Analysis":
    import op.quali as q
    q.show()
