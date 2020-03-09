import pandas as pd
import numpy as np

from sklearn.utils import shuffle

# Define constance
LOCATION = 'la'

# Read in data
google = pd.read_csv(f'../data/clean_google_data_{LOCATION}_agg.csv')
income = pd.read_csv(f'../data/clean_income_by_zip_{LOCATION}.csv')

# Merge Goolge dataset with Income dataset
df = pd.merge(google, income, how='inner', on='zipcode')
print(df.shape)

# Shuffle the dataset
index = df.index
df = shuffle(df)
df.index = index

# Feature Engineering
##Create interaction column using Google dataset
df['price_level*rating'] = df['mean_price_level'] * df['mean_rating']

## Create interaction columns using both Google dataset and Income dataset
### Create column user ratings counts devided by the population in the given zipcode
df['user_ratings_total_per_capita'] = df['mean_user_ratings_total'] / df['population']

### Create column rating weighted with population density in the given zipcode
df['rating*population_density'] = df['mean_rating'] * df['population_density_square_miles']

# Log-transform the target to normalize the distribution
df['log_home_price_to_income_ratios'] = np.log(df['home_price_to_income_ratios'])
df.drop(columns=['home_price_to_income_ratios'], inplace=True)

# Export final dataset
df.to_csv(f'../data/final_{LOCATION}_agg.csv', index=False)