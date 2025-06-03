import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv("miami_heat_2023.csv")

# Drop technical columns not useful for the user
df.drop(columns=["TEAM_ID", "TEAM_ABBREVIATION"], inplace=True, errors="ignore")

# Rename columns for display
df.rename(columns={
    "SEASON_ID": "Season",
    "GAME_ID": "Game",
    "TEAM_NAME": "Team",
    "MATCHUP": "Matchup",
    "GAME_DATE": "Date",
    "WL": "Result",
    "PTS": "Points",
    "REB": "Rebounds",
    "AST": "Assists",
    "STL": "Steals",
    "BLK": "Blocks",
    "TOV": "Turnovers",
    "PF": "Fouls",
    "PLUS_MINUS": "PlusMinus",
    "OPPONENT": "Opponent"
}, inplace=True)

df.reset_index(drop=True, inplace=True)

# Sidebar controls
st.sidebar.title("Filter Options")

# Title and intro
st.title("Miami Heat 2023 Playoff Dashboard")
st.write("Interactive dashboard built with Streamlit showing 2023 playoff stats.")

# Radio to filter by win/loss
st.subheader("Filter by Game Result")
result = st.radio("Select Result:", ["All", "Win", "Loss"])
if result == "Win":
    filtered_df = df[df["Result"] == "W"]
elif result == "Loss":
    filtered_df = df[df["Result"] == "L"]
else:
    filtered_df = df

# Interactive table
st.subheader("Filtered Game Stats")
st.dataframe(filtered_df, use_container_width=True)

# Bar chart: Points per game
st.subheader("Points Scored per Game")
st.bar_chart(filtered_df["Points"])

# Button for high-scoring games
if st.button("Show games with 110+ points"):
    high_scoring_games = filtered_df[filtered_df["Points"] >= 110]
    st.success(f"{len(high_scoring_games)} games found with 110 or more points.")
    st.dataframe(high_scoring_games, use_container_width=True)

# Feedback
if len(filtered_df) < len(df):
    st.warning(f"Filtered down to {len(filtered_df)} games from {len(df)} total.")

# Slider: minimum points
min_pts = st.slider("Minimum Points", min_value=int(df["Points"].min()), max_value=int(df["Points"].max()), value=100)
slider_df = filtered_df[filtered_df["Points"] >= min_pts]
st.subheader(f"Games with at least {min_pts} points")
st.dataframe(slider_df.reset_index(drop=True), use_container_width=True)  # Suppress index here

# Selectbox: opponent filter
if "Opponent" in df.columns:
    opponents = sorted(df["Opponent"].unique())
    selected_opp = st.selectbox("Select Opponent:", options=["All"] + opponents)
    if selected_opp != "All":
        slider_df = slider_df[slider_df["Opponent"] == selected_opp]
        st.write(f"Filtered games against {selected_opp}:")
        st.dataframe(slider_df.reset_index(drop=True), use_container_width=True)

#  Checkbox
if st.checkbox("Show all games again"):
    st.info("Showing full dataset again below.")
    st.dataframe(df, use_container_width=True)

# Map
st.subheader("Game Location: Miami Home Base")
miami_coords = pd.DataFrame({"lat": [25.7617], "lon": [-80.1918]})
st.map(miami_coords)

# Final feedback
st.info("This dashboard was built using Streamlit.")

