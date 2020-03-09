import numpy as np
import pandas as pd
import ast 
import re
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils import shuffle

# Read in data
df = pd.read_csv('../data/raw_google_data_la.csv')

# Drop columns: 'Unnamed: 0', 'icon', and 'photos'
df.drop(columns=['Unnamed: 0', 'icon', 'id', 'photos', 'reference'], inplace=True)

# Change 'opening_hours' from str to bool
df['opening_hours'] = [ast.literal_eval(df['opening_hours'][i]).get('open_now') 
                       if pd.isnull(df['opening_hours'][i]) is False else
                       df['opening_hours'][i]
                       for i in df.index ]
df.rename(columns={'opening_hours':'open_now'}, inplace=True )

# Get zip code (and city or state) from 'formatted_address', and create new columns
ZIPCODE_RE = re.compile(r'\b\d{5}(-\d{4})?\b')  

# Define a function to match the regular expression constant above
def parse_zipcode_from_address(string):
    match = re.search(ZIPCODE_RE, string)
    
    # If match fails, raise error showing the failed match string
    if match is None:
        #raise Exception(string)
        zipcode = None
        print(f'no zipcode {string}')
    #  Return a dictionary object
    else:
        zipcode = match.group(0)
        
    return {'zipcode': zipcode}

# Apply the parse_address function to column 'formatted_address'
df = pd.concat([pd.DataFrame(
    list(df['formatted_address'].apply(parse_zipcode_from_address).values)), df], 
    axis=1, copy=True)

# All zipcodes appear in the formatted address from which they're taken
#assert all([x in y for (x, y) in df[['zipcode', 'formatted_address']].values])

# Drop the 'formatted_address' column
df.drop(columns='formatted_address', inplace=True)

# Get lat, lng from 'geometry', and create new columns
def parse_geometry(df):
    # Catch observations where geometry contains NaNs
    lat_list = []
    long_list = []
    for i in df.index:
        geometry = df['geometry'][i]
        try:
            lat = ast.literal_eval(geometry).get('location').get('lat')
            long = ast.literal_eval(geometry).get('location').get('lng')
        except ValueError:
            print(f'Error evaling {geometry} at {i} on {df.iloc[i]}')
            continue
            
        lat_list.append(lat)
        long_list.append(long)
        
    df['location_lat'] = lat_list
    df['location_lng'] = long_list
    return df

df = parse_geometry(df)

# Drop the 'geometry' column
df.drop(columns='geometry', inplace=True)

# Get 'compound_code', 'global_code' from 'plus_code', and create new columns
df['compound_code'] = [ast.literal_eval(df['plus_code'][i]).get('compound_code')
                       if pd.isnull(df['plus_code'][i]) is False else
                       df['plus_code'][i]
                       for i in df.index]
df['global_code'] = [ast.literal_eval(df['plus_code'][i]).get('global_code')
                     if pd.isnull(df['plus_code'][i]) is False else
                     df['plus_code'][i]
                     for i in df.index]

# Drop the 'plus_code' column
df.drop(columns='plus_code', inplace=True)

# Use CountVectorizer to process 'types'
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['types'])
vectorizerized_types = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
df = pd.concat([df, vectorizerized_types], axis=1, copy=True)
df.drop(columns='types', inplace=True)

# Drop duplicates
df.drop_duplicates(subset=['place_id'], keep='first', inplace=True)

# Shuffle the dataset
index = df.index
df = shuffle(df)
df.index = index

#Export clean dataset as csv
df.to_csv('../data/clean_google_data_la.csv', index=False)