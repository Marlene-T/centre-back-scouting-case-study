import ast
import os
import numpy as np
import pandas as pd

# File path configurations
EVENT_FILE = "data/euro2024_events.csv"
LINEUP_FILE = "data/euro2024_lineups.csv"
OUT_FILE = "data/centre_back_metrics_v2.csv"

# Minimum minutes required to qualify for analysis (3 full matches)
MINUTES_REQUIRED = 270

print("Loading data...")
events = pd.read_csv(EVENT_FILE, low_memory=False)
lineups = pd.read_csv(LINEUP_FILE)

print("Events loaded:", len(events))
print("Lineups loaded:", len(lineups))

# -----------------------------
# Identify Centre-Backs
# -----------------------------
centre_back_positions = [
    "Center Back",
    "Left Center Back",
    "Right Center Back"
]

# Filter lineups for players occupying central defensive positions
centre_backs = lineups[
    lineups["positions"]
    .astype(str)
    .str.contains("|".join(centre_back_positions), regex=True)
].copy()

print("Unique centre-backs found:", centre_backs["player_name"].nunique())

# -----------------------------
# Estimate Minutes Played
# -----------------------------
# Aggregate total matches played per player per team
minutes_df = (
    centre_backs
    .groupby(["player_name", "team"])
    .size()
    .reset_index(name="matches")
)

# Standardise calculation assuming 90 minutes per match appearance
minutes_df["minutes"] = minutes_df["matches"] * 90

# Filter out players who do not meet the minimum game-time threshold
minutes_df = minutes_df[minutes_df["minutes"] >= MINUTES_REQUIRED]
eligible_players = minutes_df["player_name"].tolist()

# -----------------------------
# Filter Event Data
# -----------------------------
df = events[events["player"].isin(eligible_players)].copy()

# -----------------------------
# Extract Defensive Metrics
# -----------------------------
def check_is_tackle(row):
    """Scans relevant event attributes to identify valid tackle actions."""
    target_keywords = ["duel_type", "sub_type", "outcome", "type"]
    combined_text_values = []

    for column_name in row.index:
        if column_name.lower() in target_keywords:
            combined_text_values.append(str(row[column_name]).lower())

    combined_text = " ".join(combined_text_values)
    return "tackle" in combined_text or ("won" in combined_text and "duel" in combined_text)

# Flag rows representing tackle actions
df["is_tackle"] = df.apply(check_is_tackle, axis=1)

# Aggregate defensive actions per player
defensive_metrics = (
    df.groupby("player")
    .agg(
        tackles=("is_tackle", "sum"),
        interceptions=("type", lambda x: (x == "Interception").sum()),
        clearances=("type", lambda x: (x == "Clearance").sum())
    )
    .reset_index()
)

# -----------------------------
# Extract Passing Metrics
# -----------------------------
passes_df = df[df["type"] == "Pass"].copy()

# A pass is successful if no negative outcome is logged
passes_df["completed"] = passes_df["pass_outcome"].isna()

passing_metrics = (
    passes_df
    .groupby("player")
    .agg(
        total_passes=("type", "count"),
        completed_passes=("completed", "sum")
    )
    .reset_index()
)

# Calculate accuracy percentage
passing_metrics["pass_completion_pct"] = (
    passing_metrics["completed_passes"]
    / passing_metrics["total_passes"]
    * 100
)

# -----------------------------
# Extract Progressive Passes
# -----------------------------
def check_progressive_pass(row):
    """Determines if a forward pass covers a distance greater than 20 units."""
    try:
        start_coord = row["location"]
        end_coord = row["pass_end_location"]

        if isinstance(start_coord, str):
            start_coord = ast.literal_eval(start_coord)

        if isinstance(end_coord, str):
            end_coord = ast.literal_eval(end_coord)

        # Calculate forward distance covered along the pitch x-axis
        forward_distance = end_coord[0] - start_coord[0]
        return forward_distance > 20
    except (ValueError, SyntaxError, TypeError, KeyError):
        return False

passes_df["is_progressive"] = passes_df.apply(check_progressive_pass, axis=1)

progressive_metrics = (
    passes_df
    .groupby("player")["is_progressive"]
    .sum()
    .reset_index()
    .rename(columns={"is_progressive": "progressive_passes"})
)

# -----------------------------
# Merge and Finalise Dataset
# -----------------------------
final_result = (
    minutes_df
    .merge(defensive_metrics, left_on="player_name", right_on="player", how="left")
    .merge(passing_metrics, left_on="player_name", right_on="player", how="left")
    .merge(progressive_metrics, left_on="player_name", right_on="player", how="left")
)

# Clean redundant columns and fill missing data entries with zeros
final_result = final_result.drop(columns=["player_x", "player_y"], errors="ignore")
final_result = final_result.fillna(0)

# Calculate standard Per-90 performance metrics
final_result["tackles_p90"] = (final_result["tackles"] / final_result["minutes"]) * 90
final_result["interceptions_p90"] = (final_result["interceptions"] / final_result["minutes"]) * 90
final_result["clearances_p90"] = (final_result["clearances"] / final_result["minutes"]) * 90
final_result["progressive_passes_p90"] = (final_result["progressive_passes"] / final_result["minutes"]) * 90

# Export structured metrics to CSV file
final_result.to_csv(OUT_FILE, index=False)

print("\nDataset successfully saved to:")
print(OUT_FILE)

print("\nSample output preview:")
print(
    final_result[
        [
            "player_name",
            "team",
            "minutes",
            "tackles",
            "tackles_p90",
            "interceptions_p90",
            "clearances_p90",
            "pass_completion_pct",
            "progressive_passes_p90"
        ]
    ]
    .head(20)
)