import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    results_df = pd.read_csv("results.csv")
    drivers_df = pd.read_csv("drivers.csv")
    constructors_df = pd.read_csv("constructors.csv")
    races_df = pd.read_csv("races.csv")

    constructors_df = constructors_df.rename(columns={'name': 'team_name'})
    races_df = races_df.rename(columns={'name': 'race_name'})

    results_df = results_df.merge(drivers_df[['driverId', 'surname', 'nationality']], on='driverId', how='left')
    results_df = results_df.merge(constructors_df[['constructorId', 'team_name']], on='constructorId', how='left')
    results_df = results_df.merge(races_df[['raceId', 'year', 'race_name']], on='raceId', how='left')

    return results_df

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

def plot_data(df, x, y, title, plot_type, color_col=None):
    if plot_type == "Line Chart":
        fig = px.line(df, x=x, y=y, title=title, markers=True, line_shape='spline', color=color_col,color_discrete_sequence=[
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
    elif plot_type == "Bar Chart":
        fig = px.bar(df, x=x, y=y, title=title, barmode='group', color=color_col,color_discrete_sequence=[
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
    elif plot_type == "Pie Plot":
        fig = px.pie(df, names=x, values=y, title=title, color=color_col,color_discrete_sequence=[
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
                                    "#d9d9d9"   ])  # Fixed for Pie Plot
    update_fig_layout(fig)   
    return fig

def show():
    results_df = load_data()
    
    st.title("📊 Performance Analysis")

    analysis_choice = st.selectbox("What do you want to analyze?",  ["Driver Performance", "Team Performance", "Driver Comparison"])
    
    if analysis_choice == "Driver Performance":
        st.subheader("🏎️ Driver Performance Over Seasons")

        selected_driver = st.selectbox("Select Driver:", sorted(results_df['surname'].unique()))
        selected_metric = st.selectbox("Choose Metric:", ["Points Per Season", "Wins Per Season"], key="driver_metric")

        min_year, max_year = int(results_df['year'].min()), int(results_df['year'].max())
        selected_years = st.slider("Select Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year))

        driver_data = results_df[(results_df['surname'] == selected_driver) & 
                                 (results_df['year'].between(*selected_years))]

        driver_performance = driver_data.groupby('year').agg({'points': 'sum', 'positionOrder': lambda x: (x == 1).sum()}).reset_index()
        driver_performance.rename(columns={'positionOrder': 'Wins'}, inplace=True)

        plot_type = st.radio("Choose a visualization type:", ["Line Chart", "Bar Chart", "Pie Plot"], key="driver_plot")
        metric_column = 'points' if selected_metric == "Points Per Season" else 'Wins'
        fig = plot_data(driver_performance, 'year', metric_column, f"{selected_driver} - {selected_metric}", plot_type)
        st.plotly_chart(fig, use_container_width=True)

    elif analysis_choice == "Team Performance":
        st.subheader("🏎️ Team Performance Over Seasons")

        selected_team = st.selectbox("Select Team:", sorted(results_df['team_name'].unique()))
        selected_metric = st.selectbox("Choose Metric:", ["Points Per Season", "Wins Per Season"], key="team_metric")

        min_year, max_year = int(results_df['year'].min()), int(results_df['year'].max())
        selected_years = st.slider("Select Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year), key="team_years")

        team_data = results_df[(results_df['team_name'] == selected_team) & 
                               (results_df['year'].between(*selected_years))]

        team_performance = team_data.groupby('year').agg({'points': 'sum', 'positionOrder': lambda x: (x == 1).sum()}).reset_index()
        team_performance.rename(columns={'positionOrder': 'Wins'}, inplace=True)

        plot_type = st.radio("Choose a visualization type:", ["Line Chart", "Bar Chart", "Pie Plot"], key="team_plot")
        metric_column = 'points' if selected_metric == "Points Per Season" else 'Wins'
        fig = plot_data(team_performance, 'year', metric_column, f"{selected_team} - {selected_metric}", plot_type)
        st.plotly_chart(fig, use_container_width=True)

    elif analysis_choice == "Driver Comparison":
        st.subheader("🏎️ Compare Multiple Drivers")

        selected_drivers = st.multiselect("Select Drivers:", sorted(results_df['surname'].unique()))
        selected_metric = st.selectbox("Choose Metric:", ["Points Per Season", "Wins Per Season"], key="compare_metric")

        min_year, max_year = int(results_df['year'].min()), int(results_df['year'].max())
        selected_years = st.slider("Select Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year), key="compare_years")

        comparison_data = results_df[(results_df['surname'].isin(selected_drivers)) & 
                                     (results_df['year'].between(*selected_years))]

        comparison_performance = comparison_data.groupby(['year', 'surname']).agg({'points': 'sum', 'positionOrder': lambda x: (x == 1).sum()}).reset_index()
        comparison_performance.rename(columns={'positionOrder': 'Wins'}, inplace=True)

        plot_type = st.radio("Choose a visualization type:", ["Line Chart", "Bar Chart", "Pie Plot"], key="compare_plot")
        metric_column = 'points' if selected_metric == "Points Per Season" else 'Wins'

        if not selected_drivers:
            st.warning("Please select at least one driver for comparison.")
        else:
            fig = plot_data(comparison_performance, 'year', metric_column, "Driver Comparison - " + selected_metric, plot_type, 'surname')
            st.plotly_chart(fig, use_container_width=True)
