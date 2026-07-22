import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


INPUT = "data/guehi_replacements.csv"


df = pd.read_csv(INPUT)


# Players to compare
players = [
    "Marc Guehi",
    "Robin Aime Robert Le Normand",
    "Riccardo Calafiori"
]


metrics = [
    "tackles_p90",
    "interceptions_p90",
    "clearances_p90",
    "pass_completion_pct",
    "progressive_passes_p90"
]


# Get available players
comparison = df[
    df["player_name"].isin(players)
].copy()


# Add Guehi if he is missing
if "Marc Guehi" not in comparison["player_name"].values:

    guehi = df[
        df["player_name"]
        .str.contains("Marc Guehi",
                      case=False,
                      na=False)
    ]

    comparison = pd.concat(
        [comparison, guehi]
    )


# Percentile normalization
for metric in metrics:

    comparison[metric] = (
        comparison[metric]
        /
        df[metric].max()
    )


labels = [
    "Tackles/90",
    "Interceptions/90",
    "Clearances/90",
    "Pass %",
    "Progressive Passes/90"
]


angles = np.linspace(
    0,
    2*np.pi,
    len(labels),
    endpoint=False
).tolist()


angles += angles[:1]


plt.figure(figsize=(8,8))

ax = plt.subplot(
    polar=True
)


for _, row in comparison.iterrows():

    values = [
        row[m]
        for m in metrics
    ]

    values += values[:1]

    ax.plot(
        angles,
        values,
        linewidth=2,
        label=row["player_name"]
    )

    ax.fill(
        angles,
        values,
        alpha=0.1
    )


ax.set_xticks(
    angles[:-1]
)

ax.set_xticklabels(labels)


plt.title(
    "Centre Back Profile Comparison\nMarc Guéhi Replacement Search",
    size=14
)


plt.legend(
    loc="upper right",
    bbox_to_anchor=(1.4,1.1)
)


plt.savefig(
    "data/guehi_radar.png",
    bbox_inches="tight"
)


plt.show()