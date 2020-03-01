import pandas as pd
import time
from pathlib import Path
import googlemaps


with open(str(Path.home() / 'api_keys/google_api.txt')) as file:
    API_KEY = file.read().replace('\n', '')

# Instance of making a single call
client = googlemaps.Client(key=API_KEY, queries_per_second=2)

LIST_OF_KEYWORDS = ['stores', 'restaurant', 'coffee shops']


def search_place(keyword, zipcode):
    '''
    Inputs one keyword and one zip code
    Send a single request
    Outputs up to 20 results
    '''
    json_result = client.places(f'{keyword} near {zipcode}')
    df_businesses = pd.DataFrame(json_result['results'])
    
    # Add columns searched_keyword and searched_zipcode to the dataframe
    df_businesses['searched_keyword'] = keyword
    df_businesses['searched_zipcode'] = zipcode
    return df_businesses

def serach_all_places(list_of_keywords, list_of_zipcodes):
    '''
    Inputs a list of keywords (n) and a list of zip codes (m)
    Send (n*m) requests
    Outputs up to (n*m*20) results
    '''
    df = pd.DataFrame()
    for zipcode in list_of_zipcodes:
        for keyword in list_of_keywords:
            df = df.append(search_place(keyword, zipcode), ignore_index=True, sort=False) 
    return df


if __name__ == '__main__':
    zcta = pd.read_csv('../data/zcta_la.csv')
    list_of_zcta = list(zcta['zcta'].values)

    data = serach_all_places(LIST_OF_KEYWORDS, list_of_zcta)

    data.to_csv('../data/raw_google_data_la.csv')