# Import libraries
import numpy as np
import pandas as pd

# Read in data
df = pd.read_csv('../data/raw_income_by_zip_la.csv')

# Create column dictionary
col_dict = {
    'Zip (ZCTA)' : 'zipcode',
    'Median household income in the past 12 months (in 2018 inflation-adjusted dollars)' : 'median_household_income',
    'Population' : 'population',
    'Population Density (square miles) ' : 'population_density_square_miles',
    'Housing Units' : 'housing_units',
    'Median Value of Owner-occupied Units' : 'median_home_value'
}

# Change column names 
df = df.rename(columns=col_dict)

# Change datatypes
col_list_float = ['median_household_income', 'population_density_square_miles', 'median_home_value']
col_list_int = ['population', 'housing_units']

# Define fuction to change data types to float
def change_dtypes_float(df, col_list):
    for col in col_list:
        df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)
    return df

# Define fuction to change data types to int
def change_dtypes_int(df, col_list):
    for col in col_list:
        df[col] = df[col].replace('[\$,]', '', regex=True).astype(int)
    return df


df = change_dtypes_float(df, col_list_float)
df = change_dtypes_int(df, col_list_int)


# Create Target Column 'home_price_to_income_ratios'
df['home_price_to_income_ratios'] = df['median_home_value'] / df['median_household_income']

# Drop 'median_home_value' and 'median_household_income'
df.drop(columns=['median_home_value', 'median_household_income'], inplace=True)

df.to_csv('../data/clean_income_by_zip_la.csv', index=False)