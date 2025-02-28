import streamlit as st
import pandas as pd
import plotly.express as px


def show():
    st.markdown("""
    <style>
        /* Style labels for selectbox, slider, and radio */
        div.stSelectbox > label, 
        div.stSlider > label, 
        div.stRadio > label {
            font-size: 28px !important;
            font-weight: bold !important;
            color: white !important;
        }

        /* Make text inside widgets white */
        div.stSelectbox, div.stSlider, div.stRadio {
            color: white !important;
        }

        /* Make the radio options white */
        div.stRadio div[role="radiogroup"] label {
            color: white !important;
            font-size: 24px !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

    results_df = pd.read_csv("results.csv")
    drivers_df = pd.read_csv("drivers.csv")
    constructors_df = pd.read_csv("constructors.csv")
    races_df = pd.read_csv("races.csv")

    constructors_df = constructors_df.rename(columns={'name': 'team_name'})
    races_df = races_df.rename(columns={'name': 'race_name'})

    results_df = results_df.merge(drivers_df[['driverId', 'surname', 'nationality']], on='driverId', how='left')
    results_df = results_df.merge(constructors_df[['constructorId', 'team_name']], on='constructorId', how='left')
    results_df = results_df.merge(races_df[['raceId', 'year', 'race_name']], on='raceId', how='left')

    st.title("🏎️ Race History")
    
    selected_season = st.selectbox("Select Season:", sorted(results_df['year'].unique(), reverse=True))
    
    season_races = results_df[results_df['year'] == selected_season][['raceId', 'race_name']].drop_duplicates()
    race_dict = dict(zip(season_races['race_name'], season_races['raceId']))
    selected_race_name = st.selectbox("Select Race:", list(race_dict.keys()))
    selected_race_id = race_dict[selected_race_name]
    
    race_data = results_df[results_df['raceId'] == selected_race_id]
    
    st.subheader("⏱️ Fastest Lap")
    if 'fastestLapTime' in race_data.columns and race_data['fastestLapTime'].notna().any():
        fastest_lap = race_data.loc[race_data['fastestLapTime'].idxmin()]
        st.write(f"Fastest Lap by: **{fastest_lap['surname']}** ({fastest_lap['nationality']}) with a time of **{fastest_lap['fastestLapTime']}**")
    else:
        st.write("No fastest lap data available for this race.")
    
    if race_data.empty:
        st.warning("No data available for this race.")
    else:
        st.subheader("🏆 Top Drivers")
        num_drivers = st.slider("Select number of top drivers to display:", 1, len(race_data), 3)
        top_drivers = race_data.nsmallest(num_drivers, 'positionOrder')
        
        styled_drivers = top_drivers[['positionOrder', 'surname', 'team_name', 'points']]  
        styled_drivers = styled_drivers.rename(columns={'positionOrder': 'Position', 'surname': 'Driver', 'team_name': 'Team'})

        plot_type = st.radio("Choose a visualization:", ["Bar Chart", "Pie Chart", "Scatter Plot"])

        if plot_type == "Bar Chart":
            fig = px.bar(
                styled_drivers, x='Position', y='points',  
                title="Top Finishers", labels={'Position': 'Position', 'points': 'Points'},
                color='Driver',  
                color_discrete_sequence=[
                                    "#c1121f",  # Ferrari Red
                                    "#669bbc",  # Light Blue (Mercedes Accent)
                                    "#003049",  # Dark Blue (Williams)
                                    "#005f73",  # Deep Teal
                                    "#0a9396",  # Aquamarine Teal
                                    "#23aaff",  # Alpine Cyan
                                    "#001d3d",  # Midnight Navy
                                    "#002855",  # Royal Blue
                                    "#1b263b",  # Graphite Blue
                                    "#ffffff",  # Pure White
                                    "#f8f9fa",  # Off White
                                    "#b0b3b8",  # Soft Grayish White
                                    "#979dac",  # Cool Gray
                                    "#444f5a",  # Dark Gray Blue
                                    "#89c2d9",  # Soft Sky Blue
                                    "#d9d9d9"   ])
        
        elif plot_type == "Pie Chart":
            fig = px.pie(
                styled_drivers, names='Driver', values='points',
                title="Points Distribution Among Top Drivers",
                color='Driver',
                color_discrete_sequence=[
                                    "#c1121f",  # Ferrari Red
                                    "#669bbc",  # Light Blue (Mercedes Accent)
                                    "#003049",  # Dark Blue (Williams)
                                    "#005f73",  # Deep Teal
                                    "#0a9396",  # Aquamarine Teal
                                    "#23aaff",  # Alpine Cyan
                                    "#001d3d",  # Midnight Navy
                                    "#002855",  # Royal Blue
                                    "#1b263b",  # Graphite Blue
                                    "#ffffff",  # Pure White
                                    "#f8f9fa",  # Off White
                                    "#b0b3b8",  # Soft Grayish White
                                    "#979dac",  # Cool Gray
                                    "#444f5a",  # Dark Gray Blue
                                    "#780000",  # Dark Blood Red
                                    "#ff4d4d",  # Light Red
                                    "#89c2d9",  # Soft Sky Blue
                                    "#d9d9d9"   ],
            )

        elif plot_type == "Scatter Plot":
            fig = px.scatter(
                styled_drivers, x='Position', y='points', 
                text='Driver',
                title="Top Drivers Performance",
                size='points',
                color='Driver',
                color_discrete_sequence=[
                                    "#c1121f",  # Ferrari Red
                                    "#669bbc",  # Light Blue (Mercedes Accent)
                                    "#003049",  # Dark Blue (Williams)
                                    "#005f73",  # Deep Teal
                                    "#0a9396",  # Aquamarine Teal
                                    "#23aaff",  # Alpine Cyan
                                    "#001d3d",  # Midnight Navy
                                    "#002855",  # Royal Blue
                                    "#1b263b",  # Graphite Blue
                                    "#ffffff",  # Pure White
                                    "#f8f9fa",  # Off White
                                    "#b0b3b8",  # Soft Grayish White
                                    "#979dac",  # Cool Gray
                                    "#444f5a",  # Dark Gray Blue
                                    "#780000",  # Dark Blood Red
                                    "#ff4d4d",  # Light Red
                                    "#89c2d9",  # Soft Sky Blue
                                    "#d9d9d9"   ],
            )
            fig.update_traces(textposition='top center')
        if fig:
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
                paper_bgcolor='#020517',  # Dark blue background
                font=dict(size=18, color='white'),
                title=dict(font=dict(size=24, color='white')),
                xaxis=dict(title_font=dict(size=22, color='white'), tickfont=dict(size=18, color='white')),
                yaxis=dict(title_font=dict(size=22, color='white'), tickfont=dict(size=18, color='white')),
                legend=dict(font=dict(size=18, color='white'))
            )
        st.plotly_chart(fig, use_container_width=True)
