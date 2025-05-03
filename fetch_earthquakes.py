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

if __name__ == '__main__':
     df = fetch_earthquakes('2020-01-01', '2025-04-01', min_mag=5)
     print(df.head())