import streamlit as st
import pandas as pd
import plotly.express as px

def show():

    circuits_df = pd.read_csv("circuits.csv")
    races_df = pd.read_csv("races.csv")
    results_df = pd.read_csv("results.csv")
    drivers_df = pd.read_csv("drivers.csv")
    constructors_df = pd.read_csv("constructors.csv")

    circuits_df = circuits_df.rename(columns={'name': 'circuit_name'})
    races_df = races_df.rename(columns={'name': 'race_name'})
    constructors_df = constructors_df.rename(columns={'name': 'team_name'})

    results_df = results_df.merge(drivers_df[['driverId', 'surname']], on='driverId', how='left')
    results_df = results_df.merge(constructors_df[['constructorId', 'team_name']], on='constructorId', how='left')
    results_df = results_df.merge(races_df[['raceId', 'year', 'race_name', 'circuitId']], on='raceId', how='left')
    races_df = races_df.merge(circuits_df[['circuitId', 'circuit_name', 'location', 'country']], on='circuitId', how='left')
    
    st.title("\U0001F3CE️ Circuit & Track Analysis")
    
    selected_circuit = st.selectbox("Select Circuit:", sorted(circuits_df['circuit_name'].unique()))
    circuit_data = circuits_df[circuits_df['circuit_name'] == selected_circuit].iloc[0]
    
    st.markdown(f"### {selected_circuit} - {circuit_data['location']}, {circuit_data['country']}")
    st.info(f"**Location:** {circuit_data['location']}, {circuit_data['country']}")
    
    circuit_races = races_df[races_df['circuit_name'] == selected_circuit]
    race_ids = circuit_races['raceId'].tolist()
    circuit_results = results_df[results_df['raceId'].isin(race_ids)]
    
    years = sorted(circuit_races['year'].unique())
    selected_years = st.slider("Select Year Range:", min_value=1950, max_value=2024, value=(min(years), max(years)))
    filtered_results = circuit_results[(circuit_results['year'] >= selected_years[0]) & (circuit_results['year'] <= selected_years[1])]
    
    data_options = ["Fastest Lap Times", "Most Successful Drivers", "Most Successful Teams", "Top 3 Finishers"]
    selected_data = st.selectbox("Select Data Type:", data_options)
    def update_fig_layout(fig):
        fig.update_layout(
            plot_bgcolor='#020517',
            paper_bgcolor='#020517',
            font=dict(color='white', size=16),
            title_font=dict(size=20, color='white'),
            xaxis=dict(title_font=dict(size=18, color='white'), tickfont=dict(size=14, color='white')),
            yaxis=dict(title_font=dict(size=18, color='white'), tickfont=dict(size=14, color='white'))
        )
        return fig
    top_n = st.slider("Select Number of Top Entities:", min_value=1, max_value=20, value=3)
    
    if selected_data == "Fastest Lap Times":
        st.subheader("⏱️ Fastest Lap Times by Year")
        if 'fastestLapTime' in filtered_results.columns and filtered_results['fastestLapTime'].notna().any():
            fastest_laps = filtered_results.loc[filtered_results.groupby('year')['fastestLapTime'].idxmin()][['year', 'surname', 'fastestLapTime']]
            fig = px.bar(fastest_laps, x='year', y='fastestLapTime', color='surname', title="Fastest Lap Times", labels={'fastestLapTime': 'Lap Time (s)', 'year': 'Year'}, color_discrete_sequence=[
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
                                    "#d9d9d9"   ])
            fig = update_fig_layout(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No fastest lap data available.")
    
    elif selected_data == "Most Successful Drivers":
        st.subheader("🏆 Most Successful Drivers")
        driver_wins = filtered_results[filtered_results['positionOrder'] == 1]['surname'].value_counts().reset_index()
        driver_wins.columns = ['Driver', 'Wins']
        driver_wins = driver_wins.head(top_n)
        fig = px.bar(driver_wins, x='Wins', y='Driver', orientation='h', title="Most Successful Drivers", labels={'Wins': 'Number of Wins', 'Driver': 'Driver'}, color='Driver',color_discrete_sequence=[
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
                                    "#d9d9d9"   ])
        fig = update_fig_layout(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_data == "Most Successful Teams":
        st.subheader("🏆 Most Successful Teams")
        team_wins = filtered_results[filtered_results['positionOrder'] == 1]['team_name'].value_counts().reset_index()
        team_wins.columns = ['Team', 'Wins']
        team_wins = team_wins.head(top_n)
        fig = px.bar(team_wins, x='Wins', y='Team', orientation='h', title="Most Successful Teams", labels={'Wins': 'Number of Wins', 'Team': 'Team'}, color='Team',color_discrete_sequence=[
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
                                    "#d9d9d9"   ])
        fig = update_fig_layout(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_data == "Top 3 Finishers":
        st.subheader("🥇 Top 3 Finishers Over the Years")
        top_finishers = filtered_results[filtered_results['positionOrder'] <= top_n][['year', 'surname', 'positionOrder']]
        fig = px.scatter(top_finishers, x='year', y='positionOrder', color='surname', title="Top 3 Finishers", labels={'positionOrder': 'Finishing Position', 'year': 'Year'}, size_max=10,color_discrete_sequence=[
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
                                    "#d9d9d9"   ])
        fig = update_fig_layout(fig)
        st.plotly_chart(fig, use_container_width=True)