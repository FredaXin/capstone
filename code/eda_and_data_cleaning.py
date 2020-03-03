#EDA and Data Cleaning Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.utils import shuffle

# Read in data
google = pd.read_csv('../data/clean_google_data_la.csv')
income = pd.read_csv('../data/clean_income_by_zip_la.csv')

# Merge Goolge dataset with Income dataset
df = pd.merge(google, income, how='inner', left_on='zipcode', right_on='zipcode')

# Shuffle the dataset
index = df.index
df = shuffle(df)
df.index = index

# Feature Engineering
# Create interaction column using Google dataset
df['price_level*rating'] = df['price_level'] * df['rating']

# Create aggregated features for each zip code

# Create column 'avg_price_level_by_zipcode', which calculate the avg price level for each zipcode
df['avg_price_level_by_zipcode'] = [df.groupby('zipcode')['price_level'].mean()[zipcode] 
                                    for zipcode in df['zipcode']]

# Avarage rating by zipcode
df['avg_rating_by_zipcode'] = [df.groupby('zipcode')['rating'].mean()[zipcode] 
                               for zipcode in df['zipcode']]

# Avarage rating_count by zipcode
df['avg_user_ratings_total_by_zipcode'] = [df.groupby('zipcode')['user_ratings_total'].mean()[zipcode] 
                                           for zipcode in df['zipcode']]

# Total number of bars by zipcode. 
# Limitation: this approach has limiattion since our dataset is merely a sample of the businesses for each zipcode.
df['total_number_of_bars_by_zipcode'] = [df.groupby('zipcode')['bar'].sum()[zipcode] 
                                         for zipcode in df['zipcode']]

# Total number of cafe by zipcode. 
# Limitation: this approach has limiattion since our dataset is merely a sample of the businesses for each zipcode.
df['total_number_of_cafes_by_zipcode'] = [df.groupby('zipcode')['cafe'].sum()[zipcode] 
                                          for zipcode in df['zipcode']]

# Create transformation columns using demographic information from 'income' dataset
# Create column user ratings counts devided by the population in the given zipcode
df['user_ratings_total_per_capita'] = df['user_ratings_total'] / df['population']

# Create column rating weighed with population density in the given zipcode
df['rating_weighed_population_density'] = df['rating'] * df['population_density_square_miles']

# drop_first=False since we might not use linear regression models
df = pd.get_dummies(df, columns=['open_now'], drop_first=False, dummy_na=True)

df.to_csv('../data/final_la.csv', index=False)
