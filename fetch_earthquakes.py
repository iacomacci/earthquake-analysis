import requests
import pandas as pd
from datetime import datetime

#API endpoint parameters.

def fetch_earthquakes(start, end, min_mag=5):
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

        params = {
            "format": "geojson",
            "starttime": start,
            "endtime": end,
            "minmagnitude": min_mag
        }

        response = requests.get(url, params=params)
        response.raise_for_status() #Raise an error for bad responses
        data = response.json()['features']

        records = []
        for feature in data:
            properties = feature['properties']
            geometry = feature['geometry']['coordinates']
            records.append({
                'time': datetime.utcfromtimestamp(properties['time']/1000),
                'magnitude': properties['mag'],
                'location': properties['place'],
                'longitude': geometry[0],
                'latitude': geometry[1],
                'depth_km': geometry[2]
            })
        return pd.DataFrame(records)

def get_earthquake_data(start='2015-01-01', end='2025-04-01', min_mag=5):

    print('\nFetching Earthquake Data...')
    df = fetch_earthquakes(start, end, min_mag)

    # Cleaning and Data processing
    #print(df.isnull().sum()) #Columns present no missing values.
    df = df.dropna(subset=["magnitude", "depth_km"])

    df['year'] = df['time'].dt.year     #Derived into year and month.
    df['month'] = df['time'].dt.month

    # Exploratory Data Analysis

    #print(df[['magnitude','depth_km']].describe())
    df["mag_bin"] = pd.cut(df["magnitude"],
                        bins=[5,6,7,8,10],
                        labels=["Moderate (5-6)", "Strong (6-7)", "Major (7-8)", "Great (8-10)"],
                        right=False)
    #print(df["mag_bin"].value_counts().sort_index())

    yearly = df.groupby('year').size()
    monthly = df.groupby('month').size()
    print('Fetched Earthquake Data successfully!')

    return df, yearly, monthly
    

if __name__ == '__main__':
     df, yearly, monthly = get_earthquake_data()
     print(df.head())