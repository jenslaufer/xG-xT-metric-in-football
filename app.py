import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="xG and xT Demo", layout="wide")

# Title and introduction
st.title("Expected Goals (xG) and Expected Threat (xT) Demo")
st.markdown("""
This app demonstrates the concepts of **Expected Goals (xG)** and **Expected Threat (xT)** in soccer analytics using synthetic data. 
- **xG**: Measures the probability of a shot resulting in a goal based on factors like shot location, angle, and type.
- **xT**: Quantifies the threat level of a player's action (e.g., pass, dribble) based on its potential to lead to a goal.
""")

# Generate synthetic data
np.random.seed(42)
shots = pd.DataFrame({
    'x': np.random.uniform(0, 120, 100),  # x-coordinate (0 to 120 yards)
    'y': np.random.uniform(0, 80, 100),   # y-coordinate (0 to 80 yards)
    'shot_type': np.random.choice(['header', 'foot', 'volley'], 100),
    'distance_to_goal': np.random.uniform(5, 40, 100),
    'angle_to_goal': np.random.uniform(0, 90, 100),
    'xG': np.random.uniform(0.01, 0.8, 100)  # Simulated xG values
})

actions = pd.DataFrame({
    'x_start': np.random.uniform(0, 120, 200),
    'y_start': np.random.uniform(0, 80, 200),
    'x_end': np.random.uniform(0, 120, 200),
    'y_end': np.random.uniform(0, 80, 200),
    'action_type': np.random.choice(['pass', 'dribble', 'cross'], 200),
    'xT': np.random.uniform(0.01, 0.5, 200)  # Simulated xT values
})

# xG Visualization
st.header("Expected Goals (xG) Visualization")
st.markdown("The scatter plot below shows shots on a soccer pitch, colored by their xG values. Higher xG values indicate a higher probability of scoring.")

# Create soccer pitch for xG
fig_xg = go.Figure()

# Add pitch outline
fig_xg.add_shape(type="rect", x0=0, y0=0, x1=120, y1=80, line=dict(color="Green"))
fig_xg.add_shape(type="rect", x0=102, y0=20, x1=120, y1=60, line=dict(color="Green"))  # Penalty area
fig_xg.add_shape(type="rect", x0=114, y0=30, x1=120, y1=50, line=dict(color="Green"))  # Goal area
fig_xg.add_shape(type="rect", x0=120, y0=36, x1=120.1, y1=44, line=dict(color="White"))  # Goal

# Add shots
fig_xg.add_trace(go.Scatter(
    x=shots['x'], y=shots['y'], mode='markers',
    marker=dict(size=10, color=shots['xG'], colorscale='Viridis', showscale=True, colorbar_title="xG"),
    text=shots['xG'].round(2), hoverinfo='text+x+y'
))

fig_xg.update_layout(
    title="Shots on Pitch with xG",
    xaxis=dict(range=[0, 120], showgrid=False, title="X (yards)"),
    yaxis=dict(range=[0, 80], showgrid=False, title="Y (yards)"),
    showlegend=False,
    plot_bgcolor="Green",
    width=800,
    height=500
)

st.plotly_chart(fig_xg)

# xG Data Table
st.subheader("Sample xG Data")
st.dataframe(shots[['x', 'y', 'shot_type', 'distance_to_goal', 'angle_to_goal', 'xG']].head())

# xT Visualization
st.header("Expected Threat (xT) Visualization")
st.markdown("The plot below shows actions (e.g., passes, dribbles) on the pitch, with arrows indicating movement direction and colored by xT values.")

# Create soccer pitch for xT
fig_xt = go.Figure()

# Add pitch outline
fig_xt.add_shape(type="rect", x0=0, y0=0, x1=120, y1=80, line=dict(color="Green"))
fig_xt.add_shape(type="rect", x0=102, y0=20, x1=120, y1=60, line=dict(color="Green"))
fig_xt.add_shape(type="rect", x0=114, y0=30, x1=120, y1=50, line=dict(color="Green"))
fig_xt.add_shape(type="rect", x0=120, y0=36, x1=120.1, y1=44, line=dict(color="White"))

# Add actions as arrows
for i, row in actions.iterrows():
    fig_xt.add_shape(
        type="line",
        x0=row['x_start'], y0=row['y_start'],
        x1=row['x_end'], y1=row['y_end'],
        line=dict(color=px.colors.sequential.Viridis[int(row['xT']*10)], width=2),
        name=f"xT: {row['xT']:.2f}"
    )

fig_xt.update_layout(
    title="Actions on Pitch with xT",
    xaxis=dict(range=[0, 120], showgrid=False, title="X (yards)"),
    yaxis=dict(range=[0, 80], showgrid=False, title="Y (yards)"),
    showlegend=False,
    plot_bgcolor="Green",
    width=800,
    height=500
)

st.plotly_chart(fig_xt)

# xT Data Table
st.subheader("Sample xT Data")
st.dataframe(actions[['x_start', 'y_start', 'x_end', 'y_end', 'action_type', 'xT']].head())

# Explanations
st.header("Understanding xG and xT")
st.markdown("""
- **xG Calculation**: Typically derived from logistic regression models using features like shot distance, angle, and type. In this demo, xG values are synthetic but represent realistic probabilities.
- **xT Calculation**: Measures the increase in goal-scoring probability from an action. It considers the starting and ending positions of actions like passes or dribbles. Higher xT values indicate actions closer to the goal or in dangerous areas.
- **Use Cases**: xG helps evaluate shot quality, while xT quantifies the value of non-shooting actions in creating goal-scoring opportunities.
""")

# Notes
st.markdown("**Note**: This demo uses synthetic data for illustration. Real-world xG and xT models require detailed match event data and advanced statistical modeling.")