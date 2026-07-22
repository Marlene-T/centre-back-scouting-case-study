import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances


INPUT = "data/centre_back_metrics_v2.csv"
OUTPUT = "data/guehi_replacements.csv"


df = pd.read_csv(INPUT)


# Metrics important for a modern CB
features = [
    "tackles_p90",
    "interceptions_p90",
    "clearances_p90",
    "pass_completion_pct",
    "progressive_passes_p90"
]


# Remove missing values
data = df.dropna(subset=features).copy()


# Scale metrics
scaler = StandardScaler()

scaled = scaler.fit_transform(
    data[features]
)


data_scaled = pd.DataFrame(
    scaled,
    columns=features
)


# Find Marc Guehi

guehi_index = data[
    data["player_name"]
    .str.contains("Marc Guehi",
                  case=False,
                  na=False)
].index[0]


guehi_position = data.index.get_loc(
    guehi_index
)


guehi_vector = scaled[guehi_position]


# Distance from Guehi

distances = euclidean_distances(
    scaled,
    [guehi_vector]
).flatten()


data["distance_to_guehi"] = distances


# Remove Guehi himself

results = data[
    ~data["player_name"]
    .str.contains("Marc Guehi",
                  case=False,
                  na=False)
]


results = results.sort_values(
    "distance_to_guehi"
)


results.to_csv(
    OUTPUT,
    index=False
)


print("\nClosest profiles to Marc Guehi:\n")

print(
    results[
        [
        "player_name",
        "team",
        "minutes",
        "distance_to_guehi"
        ]
    ]
    .head(15)
)