from statsbombpy import sb
import pandas as pd
import os


os.makedirs("data", exist_ok=True)

competition_id = 55
season_id = 282


print("Downloading matches...")

matches = sb.matches(
    competition_id=competition_id,
    season_id=season_id
)

matches.to_csv(
    "data/euro2024_matches.csv",
    index=False
)


print("Downloading lineups...")

lineups = []

for match_id in matches["match_id"]:

    print("Lineup:", match_id)

    lineup = sb.lineups(match_id=match_id)

    for team, players in lineup.items():

        players["team"] = team
        players["match_id"] = match_id

        lineups.append(players)


all_lineups = pd.concat(lineups)


all_lineups.to_csv(
    "data/euro2024_lineups.csv",
    index=False
)


print("Lineups saved!")


print("Downloading events...")

events_list = []

for match_id in matches["match_id"]:

    print("Events:", match_id)

    events = sb.events(match_id=match_id)

    events["match_id"] = match_id

    events_list.append(events)


all_events = pd.concat(events_list)


all_events.to_csv(
    "data/euro2024_events.csv",
    index=False
)


print("Finished!")