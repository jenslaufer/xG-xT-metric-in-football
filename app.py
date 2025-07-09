import streamlit as st
import polars as pl  # Using Polars instead of Pandas
import numpy as np
import altair as alt  # Using Altair instead of Matplotlib/Seaborn

st.set_page_config(layout="wide", page_title="xG & xT Explainer")

st.title("Understanding Expected Goals (xG) and Expected Threat (xT)")

st.markdown("""
Welcome to this interactive explainer for two advanced football analytics metrics:
**Expected Goals (xG)** and **Expected Threat (xT)**. These metrics provide deeper insights
into the quality of chances and the danger created by player actions on the pitch.
""")

st.header("1. Expected Goals (xG)")

st.markdown("""
**What is xG?**

Expected Goals (xG) is a metric that quantifies the **probability** that a shot will result
in a goal, based on the characteristics of that shot and the events leading up to it.
It's a statistical measure that assigns a value between 0 and 1 to every shot.

* **0 xG:** An extremely unlikely goal (e.g., a shot from your own half).
* **1 xG:** A guaranteed goal (e.g., an open net from 1 yard out).

**How is xG calculated?**

xG models are built using historical data from thousands of shots. Machine learning algorithms
are trained to identify patterns and relationships between various features of a shot and
whether it resulted in a goal. Common features used in xG models include:

* **Shot Location:** Distance from goal, angle to goal.
* **Body Part:** Head, left foot, right foot.
* **Type of Assist:** Through ball, cross, cut-back, rebound.
* **Defensive Pressure:** Number of defenders between the shooter and goal, proximity of defenders.
* **Goalkeeper Position:** Is the keeper out of position?
* **Game State:** Score difference, time remaining.
* **Big Chance:** Was it a clear goal-scoring opportunity?

**Why is xG useful?**

* **Evaluates Shot Quality:** It allows us to assess how good a chance was, independent of whether it was scored.
* **Measures Attacking Performance:** A team with high xG is creating good chances, even if they aren't scoring many goals in a particular game.
* **Identifies Over/Underperformers:** Players or teams consistently scoring significantly more than their xG might be clinical finishers (or lucky), while those scoring less might be poor finishers (or unlucky).
* **Predictive Power:** xG is often a better predictor of future goal-scoring than actual goals over small sample samples.
""")

st.subheader("xG Example: Visualizing Shot Locations")

st.markdown("""
Imagine a simple xG model that only considers the distance from the goal.
Shots closer to the goal would have a higher xG.
""")

# Dummy shot data (x, y, xG value) - assuming goal is at (100, 35)
# Using Polars DataFrame
shots_data = pl.DataFrame({
    "x": [85, 70, 90, 60, 95, 75],
    "y": [35, 40, 25, 50, 36, 30],
    "xG": [0.7, 0.3, 0.5, 0.1, 0.8, 0.4]
})

# Define pitch dimensions
PITCH_WIDTH = 100
PITCH_HEIGHT = 70
GOAL_WIDTH = 7.32  # Approx 7.32m -> ~7.32 units on a 70 unit pitch height
PENALTY_BOX_LENGTH = 16.5
PENALTY_BOX_WIDTH = 40.0  # Approx 40.0 units for 16.5m length

# Create base chart for pitch (as a transparent rectangle)
pitch_outline = alt.Chart(pl.DataFrame({
    'x_start': [0], 'y_start': [0], 'x_end': [PITCH_WIDTH], 'y_end': [PITCH_HEIGHT]
}).to_pandas()).mark_rect(
    fill='lightgreen',
    stroke='black',
    strokeWidth=2,
    opacity=0.1
).encode(
    x=alt.X('x_start', scale=alt.Scale(domain=[0, PITCH_WIDTH])),
    y=alt.Y('y_start', scale=alt.Scale(domain=[0, PITCH_HEIGHT])),
    x2='x_end',
    y2='y_end'
).properties(
    width=700,
    height=450
)

# Pitch lines (simplified for Altair)
pitch_lines = pl.DataFrame([
    {'x': PITCH_WIDTH / 2, 'y': 0, 'x2': PITCH_WIDTH / 2, 'y2': PITCH_HEIGHT},
])

pitch_line_chart = alt.Chart(pitch_lines.to_pandas()).mark_rule(
    color='black',
    strokeWidth=1
).encode(
    x=alt.X('x', scale=alt.Scale(domain=[0, PITCH_WIDTH])),
    y=alt.Y('y', scale=alt.Scale(domain=[0, PITCH_HEIGHT])),
    x2='x2',
    y2='y2'
)

# Penalty boxes (simplified as rectangles)
left_pb_x1 = 0
left_pb_x2 = PENALTY_BOX_LENGTH
left_pb_y1 = (PITCH_HEIGHT - PENALTY_BOX_WIDTH) / 2
left_pb_y2 = (PITCH_HEIGHT + PENALTY_BOX_WIDTH) / 2

right_pb_x1 = PITCH_WIDTH - PENALTY_BOX_LENGTH
right_pb_x2 = PITCH_WIDTH
right_pb_y1 = (PITCH_HEIGHT - PENALTY_BOX_WIDTH) / 2
right_pb_y2 = (PITCH_HEIGHT + PENALTY_BOX_WIDTH) / 2

penalty_boxes = pl.DataFrame([
    {'x': left_pb_x1, 'y': left_pb_y1, 'x2': left_pb_x2, 'y2': left_pb_y2},
    {'x': right_pb_x1, 'y': right_pb_y1, 'x2': right_pb_x2, 'y2': right_pb_y2},
])

penalty_box_chart = alt.Chart(penalty_boxes.to_pandas()).mark_rect(
    fill=None,
    stroke='black',
    strokeWidth=1
).encode(
    x=alt.X('x', scale=alt.Scale(domain=[0, PITCH_WIDTH])),
    y=alt.Y('y', scale=alt.Scale(domain=[0, PITCH_HEIGHT])),
    x2='x2',
    y2='y2'
)

# Goals (simplified as thick lines)
goals = pl.DataFrame([
    {'x': 0, 'y': (PITCH_HEIGHT - GOAL_WIDTH) / 2, 'x2': 0,
     'y2': (PITCH_HEIGHT + GOAL_WIDTH) / 2},
    {'x': PITCH_WIDTH, 'y': (PITCH_HEIGHT - GOAL_WIDTH) / 2,
     'x2': PITCH_WIDTH, 'y2': (PITCH_HEIGHT + GOAL_WIDTH) / 2},
])

goal_chart = alt.Chart(goals.to_pandas()).mark_rule(
    color='red',
    strokeWidth=4
).encode(
    x=alt.X('x', scale=alt.Scale(domain=[0, PITCH_WIDTH])),
    y=alt.Y('y', scale=alt.Scale(domain=[0, PITCH_HEIGHT])),
    x2='x2',
    y2='y2'
)

# Shot data visualization
shot_chart = alt.Chart(shots_data.to_pandas()).mark_circle(
    size=200,
    stroke='black',
    strokeWidth=1,
    opacity=0.8
).encode(
    x=alt.X('x', scale=alt.Scale(domain=[0, PITCH_WIDTH]), axis=None),
    y=alt.Y('y', scale=alt.Scale(domain=[0, PITCH_HEIGHT]), axis=None),
    color=alt.Color('xG',
                    scale=alt.Scale(scheme='viridis', domain=[0, 1]),
                    legend=alt.Legend(title="Expected Goals (xG)")),
    tooltip=['x', 'y', alt.Tooltip('xG', format='.1f')]
)

# Add text labels for xG values
text_chart = alt.Chart(shots_data.to_pandas()).mark_text(
    align='left',
    baseline='middle',
    dx=10,
    dy=0,
    fontSize=10,
    fontWeight='bold'
).encode(
    x=alt.X('x', scale=alt.Scale(domain=[0, PITCH_WIDTH])),
    y=alt.Y('y', scale=alt.Scale(domain=[0, PITCH_HEIGHT])),
    text=alt.Text('xG', format='.1f'),
    color=alt.value('black')
)

# Combine all layers
xg_chart = alt.layer(
    pitch_outline,
    pitch_line_chart,
    penalty_box_chart,
    goal_chart,
    shot_chart,
    text_chart
).properties(
    title="Example Shots with Hypothetical xG Values",
    width=700,
    height=450
).resolve_scale(
    color='independent'
).configure_view(
    stroke=None
)

st.altair_chart(xg_chart, use_container_width=True)

st.markdown("""
* **Green/Yellow dots** represent shots with higher xG (more likely to be a goal).
* **Purple/Blue dots** represent shots with lower xG (less likely to be a goal).

This visual demonstrates how xG assigns a probability based on the shot's characteristics,
even before the outcome is known.
""")

st.header("2. Expected Threat (xT)")

st.markdown("""
**What is xT?**

Expected Threat (xT) is a more advanced metric that measures how much a player's action
(e.g., a pass, a dribble) **increases or decreases the probability of their team scoring a goal**
in the *future*. Unlike xG, which focuses on the final shot, xT considers the entire sequence
of play and the value of moving the ball into more dangerous areas of the pitch.

xT is often calculated using a **pitch control model** or a **Markov chain model** that
divides the pitch into a grid. Each grid cell is assigned an xG value, representing the
average xG of shots taken from that specific cell.

**How is xT calculated (simplified)?**

1.  **Pitch Grid:** The football pitch is divided into a grid (e.g., 10x10 or 16x12 cells).
2.  **Cell Value:** Each cell is assigned a "threat value" based on the average xG of shots taken from that cell. Cells closer to the opponent's goal and more central typically have higher threat values.
3.  **Action Value:** When a player makes an action (e.g., a pass from cell A to cell B), the xT value of that action is calculated as:
    `xT(Action) = Threat Value(Cell B) - Threat Value(Cell A)`
    If the ball moves into a more dangerous cell, the xT value is positive. If it moves into a less dangerous cell, it's negative.

**Why is xT useful?**

* **Values Non-Shot Actions:** xT recognizes the importance of actions that don't directly lead to a shot but set up future opportunities (e.g., a progressive pass into the final third).
* **Measures Playmaking Ability:** It helps identify players who consistently move the ball into high-threat areas, even if they aren't always getting the assist or the goal.
* **Evaluates Ball Progression:** It provides a way to quantify how effectively a team progresses the ball up the pitch and into dangerous zones.
* **Identifies Creative Players:** Players like deep-lying playmakers or wingers who make incisive passes are often highlighted by xT.
""")

st.subheader("xT Example: Visualizing Pitch Threat")

st.markdown("""
Here's a simplified visualization of a pitch grid with hypothetical threat values.
Darker shades indicate higher threat.
""")

# Create a dummy pitch grid for xT
grid_rows = 8
grid_cols = 12
xt_grid_np = np.zeros((grid_rows, grid_cols))

# Assign hypothetical threat values (higher closer to goal, more central)
for r in range(grid_rows):
    for c in range(grid_cols):
        # Simple heuristic: threat increases with column index (closer to goal)
        # and is higher in central rows
        threat = (c / grid_cols) * 0.8  # Scale from 0 to 0.8
        if r >= grid_rows / 4 and r < 3 * grid_rows / 4:  # Central rows
            threat += 0.2  # Add bonus for central areas
        xt_grid_np[r, c] = threat

# Convert numpy array to Polars DataFrame for Altair heatmap
xt_data = []
for r_idx in range(grid_rows):
    for c_idx in range(grid_cols):
        xt_data.append({
            "row": r_idx,
            "col": c_idx,
            "threat": xt_grid_np[r_idx, c_idx]
        })
xt_df = pl.DataFrame(xt_data)

# Create Altair heatmap
xt_chart = alt.Chart(xt_df.to_pandas()).mark_rect().encode(
    x=alt.X('col:O', title="Pitch Columns (closer to opponent's goal)",
            axis=alt.Axis(labels=False, ticks=False)),
    y=alt.Y('row:O', title="Pitch Rows",
            axis=alt.Axis(labels=False, ticks=False)),
    color=alt.Color('threat:Q', scale=alt.Scale(scheme='blues'),
                    legend=alt.Legend(title="Threat Value (xT)")),
    tooltip=['row', 'col', alt.Tooltip('threat', format='.2f')]
).properties(
    title="Hypothetical Pitch Threat Grid (xT Values)",
    width=800,
    height=400
)

st.altair_chart(xt_chart, use_container_width=True)

st.markdown("""
* **Darker cells** represent areas with higher threat values (more likely to lead to a goal).
* **Lighter cells** represent areas with lower threat values.

Now, consider a pass from a player:
* **Pass A:** From a light blue cell to a dark blue cell. This pass would have a **positive xT** value, as it moves the ball into a more dangerous area.
* **Pass B:** From a dark blue cell to a light blue cell (e.g., a back pass under pressure). This pass would have a **negative xT** value, as it moves the ball into a less dangerous area.

xT helps us understand the true value of ball progression and creativity on the pitch, beyond just goals and assists.
""")

st.header("Conclusion")

st.markdown("""
Both xG and xT are powerful tools in modern football analytics.
* **xG** helps us understand the quality of goal-scoring chances.
* **xT** helps us understand the value of ball progression and creating dangerous situations.

By combining these metrics, analysts and coaches can gain a much more comprehensive understanding
of team and player performance, moving beyond simple goal counts to evaluate the underlying
processes that lead to success.
""")

st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit")
