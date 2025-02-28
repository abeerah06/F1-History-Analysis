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
    drivers_df = drivers_df.rename(columns={'surname': 'driver_name'})

    results_df = results_df.merge(drivers_df[['driverId', 'driver_name']], on='driverId', how='left')
    results_df = results_df.merge(constructors_df[['constructorId', 'team_name']], on='constructorId', how='left')
    results_df = results_df.merge(races_df[['raceId', 'year', 'race_name', 'circuitId']], on='raceId', how='left')
    races_df = races_df.merge(circuits_df[['circuitId', 'circuit_name', 'location', 'country']], on='circuitId', how='left')

    results_df['year'] = pd.to_numeric(results_df['year'], errors='coerce')
    results_df['grid'] = pd.to_numeric(results_df['grid'], errors='coerce')
    results_df['positionOrder'] = pd.to_numeric(results_df['positionOrder'], errors='coerce')
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
    st.title("Pole Positions & Qualifying Analysis")
    
    analysis_option = st.selectbox("Choose Analysis Type:", ["Most Pole Positions per Driver", "Qualifying Position vs. Final Position", "Track-wise Pole Position Winners"])
    
    if analysis_option == "Most Pole Positions per Driver":
        st.subheader("Most Pole Positions per Driver")
        top_n = st.slider("Select Top N Drivers:", min_value=1, value=10)
        selected_drivers = st.multiselect("Or Select Specific Drivers:", sorted(results_df['driver_name'].dropna().unique()))
        
        if selected_drivers:
            filtered_results = results_df[results_df['driver_name'].isin(selected_drivers)]
        else:
            pole_positions = results_df[results_df['grid'] == 1].groupby('driver_name').size().reset_index(name='pole_count').sort_values(by='pole_count', ascending=False)
            filtered_results = results_df[results_df['driver_name'].isin(pole_positions.head(top_n)['driver_name'])]
        
        pole_positions = filtered_results[filtered_results['grid'] == 1].groupby('driver_name').size().reset_index(name='pole_count').sort_values(by='pole_count', ascending=False)
        chart_type = st.radio("Choose Visualization Type:", ["Bar Chart", "Pie Chart"])
        
        if chart_type == "Bar Chart":
            fig_poles = px.bar(pole_positions, x='driver_name', y='pole_count', title="Most Pole Positions per Driver", labels={'pole_count': 'Pole Positions'}, color_discrete_sequence=[
                                    
                                    "#89c2d9",  # Soft Sky Blue
                                    "#d9d9d9"   ])
        else:
            fig_poles = px.pie(pole_positions, names='driver_name', values='pole_count', title="Most Pole Positions per Driver",color_discrete_sequence=[
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
        fig_poles=update_fig_layout(fig_poles)
        st.plotly_chart(fig_poles, use_container_width=True)
    
    elif analysis_option == "Qualifying Position vs. Final Position":
        st.subheader("Qualifying Position vs. Final Position")
        min_year = int(results_df['year'].min())
        max_year = int(results_df['year'].max())
        selected_years = st.slider("Select Year Range:", min_year, max_year, (max_year - 5, max_year))
        selected_drivers = st.multiselect("Select Drivers (Optional):", sorted(results_df['driver_name'].dropna().unique()))
        qualifying_data = results_df[(results_df['year'].between(selected_years[0], selected_years[1])) & results_df[['grid', 'positionOrder', 'driver_name']].notna().all(axis=1)]
        
        if selected_drivers:
            qualifying_data = qualifying_data[qualifying_data['driver_name'].isin(selected_drivers)]
        
        fig_qualifying = px.scatter(qualifying_data, x='grid', y='positionOrder', color='driver_name', title="Qualifying Position vs. Final Position",color_discrete_sequence=[
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
        fig_qualifying=update_fig_layout(fig_qualifying)
        st.plotly_chart(fig_qualifying, use_container_width=True)
    
    elif analysis_option == "Track-wise Pole Position Winners":
        st.subheader("Track-wise Pole Position Winners")
        selected_circuits = st.multiselect("Select Circuits (Leave empty to view all):", sorted(circuits_df['circuit_name'].dropna().unique()))
        selected_drivers = st.multiselect("Select Drivers (Optional):", sorted(results_df['driver_name'].dropna().unique()))
        pole_winners = results_df[results_df['grid'] == 1].groupby(['circuitId', 'driver_name']).size().reset_index(name='count')
        pole_winners = pole_winners.merge(circuits_df[['circuitId', 'circuit_name']], on='circuitId', how='left')
        
        if selected_circuits:
            pole_winners = pole_winners[pole_winners['circuit_name'].isin(selected_circuits)]
        if selected_drivers:
            pole_winners = pole_winners[pole_winners['driver_name'].isin(selected_drivers)]
        
        fig_pole_heatmap = px.density_heatmap(pole_winners, x='circuit_name', y='driver_name', z='count', title="Track-wise Pole Position Winners", color_continuous_scale='Viridis',color_discrete_sequence=[
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
        fig_pole_heatmap=update_fig_layout(fig_pole_heatmap)
        st.plotly_chart(fig_pole_heatmap, use_container_width=True)
