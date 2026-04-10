from statsbombpy import sb
import pandas as pd

# Load all Bundesliga 2023/24 matches
matches = sb.matches(competition_id=9, season_id=281)
match_ids = matches['match_id'].tolist()

all_shots = []

for match_id in match_ids:
    events = sb.events(match_id=match_id)
    shots = events[events['type'] == 'Shot'].copy()
    if len(shots) > 0:
        shots['match_id'] = match_id
        all_shots.append(shots)

# Combine all matches
all_shots_df = pd.concat(all_shots, ignore_index=True)

# Build player summary
player_stats = all_shots_df.groupby(['player', 'team']).agg(
    shots=('type', 'count'),
    goals=('shot_outcome', lambda x: (x == 'Goal').sum()),
    xG=('shot_statsbomb_xg', 'sum'),
    xG_per_shot=('shot_statsbomb_xg', 'mean')
).reset_index()

player_stats['xG_per_shot'] = player_stats['xG_per_shot'].round(3)
player_stats['xG'] = player_stats['xG'].round(3)
player_stats['conversion_rate'] = (player_stats['goals'] / player_stats['shots']).round(3)

# Save to CSV
player_stats.to_csv('/Users/chriszaimi/Desktop/bundesliga_player_stats.csv', index=False)
print("Done! Rows:", len(player_stats))
print(player_stats.sort_values('xG', ascending=False).head(10))