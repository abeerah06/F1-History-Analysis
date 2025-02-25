import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    
    results_df = pd.read_csv("results.csv")  
    standings_df = pd.read_csv("driver_standings.csv")  
    drivers_df = pd.read_csv("drivers.csv")  
    constructors_df = pd.read_csv("constructors.csv")  
    races_df = pd.read_csv("races.csv")  

    results_df = results_df.merge(drivers_df[['driverId', 'surname']], on='driverId', how='left')
    results_df = results_df.merge(constructors_df[['constructorId', 'name']], on='constructorId', how='left')
    results_df = results_df.merge(races_df[['raceId', 'year', 'round']], on='raceId', how='left')

    results_df = results_df[['raceId', 'year', 'round', 'surname', 'name', 'positionOrder']]
    standings_df = standings_df[['raceId', 'driverId', 'points']]

    st.title("🏎️ Constructors Standings")
    selected_season = st.selectbox("📅 Select Season:", sorted(results_df['year'].unique(), reverse=True))
    
    season_data = results_df[results_df['year'] == selected_season]
    standings_data = standings_df.merge(races_df[['raceId', 'name']], on='raceId', how='left')
    standings_summary = standings_data.groupby('driverId')['points'].sum().reset_index()
    
    select_plot = st.radio('📊 Select Plot:', ["Race Wins by Constructor", "Constructor Wins Distribution"])    
    wins_by_team = season_data[season_data['positionOrder'] == 1]['name'].value_counts()
    
    if select_plot == "Race Wins by Constructor":
        race_wins_fig = px.bar(wins_by_team, x=wins_by_team.index, y=wins_by_team.values, 
                                title="🏎️ Race Wins by Constructor", labels={'x': 'Constructor', 'y': 'Wins'},
                                color=wins_by_team.index,
                                color_discrete_sequence=["#c1121f", "#003049", "#fdf0d5"])
        race_wins_fig.update_layout(
            plot_bgcolor='#020517',
            paper_bgcolor='#020517',
            title_font=dict(size=24, color='white'),
            xaxis=dict(title_font=dict(size=20, color='white'), tickfont=dict(size=16, color='white')),
            yaxis=dict(title_font=dict(size=20, color='white'), tickfont=dict(size=16, color='white'))
        )
        st.plotly_chart(race_wins_fig, use_container_width=True)
    
    elif select_plot == 'Constructor Wins Distribution':
        st.subheader("🏆 Constructor Wins Distribution")
        pie_fig = px.pie(wins_by_team, names=wins_by_team.index, values=wins_by_team.values, 
                        title="Percentage of Wins per Constructor",
                        color_discrete_sequence=["#c1121f", "#003049", "#fdf0d5"])
        pie_fig.update_layout(
            plot_bgcolor='#020517',
            paper_bgcolor='#020517',
            title_font=dict(size=24, color='white'),
            legend=dict(font=dict(size=16, color='white'))
        )
        st.plotly_chart(pie_fig)
