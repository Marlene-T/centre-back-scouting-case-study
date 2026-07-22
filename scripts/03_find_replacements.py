import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Input and output file paths
GLOBAL_DATA_FILE = "data/centre_back_metrics_v2.csv"  # The 108 defenders dataset
FILTERED_REPLACEMENTS_FILE = "data/guehi_replacements.csv"  # The 3 target players dataset
OUTPUT_IMAGE = "visuals/RadarChart.png"

# Load both datasets
df_global = pd.read_csv(GLOBAL_DATA_FILE)
df_replacements = pd.read_csv(FILTERED_REPLACEMENTS_FILE)

# Define the metrics to analyse
metrics = [
    "tackles_p90",
    "interceptions_p90",
    "clearances_p90",
    "pass_completion_pct",
    "progressive_passes_p90",
]

# --- THE ABSOLUTE VISUAL FIX ---
# Fit the scaler on all 108 defenders so the scale represents full league standards
scaler = MinMaxScaler()
scaler.fit(df_global[metrics])

# Transform ONLY our 3 selected players based on that league-wide benchmark
comparison_df = df_replacements.copy()
comparison_df[metrics] = scaler.transform(df_replacements[metrics])

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