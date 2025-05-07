from fetch_earthquakes import get_earthquake_data


df, yearly, monthly = get_earthquake_data()

print('Number of Earthquakes:', len(df))
print('Data range:', df['year'].min(), 'to', df['year'].max())
print('Strongest Earthquake:', df['magnitude'].max())
print('Average Magnitude:', round(df['magnitude'].mean(),2))
print('Minimum Depth:', df['depth_km'].min(), 'km')
print('Maximum Depth:', df['depth_km'].max(), 'km')


print('____________________________________________________________________________________________________________________________')
print('Key information: \n ', 
      'Positive depth values indicate how far below the surface the earthquake occurred.')

print('A negative depth might suggest a surface-level event on high ground, like a mountain or volcano. \n',
      'But it is more often a data artifact or modeling inaccuracy—USGS and other agencies sometimes revise those values later')