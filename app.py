import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mplsoccer
from mplsoccer import Pitch
import numpy as np

st.set_page_config(page_title="xG & xT Demo", layout="wide")

# --- Header ---
st.title("📊 Expected Goals (xG) and Expected Threat (xT) Explained")
st.markdown("""
This interactive app helps **laypeople understand** the concepts of expected goals (xG) and expected threat (xT) in football.
It also includes tools for **professionals** to explore and analyze custom match data.
""")

# --- Section 1: xG Explanation ---
st.header("⚽ What is Expected Goals (xG)?")
st.markdown("""
- **xG** measures the probability that a shot will result in a goal.
- It considers factors like:
  - Distance to goal
  - Angle of the shot
  - Shot type (header, volley, etc.)
""")

# Example shot chart
pitch = Pitch(pitch_type='statsbomb', line_zorder=2)
fig, ax = pitch.draw(figsize=(8, 5))

# Sample shots with xG values
shots = pd.DataFrame({
    'x': [102, 94, 88],
    'y': [34, 20, 40],
    'xg': [0.85, 0.35, 0.10]
})

for _, shot in shots.iterrows():
    pitch.scatter(shot['x'], shot['y'], s=800*shot['xg'],
                  alpha=0.6, ax=ax, color='red')
    ax.text(shot['x'], shot['y']+2,
            f"xG: {shot['xg']:.2f}", ha='center', fontsize=10)

st.pyplot(fig)

# --- Section 2: xT Explanation ---
st.header("📈 What is Expected Threat (xT)?")
st.markdown("""
- **xT** estimates how much an action increases the chance of scoring.
- It values **passes**, **dribbles**, and **movement**, not just shots.

Imagine it like chess: every move changes the game state and potential.
""")

# Create random demo events for xT visualization
np.random.seed(42)
x = np.random.uniform(0, 120, 300)
y = np.random.uniform(0, 80, 300)
xt_values = np.random.uniform(0, 0.3, 300)  # synthetic xT values

# Bin and visualize
pitch = Pitch(pitch_type='statsbomb')
fig, ax = pitch.draw(figsize=(8, 5))

bin_stat = pitch.bin_statistic(
    x, y, values=xt_values, statistic='mean', bins=(30, 20))
pitch.heatmap(bin_stat, ax=ax, cmap='Reds', alpha=0.6)
pitch.scatter(x, y, ax=ax, color='black', s=5, alpha=0.2)

st.pyplot(fig)

# --- Section 3: Upload Your Match Data ---
st.header("📂 Upload Match Data to Explore")
uploaded_file = st.file_uploader(
    "Upload a CSV with shot/pass data (x, y, event_type, xg/xT)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())

    pitch = Pitch(pitch_type='statsbomb')
    fig, ax = pitch.draw(figsize=(9, 6))

    for _, row in df.iterrows():
        if row['event_type'] == 'shot':
            pitch.scatter(row['x'], row['y'], ax=ax, s=800 *
                          row['xg'], color='blue', alpha=0.6)
        elif row['event_type'] == 'pass':
            pitch.scatter(row['x'], row['y'], ax=ax, s=800 *
                          row['xT'], color='green', alpha=0.6)

    st.pyplot(fig)

# --- Section 4: Learn More ---
st.header("🔍 Learn More")
st.markdown("""
- xG Model Tutorial: [StatsBomb Guide](https://statsbomb.com/articles/soccer/statsbomb-xg-model/)
- xT Calculation: [Karun Singh’s Blog](https://karun.in/blog/expected-threat.html)
""")


# Footer (outside both tabs so it always shows)
st.markdown("""
---
#### Interested in Dev, AI, Modeling, Uncertainty, Decision Support Tools, or Sports Analytics?

This demo was created by Jens Laufer from [Solytics GmbH](https://www.solytics.de) — a team passionate about empowering better decisions under uncertainty.

We specialize in:

- Custom analytics and simulation tools  
- Forecasting, risk modeling, and decision intelligence  
- Data-driven product development  

👉 [Visit solytics.de](https://www.solytics.de) — we’d love to hear from you.

""")
