import numpy as np
import pandas as pd
from dateutil import parser
from datetime import datetime

# Load raw data from card dump
raw_data = pd.DataFrame(pd.read_json("./Data/MTG/scryfall-default-cards.json"))

# Filter data to keep only wanted cards

# Filter data to only keep rare and mythics
raw_data = raw_data.loc[raw_data['rarity'].isin(['mythic', 'rare'])]

# Filter to only keep english cards
raw_data = raw_data.loc[raw_data['lang'].isin(['en'])]

# Filter to only keep cards from core and expansion sets
raw_data = raw_data.loc[raw_data['set_type'].isin(['core', 'expansion'])]

# Remove cards to old. Goldfish starts price tracking at 2010-11-02
raw_data = raw_data[(raw_data['released_at'] > '2010-11-02' )]
raw_data = raw_data[(raw_data['released_at'] < '2018-07-02')]

# Check for duplicate names
# filtered_data = raw_data.to_numpy()
# unique_names = []
# duplicate_names = []
# for data in filtered_data:
#     if data[4] in unique_names:
#         duplicate_names.append(data[4])
#     else:
#         unique_names.append(data[4])
raw_data.to_csv("./Data/MTG/filtered_data.csv",index=False)