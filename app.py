import streamlit as st
import polars as pl
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# Set page config
st.set_page_config(
    page_title="xG & xT Football Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enable Altair themes
alt.themes.enable('default')


def create_football_pitch():
    """Create a professional football pitch visualization using mplsoccer"""
    pitch = Pitch(pitch_type='opta', pitch_color='#4CAF50',
                  line_color='white', linewidth=3)
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.patch.set_facecolor('white')
    return fig, ax


def calculate_xg(distance, angle, shot_type="foot", assist_type="none"):
    """Simplified xG calculation - distance in meters"""
    # Base probability decreases with distance (adjusted for meters)
    base_prob = max(0.1, 0.8 - (distance / 27))

    # Angle modifier (shots from center are better)
    angle_modifier = 1 - abs(angle) / 90

    # Shot type modifier
    shot_modifiers = {
        "foot": 1.0,
        "header": 0.7,
        "volley": 1.2,
        "penalty": 3.0
    }

    # Assist type modifier
    assist_modifiers = {
        "none": 1.0,
        "cross": 0.8,
        "through_ball": 1.3,
        "corner": 0.6,
        "free_kick": 1.1
    }

    xg = (base_prob * angle_modifier *
          shot_modifiers.get(shot_type, 1.0) *
          assist_modifiers.get(assist_type, 1.0))

    return min(xg, 0.9)  # Cap at 90%


def calculate_xt_zones():
    """Create xT zones for the pitch"""
    # Simplified xT grid (12x8)
    xt_values = np.array([
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.01, 0.01, 0.01],
        [0.00, 0.00, 0.00, 0.00, 0.01, 0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.03],
        [0.00, 0.00, 0.01, 0.01, 0.01, 0.02, 0.02, 0.03, 0.04, 0.04, 0.05, 0.06],
        [0.00, 0.01, 0.01, 0.02, 0.02, 0.03, 0.04, 0.05, 0.08, 0.12, 0.15, 0.20],
        [0.00, 0.01, 0.01, 0.02, 0.02, 0.03, 0.04, 0.05, 0.08, 0.12, 0.15, 0.20],
        [0.00, 0.00, 0.01, 0.01, 0.01, 0.02, 0.02, 0.03, 0.04, 0.04, 0.05, 0.06],
        [0.00, 0.00, 0.00, 0.00, 0.01, 0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.03],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.01, 0.01, 0.01]
    ])
    return xt_values


def main():
    st.markdown("# ⚽ Football Analytics: xG & xT Explained")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a section:", [
        "Introduction",
        "Expected Goals (xG)",
        "Expected Threat (xT)",
        "Interactive xG Calculator",
        "xT Heatmap",
        "Real Examples",
        "Quiz & Practice"
    ])

    if page == "Introduction":
        st.markdown("## Welcome to Football Analytics")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### What is xG (Expected Goals)?")
            st.write("xG measures the quality of a scoring chance. It assigns a probability (between 0 and 1) to each shot based on historical data of similar shots.")

        with col2:
            st.markdown("### What is xT (Expected Threat)?")
            st.write("xT measures how much a player's action increases their team's likelihood of scoring. It considers the value of different pitch positions.")

        st.markdown("### Why These Metrics Matter")
        st.write("""
        - **Performance Analysis**: Understand if goals were due to skill or luck
        - **Player Evaluation**: Compare players beyond just goals and assists  
        - **Team Strategy**: Identify the most dangerous areas of the pitch
        - **Recruitment**: Find undervalued players with good underlying numbers
        """)

        # Simple example
        st.markdown("### Quick Example")
        st.write(
            "**Scenario:** Player A scores from 5 meters (xG: 0.8), Player B scores from 27 meters (xG: 0.05)")
        st.write(
            "**Insight:** Player A's goal was expected, Player B's was exceptional!")

    elif page == "Expected Goals (xG)":
        st.markdown("## Expected Goals (xG) Deep Dive")

        st.markdown("### How xG is Calculated")
        st.write("""
        xG models use machine learning on thousands of historical shots, considering:
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.write("""
            **Shot Location Factors:**
            - Distance from goal
            - Angle to goal
            - Position relative to penalty area
            """)

        with col2:
            st.write("""
            **Situational Factors:**
            - Type of shot (foot, header, volley)
            - Type of assist (cross, through ball, etc.)
            - Number of defenders between shooter and goal
            """)

        # xG visualization
        st.markdown("### xG by Distance and Angle")

        # Convert to meters (5-32m instead of 5-35 yards)
        distances = np.linspace(5, 32, 50)
        angles = [0, 15, 30, 45, 60]

        # Create data for Altair
        chart_data = []
        for angle in angles:
            for distance in distances:
                xg_value = calculate_xg(distance, angle)
                chart_data.append({
                    'Distance': distance,
                    'xG': xg_value,
                    'Angle': f'{angle}° angle'
                })

        chart_df = pl.DataFrame(chart_data)

        chart = alt.Chart(chart_df.to_pandas()).mark_line(strokeWidth=3).encode(
            x=alt.X('Distance:Q', title='Distance from Goal (meters)'),
            y=alt.Y('xG:Q', title='xG Probability'),
            color=alt.Color('Angle:N',
                            scale=alt.Scale(range=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])),
            tooltip=['Distance:Q', 'xG:Q', 'Angle:N']
        ).properties(
            title='xG Probability by Distance and Angle',
            width=600,
            height=400
        ).resolve_scale(
            color='independent'
        )

        st.altair_chart(chart, use_container_width=True)

        st.markdown("### xG Ranges")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Big Chance", "0.35+", "High probability")
        with col2:
            st.metric("Half Chance", "0.1 - 0.35", "Medium probability")
        with col3:
            st.metric("Low Chance", "< 0.1", "Low probability")

    elif page == "Expected Threat (xT)":
        st.markdown("## Expected Threat (xT) Explained")

        st.write("""
        Expected Threat measures the value of ball possession at different areas of the pitch.
        It answers: "How likely is this position to lead to a goal?"
        """)

        st.markdown("### How xT Works")
        st.write("""
        1. **Pitch Division**: The pitch is divided into a grid (typically 12x8 or 16x12 zones)
        2. **Historical Analysis**: Each zone gets a value based on how often possession there leads to goals
        3. **Action Value**: xT = Value of end zone - Value of start zone
        """)

        # Create xT heatmap with mplsoccer pitch
        xt_zones = calculate_xt_zones()

        # Create professional pitch
        pitch = Pitch(pitch_type='opta', pitch_color='#4CAF50',
                      line_color='white', linewidth=2)
        fig, ax = pitch.draw(figsize=(12, 8))
        fig.patch.set_facecolor('white')

        # Create heatmap overlay (adjust coordinates for mplsoccer)
        im = ax.imshow(xt_zones, cmap='Reds', aspect='auto',
                       extent=[0, 100, 0, 100], alpha=0.6)

        ax.set_title('Expected Threat (xT) Heatmap', fontsize=16,
                     color='black', fontweight='bold')

        # Simple colorbar
        cbar = plt.colorbar(im, ax=ax, label='xT Value', shrink=0.6)
        cbar.set_label('xT Value', color='black', fontweight='bold')
        st.pyplot(fig)

        st.markdown("### Key Insights")
        col1, col2 = st.columns(2)

        with col1:
            st.write("""
            **High xT Zones:**
            - Central areas near penalty box
            - Wide areas close to goal
            - Areas just outside penalty area
            """)

        with col2:
            st.write("""
            **Low xT Zones:**
            - Defensive third
            - Wide areas far from goal
            - Areas behind the ball
            """)

    elif page == "Interactive xG Calculator":
        st.markdown("## Interactive xG Calculator")

        st.write("Adjust the parameters below to see how xG changes:")

        col1, col2 = st.columns([2, 1])

        with col2:
            distance = st.slider("Distance from goal (meters)", 5, 35, 15)
            angle = st.slider("Angle from center (degrees)", -60, 60, 0)
            shot_type = st.selectbox("Shot Type",
                                     ["foot", "header", "volley", "penalty"])
            assist_type = st.selectbox("Assist Type",
                                       ["none", "cross", "through_ball", "corner", "free_kick"])

            # Calculate xG
            xg_value = calculate_xg(distance, angle, shot_type, assist_type)

            st.markdown("### Result")
            st.metric("Expected Goals (xG)", f"{xg_value:.3f}",
                      f"{xg_value*100:.1f}% chance")

            # Interpretation
            if xg_value >= 0.35:
                st.success("🎯 Big Chance!")
            elif xg_value >= 0.1:
                st.warning("⚽ Half Chance")
            else:
                st.info("🤏 Low Chance")

        with col1:
            # Create pitch with shot position using mplsoccer
            fig, ax = create_football_pitch()

            # mplsoccer opta coordinates: 1 unit = 1 meter exactly
            # Goal is at x=100, penalty area at x=83.5 (16.5m from goal)
            x_pos = 100 - distance  # Direct 1:1 conversion
            y_pos = 50 + (angle / 60) * 30  # Scale angle to pitch width

            # Plot shot position with clear visibility
            ax.scatter(x_pos, y_pos, s=200, c='red', edgecolors='black', linewidth=2,
                       label=f'Shot (xG: {xg_value:.3f})', zorder=5)
            ax.plot([x_pos, 100], [y_pos, 50], 'r--', linewidth=2, alpha=0.8)

            # Simple legend
            ax.legend(loc='upper left', fontsize=12,
                      facecolor='white', edgecolor='black')
            ax.set_title(f'Shot Position - Distance: {distance}m, Angle: {angle}°',
                         fontsize=14, color='black', fontweight='bold', pad=15)

            st.pyplot(fig)

    elif page == "xT Heatmap":
        st.markdown("## Interactive xT Heatmap")

        st.write("Click on the pitch below to see xT values for different positions:")

        # Create interactive xT heatmap with Altair
        xt_zones = calculate_xt_zones()

        # Create data for Altair heatmap
        heatmap_data = []
        for i in range(xt_zones.shape[0]):
            for j in range(xt_zones.shape[1]):
                heatmap_data.append({
                    'x': j,
                    'y': i,
                    'xT_value': xt_zones[i, j]
                })

        heatmap_df = pl.DataFrame(heatmap_data)

        heatmap_chart = alt.Chart(heatmap_df.to_pandas()).mark_rect().encode(
            x=alt.X('x:O', title='Pitch Length', axis=alt.Axis(labels=False)),
            y=alt.Y('y:O', title='Pitch Width', axis=alt.Axis(labels=False)),
            color=alt.Color('xT_value:Q',
                            scale=alt.Scale(scheme='reds'),
                            title='xT Value'),
            tooltip=['x:O', 'y:O', 'xT_value:Q']
        ).properties(
            title='Expected Threat (xT) Heatmap - Hover to Explore',
            width=600,
            height=400
        )

        st.altair_chart(heatmap_chart, use_container_width=True)

        # xT examples
        st.markdown("### xT Action Examples")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Positive xT Actions")
            st.write("""
            - Progressive pass into penalty area: +0.15 xT
            - Dribble from midfield to final third: +0.08 xT
            - Cross from wide position: +0.05 xT
            """)

        with col2:
            st.markdown("#### Negative xT Actions")
            st.write("""
            - Back pass to goalkeeper: -0.03 xT
            - Sideways pass in own half: -0.01 xT
            - Lost possession in final third: -0.12 xT
            """)

    elif page == "Real Examples":
        st.markdown("## Real World Examples")

        # Create sample match data using Polars
        match_data = pl.DataFrame({
            'Player': ['Messi', 'Ronaldo', 'Haaland', 'Mbappé', 'Kane'],
            'Goals': [2, 1, 3, 1, 2],
            'xG': [1.2, 0.8, 2.1, 1.5, 1.8],
            'Assists': [1, 0, 0, 2, 1],
            'xT': [0.45, 0.32, 0.38, 0.52, 0.41]
        })

        match_data = match_data.with_columns(
            (pl.col('Goals') - pl.col('xG')).alias('xG_diff')
        )

        st.markdown("### Sample Match Performance")
        st.dataframe(match_data.to_pandas(), use_container_width=True)

        # Performance analysis
        col1, col2 = st.columns(2)

        # Convert to pandas for Altair compatibility
        match_df = match_data.to_pandas()

        with col1:
            scatter_chart = alt.Chart(match_df).mark_circle(size=100, color='#d62728').encode(
                x=alt.X('xG:Q', title='Expected Goals (xG)'),
                y=alt.Y('Goals:Q', title='Goals Scored'),
                tooltip=['Player:N', 'xG:Q', 'Goals:Q']
            ).properties(
                title='Goals vs Expected Goals',
                width=400,
                height=300
            )

            # Add diagonal line
            line_data = pl.DataFrame({'x': [0, 3], 'y': [0, 3]})
            line_chart = alt.Chart(line_data.to_pandas()).mark_line(
                strokeDash=[5, 5], color='gray'
            ).encode(
                x='x:Q',
                y='y:Q'
            )

            # Add text labels
            text_chart = alt.Chart(match_df).mark_text(
                align='left', baseline='middle', dx=5, dy=-5, fontSize=10
            ).encode(
                x='xG:Q',
                y='Goals:Q',
                text='Player:N'
            )

            combined_chart = (scatter_chart + line_chart + text_chart)
            st.altair_chart(combined_chart, use_container_width=True)

        with col2:
            bar_chart = alt.Chart(match_df).mark_bar().encode(
                x=alt.X('Player:N', title='Player'),
                y=alt.Y('xT:Q', title='Expected Threat (xT)'),
                color=alt.Color('xT:Q', scale=alt.Scale(scheme='blues')),
                tooltip=['Player:N', 'xT:Q']
            ).properties(
                title='Expected Threat by Player',
                width=400,
                height=300
            )

            st.altair_chart(bar_chart, use_container_width=True)

        st.markdown("### Analysis")
        st.write("""
        - **Haaland**: Scored more goals than expected (clinical finishing)
        - **Ronaldo**: Underperformed xG (unlucky or poor finishing)
        - **Mbappé**: Highest xT despite fewer goals (great creative play)
        """)

    elif page == "Quiz & Practice":
        st.markdown("## Test Your Knowledge")

        # Quiz questions
        st.markdown("### Quiz Questions")

        q1 = st.radio(
            "1. A shot from 6 yards in the center of goal has an xG of 0.8. What does this mean?",
            [
                "The shot will definitely score",
                "80% of similar shots historically result in goals",
                "The shot is worth 0.8 goals",
                "The player has 80% shooting accuracy"
            ]
        )

        q2 = st.radio(
            "2. Which area typically has the highest xT value?",
            [
                "Center circle",
                "Corner of the pitch",
                "Edge of penalty area",
                "Goalkeeper area"
            ]
        )

        q3 = st.radio(
            "3. A player has 2 goals from 0.5 xG. This suggests:",
            [
                "Poor finishing",
                "Excellent finishing",
                "Average performance",
                "The model is wrong"
            ]
        )

        if st.button("Check Answers"):
            score = 0
            if q1 == "80% of similar shots historically result in goals":
                st.success("Q1: Correct! ✅")
                score += 1
            else:
                st.error("Q1: Incorrect. xG represents historical probability.")

            if q2 == "Edge of penalty area":
                st.success("Q2: Correct! ✅")
                score += 1
            else:
                st.error("Q2: Incorrect. Edge of penalty area has highest xT.")

            if q3 == "Excellent finishing":
                st.success("Q3: Correct! ✅")
                score += 1
            else:
                st.error(
                    "Q3: Incorrect. Scoring more than xG suggests good finishing.")

            st.info(f"Your Score: {score}/3")

        # Practice scenario
        st.markdown("### Practice Scenario")
        st.write("""
        **Scenario**: A midfielder receives the ball 23 meters from goal, slightly to the right. 
        They can either:
        - Take a shot (estimated xG: 0.03)
        - Pass to a striker in the penalty area (estimated xG for striker: 0.25)
        
        Which action creates more value for the team?
        """)

        if st.button("Show Answer"):
            st.success("**Answer**: The pass creates more value!")
            st.write("""
            - Shot xG: 0.03
            - Pass leading to shot xG: 0.25
            - The midfielder's xT for the pass would be positive (~0.22)
            """)


if __name__ == "__main__":
    # Requirements: streamlit polars numpy altair matplotlib mplsoccer
    # All distances now use metric system (meters instead of yards)
    main()
