import matplotlib.pyplot as plt
from fetch_earthquakes import get_earthquake_data

df = get_earthquake_data()

plt.hist(df["magnitude"], bins=20)
plt.xlabel("Magnitude")
plt.ylabel("Count")
plt.title("Distribution of Earthquake Magnitudes")
plt.show()