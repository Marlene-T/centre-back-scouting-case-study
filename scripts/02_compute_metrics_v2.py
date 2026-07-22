import pandas as pd
import numpy as np
import os


EVENT_FILE = "data/euro2024_events.csv"
LINEUP_FILE = "data/euro2024_lineups.csv"
OUT_FILE = "data/centre_back_metrics_v2.csv"


MINUTES_REQUIRED = 270


print("Loading data...")

events = pd.read_csv(EVENT_FILE, low_memory=False)
lineups = pd.read_csv(LINEUP_FILE)


print("Events:", len(events))
print("Lineups:", len(lineups))


# -----------------------------
# Find centre backs
# -----------------------------

centre_back_positions = [
    "Center Back",
    "Left Center Back",
    "Right Center Back"
]


centre_backs = lineups[
    lineups["positions"]
    .astype(str)
    .str.contains("|".join(centre_back_positions))
]


print(
    "Centre backs found:",
    centre_backs["player_name"].nunique()
)


# minutes approximation

minutes = (
    centre_backs
    .groupby(["player_name", "team"])
    .size()
    .reset_index(name="matches")
)

minutes["minutes"] = minutes["matches"] * 90


minutes = minutes[
    minutes["minutes"] >= MINUTES_REQUIRED
]


players = minutes["player_name"].tolist()


# -----------------------------
# Defensive actions
# -----------------------------

df = events[
    events["player"].isin(players)
]


metrics = (
    df.groupby("player")
    .agg(
        tackles=("type",
                 lambda x: (x=="Tackle").sum()),

        interceptions=("type",
                 lambda x: (x=="Interception").sum()),

        clearances=("type",
                 lambda x: (x=="Clearance").sum())
    )
    .reset_index()
)


# -----------------------------
# Passing metrics
# -----------------------------

passes = df[df["type"]=="Pass"].copy()


passes["completed"] = passes["pass_outcome"].isna()


passing = (
    passes.groupby("player")
    .agg(
        passes=("type","count"),
        completed_passes=("completed","sum")
    )
    .reset_index()
)


passing["pass_completion_pct"] = (
    passing["completed_passes"]
    /
    passing["passes"]
    *
    100
)


# -----------------------------
# Progressive passes
# -----------------------------

def progressive_pass(row):

    try:
        start = row["location"]
        end = row["pass_end_location"]

        if isinstance(start,str):
            start = eval(start)

        if isinstance(end,str):
            end = eval(end)

        distance = end[0] - start[0]

        return distance > 20

    except:
        return False


passes["progressive"] = passes.apply(
    progressive_pass,
    axis=1
)


progressive_passes = (
    passes.groupby("player")["progressive"]
    .sum()
    .reset_index()
    .rename(columns={"progressive":
                     "progressive_passes"})
)


# -----------------------------
# Merge everything
# -----------------------------

result = (
    minutes
    .merge(metrics,
           left_on="player_name",
           right_on="player")
    .merge(passing,
           left_on="player_name",
           right_on="player",
           how="left")
    .merge(progressive_passes,
           left_on="player_name",
           right_on="player",
           how="left")
)


result = result.drop(
    columns=["player_x","player_y"],
    errors="ignore"
)


result["tackles_p90"] = (
    result["tackles"]
    /
    result["minutes"]
    *
    90
)

result["interceptions_p90"] = (
    result["interceptions"]
    /
    result["minutes"]
    *
    90
)

result["clearances_p90"] = (
    result["clearances"]
    /
    result["minutes"]
    *
    90
)

result["progressive_passes_p90"] = (
    result["progressive_passes"]
    /
    result["minutes"]
    *
    90
)


result.to_csv(
    OUT_FILE,
    index=False
)


print("\nSaved:")
print(OUT_FILE)


print(
    result[
        [
        "player_name",
        "team",
        "minutes",
        "tackles_p90",
        "interceptions_p90",
        "clearances_p90",
        "pass_completion_pct",
        "progressive_passes_p90"
        ]
    ]
    .head(20)
)