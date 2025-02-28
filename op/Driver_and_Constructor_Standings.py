import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    results_df = pd.read_csv("results.csv")
    drivers_df = pd.read_csv("drivers.csv")
    constructors_df = pd.read_csv("constructors.csv")
    races_df = pd.read_csv("races.csv")

    constructors_df = constructors_df.rename(columns={'name': 'team_name'})
    races_df = races_df.rename(columns={'name': 'race_name'})
    drivers_df = drivers_df.rename(columns={'driverId': 'driverId', 'surname': 'surname', 'nationality': 'nationality'})
    constructors_df = constructors_df.rename(columns={'constructorId': 'constructorId', 'team_name': 'team_name'})

    results_df = results_df.merge(drivers_df[['driverId', 'surname', 'nationality']], on='driverId', how='left')
    results_df = results_df.merge(constructors_df[['constructorId', 'team_name']], on='constructorId', how='left')
    results_df = results_df.merge(races_df[['raceId', 'year', 'race_name']], on='raceId', how='left')

    st.title("Driver & Constructor Standings")
    selected_season = st.selectbox("Select Season:", sorted(results_df['year'].unique(), reverse=True))
    season_results = results_df[results_df['year'] == selected_season]
    
    driver_standings = season_results.groupby(['surname', 'nationality'])['points'].sum().reset_index()
    driver_standings = driver_standings.sort_values(by='points', ascending=False)
    
    constructor_standings = season_results.groupby(['team_name'])['points'].sum().reset_index()
    constructor_standings = constructor_standings.sort_values(by='points', ascending=False)
    
    plot_option = st.radio("Select Analysis Type:", ["Driver Standings", "Constructor Standings",])
    chart_type = st.selectbox("Select Chart Type:", ["Bar Chart", "Pie Chart",])
    top_n = st.slider("Select Top N Drivers:", min_value=1, max_value=20, value=10)
    
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
    
    if plot_option == "Driver Standings":
        st.subheader(f"Top {top_n} Drivers by Points")
        driver_data = driver_standings.head(top_n)
        
        if chart_type == "Bar Chart":
            fig = px.bar(driver_data, x='surname', y='points', color='surname', title=f"Top {top_n} Drivers", color_discrete_sequence=[
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
        elif chart_type == "Pie Chart":
            fig = px.pie(driver_data, names='surname', values='points', title=f"Top {top_n} Drivers",color_discrete_sequence=[
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
        
        st.plotly_chart(update_fig_layout(fig), use_container_width=True)
    
    elif plot_option == "Constructor Standings":
        st.subheader("Constructor Standings")
        if chart_type == "Bar Chart":
            fig = px.bar(constructor_standings, x='team_name', y='points', color='team_name', title="Constructor Standings",color_discrete_sequence=[
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
        elif chart_type == "Pie Chart":
            fig = px.pie(constructor_standings, names='team_name', values='points', title="Constructor Standings",color_discrete_sequence=[
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
        st.plotly_chart(update_fig_layout(fig), use_container_width=True)
    