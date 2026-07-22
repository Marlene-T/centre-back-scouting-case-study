import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Input and output file paths
INPUT_FILE = "data/guehi_replacements.csv"
OUTPUT_IMAGE = "visuals/RadarChart.png"

# Load the dataset
df = pd.read_csv(INPUT_FILE)

# --- DIAGNOSTIC STEP ---
# This prints all available player names in your console to verify spellings
print("\n--- Available players in your CSV file: ---")
print(df["player_name"].unique())
print("-------------------------------------------\n")

# Define the metrics to analyse
metrics = [
    "tackles_p90",
    "interceptions_p90",
    "clearances_p90",
    "pass_completion_pct",
    "progressive_passes_p90",
]

# Robust filtering: search using broad keywords to bypass accent or spelling mismatch bugs
matching_rows = []
keywords = ["Guehi", "Guéhi", "Marc", "Le Normand", "Calafiori"]

for keyword in keywords:
    match = df[df["player_name"].str.contains(keyword, case=False, na=False)]
    if not match.empty:
        matching_rows.append(match)

# Combine the matched players into a single DataFrame
if matching_rows:
    comparison_df = pd.concat(matching_rows).drop_duplicates(subset=["player_name"])
else:
    comparison_df = pd.DataFrame()

# Verify which players were captured for the plot
print("--- Selected players for the radar chart: ---")
print(comparison_df["player_name"].tolist())
print("---------------------------------------------\n")

# Apply global MinMax scaling based on the entire league standard
scaler = MinMaxScaler()
scaler.fit(df[metrics])
comparison_df[metrics] = scaler.transform(comparison_df[metrics])

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

# Enforce radar boundaries between 0 and 1 for strict consistency
ax.set_ylim(0, 1)

# Plot each player's profile data
for _, row in comparison_df.iterrows():
    values = [row[metric] for metric in metrics]
    values += values[:1]  # Close the loop for the line plot

    ax.plot(angles, values, linewidth=2, label=row["player_name"])
    ax.fill(angles, values, alpha=0.05)  # Soft opacity for overlapping profiles

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