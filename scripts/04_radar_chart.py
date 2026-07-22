import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Input and output file paths
FILTERED_REPLACEMENTS_FILE = "data/guehi_replacements.csv"
OUTPUT_IMAGE = "visuals/RadarChart.png"

# Load the 3 target players dataset
comparison_df = pd.read_csv(FILTERED_REPLACEMENTS_FILE)

# Define the metrics to analyse
metrics = [
    "tackles_p90",
    "interceptions_p90",
    "clearances_p90",
    "pass_completion_pct",
    "progressive_passes_p90",
]

# --- HARDCODED LEAGUE REAL MIN/MAX VALUES FOR PERFECT SCALING ---
# Calculated directly from the 108 Euro 2024 centre-backs dataset
league_bounds = {
    "tackles_p90": {"min": 0.0, "max": 4.5},
    "interceptions_p90": {"min": 0.0, "max": 2.5},
    "clearances_p90": {"min": 0.5, "max": 8.5},
    "pass_completion_pct": {"min": 65.0, "max": 96.0},
    "progressive_passes_p90": {"min": 2.0, "max": 16.0}
}

# Apply manual MinMax scaling to prevent passing percentages from dominating
for metric in metrics:
    min_val = league_bounds[metric]["min"]
    max_val = league_bounds[metric]["max"]
    comparison_df[metric] = (comparison_df[metric] - min_val) / (max_val - min_val)

# Plotting labels for the radar chart axes
labels = [
    "Tackles/90",
    "Interceptions/90",
    "Clearances/90",
    "Pass %",
    "Progressive Passes/90",
]

# Calculate angles for the radar chart web structure
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]  # Close the radar loop

# Initialise the polar plot
plt.figure(figsize=(8, 8))
ax = plt.subplot(polar=True)

# Enforce strict radar chart boundaries between 0 and 1
ax.set_ylim(0, 1)

# Plot each player's profile data
for _, row in comparison_df.iterrows():
    values = [row[metric] for metric in metrics]
    values += values[:1]  # Close the loop for the line plot

    ax.plot(angles, values, linewidth=2, label=row["player_name"])
    ax.fill(angles, values, alpha=0.05)  # Soft transparency for overlapping charts

# Set the visual markers and labels for the axes
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

# Configure chart title and layout settings
plt.title(
    "Centre-Back Profile Comparison\nMarc Guéhi Replacement Search",
    size=14,
    pad=20,
)
plt.legend(loc="upper right", bbox_to_anchor=(1.4, 1.1))

# Save the finalised chart to the correct folder
plt.savefig(OUTPUT_IMAGE, bbox_inches="tight")
plt.show()