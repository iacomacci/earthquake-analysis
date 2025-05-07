import pandas as pd
from fetch_earthquakes import get_earthquake_data

df, yearly, monthly = get_earthquake_data()

print('____________________________________________________________________________________________________________________________')
print(f'Number of Earthquakes:      {len(df):,}')
print(f'Data range:                 {df['year'].min()} to {df['year'].max()}')
print(f'Strongest Earthquake:       {df['magnitude'].max()} Mw')
print(f'Average Magnitude:          {round(df['magnitude'].mean(),2)} Mw')
print(f'Minimum Depth:              {df['depth_km'].min()} km')
print(f'Maximum Depth:              {df['depth_km'].max()} km')

most_common_location = df['location'].mode()[0]
count_most_common_location = df['location'].value_counts()[most_common_location]

print(f"Most common location:       {most_common_location} (appears {count_most_common_location} times)")

print('____________________________________________________________________________________________________________________________')
print('Key information:\n', 
      'Positive depth values indicate how far below the surface the earthquake occurred.\n',
      'A negative depth might suggest a surface-level event on high ground, like a mountain or volcano. \n',
      'But it is more often a data artifact or modeling inaccuracy—USGS and other agencies sometimes revise those values later')
