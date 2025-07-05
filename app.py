import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Set page config for a polished look
st.set_page_config(page_title="Road Accident Analysis Dashboard", layout="wide", page_icon="🚗")

# Define color scheme
COLORS = {
    'primary': '#1E3A8A',    # Deep blue
    'secondary': '#10B981',  # Teal
    'accent': '#F59E0B',    # Amber
    'gray': '#6B7280',      # Gray
    'red': '#EF4444',       # Red
    'background': 'linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%)',  # Light gradient
    'text': '#1F2937'       # Dark gray
}

# Load sample datasets
@st.cache_data
def load_data():
    data_dir = Path(__file__).parent
    main_data = pd.read_csv(data_dir / "sample_road_accident_data.csv")
    yearly_data = pd.read_csv(data_dir / "yearly_accidents.csv")
    monthly_data = pd.read_csv(data_dir / "monthly_accidents.csv")
    daily_data = pd.read_csv(data_dir / "daily_accidents.csv")
    time_data = pd.read_csv(data_dir / "time_accidents.csv")
    road_type_data = pd.read_csv(data_dir / "road_type_severity.csv")
    weather_data = pd.read_csv(data_dir / "weather_severity.csv")
    severity_data = pd.read_csv(data_dir / "severity_by_cause.csv")
    return main_data, yearly_data, monthly_data, daily_data, time_data, road_type_data, weather_data, severity_data

main_data, yearly_data, monthly_data, daily_data, time_data, road_type_data, weather_data, severity_data = load_data()

# Sidebar
st.sidebar.title("Road Accident Dashboard")
section = st.sidebar.selectbox(
    "Select Analysis Section",
    [
        "Yearly Trends",
        "Monthly Trends",
        "Daily Trends",
        "Time of Day",
        "Road Type and Location",
        "Weather Conditions",
        "Outcomes by Cause"
    ]
)

# Filters
st.sidebar.subheader("Filters")
selected_years = st.sidebar.multiselect("Select Years", sorted(main_data['Year'].unique()), default=sorted(main_data['Year'].unique()))
selected_causes = st.sidebar.multiselect("Select Accident Causes", sorted(main_data['Accident Cause'].unique()), default=sorted(main_data['Accident Cause'].unique()))
selected_regions = st.sidebar.multiselect("Select Regions", sorted(main_data['Region'].unique()), default=sorted(main_data['Region'].unique()))

# Filter main data
filtered_data = main_data[
    (main_data['Year'].isin(selected_years)) &
    (main_data['Accident Cause'].isin(selected_causes)) &
    (main_data['Region'].isin(selected_regions))
]

# Helper function for styling
def apply_styles():
    st.markdown(
        f"""
        <style>
        .main {{
            background: {COLORS['background']};
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        h1, h2, h3 {{
            color: {COLORS['text']};
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .stSidebar {{
            background-color: {COLORS['primary']};
            color: white;
            padding: 10px;
        }}
        .stButton>button {{
            background-color: {COLORS['secondary']};
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 5px;
        }}
        .stSelectbox {{
            background-color: #FFFFFF;
            border-radius: 5px;
            padding: 5px;
        }}
        .stMarkdown {{
            line-height: 1.6;
            color: {COLORS['text']};
        }}
        .footer {{
            text-align: center;
            color: {COLORS['text']};
            margin-top: 20px;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 5px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

apply_styles()

# Logo (optional)
st.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://via.placeholder.com/150" alt="Your Logo" width="150">
    </div>
    """,
    unsafe_allow_html=True
)

# Section rendering
st.title("Road Accident Analysis Dashboard")

if section == "Yearly Trends":
    st.header("Yearly Trends in Road Accidents")
    # Stacked Bar Chart
    fig_bar = px.bar(
        yearly_data,
        x='Year',
        y=['Weather', 'Drunk Driving', 'Mechanical Failure', 'Speeding', 'Distracted Driving'],
        title="Accident Causes by Year",
        labels={'value': 'Number of Accidents', 'variable': 'Accident Cause'},
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['gray'], COLORS['red']]
    )
    fig_bar.update_layout(barmode='stack')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Line Chart
    fig_line = px.line(
        yearly_data,
        x='Year',
        y='Total',
        title="Total Road Accidents Per Year",
        labels={'Total': 'Number of Accidents'},
        line_shape='spline',
        markers=True,
        color_discrete_sequence=[COLORS['accent']]
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
    ### Data Storytelling: Yearly Trends in Road Accident Causes
    This grouped table reveals how various accident causes have evolved over the years...
    - **Overspeeding** consistently dominates the chart...
    - **Driver inattention** and **alcohol influence** also maintain a persistent presence...
    - The year **2002** recorded the **highest number of total road accidents (5,433)**...
    - Continued investment in **speed control technologies**, **public education**, and **law enforcement** is essential...
    """)

elif section == "Monthly Trends":
    st.header("Monthly Trends in Road Accidents")
    # Stacked Bar Chart
    fig_bar = px.bar(
        monthly_data,
        x='Month',
        y=['Distracted Driving', 'Drunk Driving', 'Mechanical Failure', 'Speeding', 'Weather'],
        title="Accident Causes by Month",
        labels={'value': 'Number of Accidents', 'variable': 'Accident Cause'},
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['gray'], COLORS['red']]
    )
    fig_bar.update_layout(barmode='stack')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Line Chart
    fig_line = px.line(
        monthly_data,
        x='Month',
        y=['Distracted Driving', 'Drunk Driving', 'Mechanical Failure', 'Speeding', 'Weather'],
        title="Monthly Trends of Road Accidents by Cause",
        labels={'value': 'Number of Accidents', 'variable': 'Accident Cause'},
        markers=True,
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['gray'], COLORS['red']]
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
    ### Data Storytelling: Monthly Trends in Road Accident Causes
    The analysis of monthly accident data reveals insightful patterns...
    - **May** emerges as the **riskiest month** with the highest total number of road accidents...
    - **Safety campaigns** and **law enforcement measures** should intensify during **May and June**...
    """)

elif section == "Daily Trends":
    st.header("Accidents by Day of the Week")
    # Stacked Bar Chart
    fig_bar = px.bar(
        daily_data,
        x='Accident Cause',
        y=['Friday', 'Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday'],
        title="Accident Causes by Day of Week",
        labels={'value': 'Number of Accidents', 'variable': 'Day of Week'},
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['gray'], COLORS['red'], '#8B5CF6', '#EC4899']
    )
    fig_bar.update_layout(barmode='stack')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Line Chart
    fig_line = px.line(
        daily_data.set_index('Accident Cause').T.reset_index(),
        x='index',
        y=['Weather', 'Drunk Driving', 'Mechanical Failure', 'Speeding', 'Distracted Driving'],
        title="Accident Causes by Day of the Week",
        labels={'index': 'Day of Week', 'value': 'Number of Accidents', 'variable': 'Accident Cause'},
        markers=True,
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['gray'], COLORS['red']]
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
    ### Wednesday—The Unexpected Danger Day on Roads
    The analysis of road accidents by day of the week reveals an insightful and somewhat unexpected trend...
    - **Midweek fatigue**, where drivers may be mentally drained...
    - **Midweek road safety campaigns** could prove crucial...
    """)

elif section == "Time of Day":
    st.header("Accidents by Time of Day")
    # Stacked Bar Chart
    fig_bar = px.bar(
        time_data,
        x='Accident Cause',
        y=['Afternoon', 'Evening', 'Morning', 'Night'],
        title="Accident Causes by Time of Day",
        labels={'value': 'Number of Accidents', 'variable': 'Time of Day'},
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['gray']]
    )
    fig_bar.update_layout(barmode='stack')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Line Chart
    fig_line = px.line(
        time_data.set_index('Accident Cause').T.reset_index(),
        x='index',
        y=['Mechanical Failure', 'Drunk Driving', 'Speeding', 'Distracted Driving', 'Weather'],
        title="Accident Causes by Time of Day",
        labels={'index': 'Time of Day', 'value': 'Number of Accidents', 'variable': 'Accident Cause'},
        markers=True,
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['gray'], COLORS['red']]
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
    ### How Time of Day Influences Road Accidents by Cause
    The data clearly reveals that time of day significantly impacts the type and frequency of road accidents...
    - **Evening and Night** hours are the most dangerous periods...
    - **Increased nighttime patrols** and **alcohol checkpoints** could help...
    """)

elif section == "Road Type and Location":
    st.header("Accidents by Road Type and Location")
    # Heatmap
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=road_type_data[['Minor', 'Moderate', 'Severe']].values,
        x=['Minor', 'Moderate', 'Severe'],
        y=road_type_data['Urban/Rural'] + ' - ' + road_type_data['Road Type'],
        colorscale='YlOrRd',
        showscale=True
    ))
    fig_heatmap.update_layout(
        title="Accident Severity by Road Type and Location",
        xaxis_title="Accident Severity",
        yaxis_title="Urban/Rural & Road Type"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("""
    ### How Road Type and Location Influence Accident Severity
    The data reveals that accident severity varies significantly depending on the road type...
    - **Rural Areas**: Highways record the highest number of severe accidents...
    - **Urban Areas**: Main roads have the highest severe accident count...
    """)

elif section == "Weather Conditions":
    st.header("Accidents by Weather Conditions")
    # Bar Chart
    weather_counts = filtered_data['Weather Conditions'].value_counts().reindex(['Windy', 'Rainy', 'Clear', 'Snowy', 'Foggy'])
    fig_bar = px.bar(
        x=weather_counts.index,
        y=weather_counts.values,
        title="Accident Frequency by Weather Condition",
        labels={'x': 'Weather Condition', 'y': 'Number of Accidents'},
        color_discrete_sequence=[COLORS['primary']]
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Stacked Bar Chart
    fig_stacked = px.bar(
        weather_data,
        x='Weather Conditions',
        y=['Minor', 'Moderate', 'Severe'],
        title="Accident Severity Distribution by Weather Condition",
        labels={'value': 'Number of Accidents', 'variable': 'Accident Severity'},
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent']]
    )
    fig_stacked.update_layout(barmode='stack')
    st.plotly_chart(fig_stacked, use_container_width=True)

    st.markdown("""
    ### The Hidden Dangers of Weather Conditions on Road Accident Severity
    This data shows that adverse weather conditions have a noticeable impact...
    - **Rainy Conditions**: Highest severe accident count...
    - **Road safety measures** like weather-responsive speed limits...
    """)

elif section == "Outcomes by Cause":
    st.header("Outcomes by Accident Cause")
    # Stacked Bar Chart
    fig_bar = px.bar(
        severity_data,
        x='Accident Cause',
        y=['Minor', 'Moderate', 'Severe'],
        title="Accident Severity by Accident Cause",
        labels={'value': 'Number of Accidents', 'variable': 'Accident Severity'},
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent']]
    )
    fig_bar.update_layout(barmode='stack')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Line Chart
    fig_line = px.line(
        severity_data,
        x='Accident Cause',
        y=['Minor', 'Moderate', 'Severe'],
        title="Accident Severity by Accident Cause",
        labels={'value': 'Number of Accidents', 'variable': 'Severity Level'},
        markers=True,
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent']]
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
    ### Outcomes by Accident Cause
    Distracted Driving is the leading cause of severe accidents...
    - **Efforts to reduce distracted and drunk driving** could have the biggest impact...
    """)

# Footer
st.markdown(
    f"""
    <div class="footer">
        <p>Created for portfolio showcase | biult by Sammdetech.com</p>
    </div>
    """,
    unsafe_allow_html=True
)
