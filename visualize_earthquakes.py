import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import folium
import time
from branca.element import Template, MacroElement
from fetch_earthquakes import get_earthquake_data

df, yearly, monthly = get_earthquake_data()

fig1, (ax1,ax2) = plt.subplots(2,1)

ax1.hist(df["magnitude"], bins=20)
ax1.set_xlabel("Magnitude")
ax1.set_ylabel("Count")
ax1.set_title("Distribution of Earthquake Magnitudes")

ax2.scatter(df["depth_km"], df["magnitude"], s=10,c='#FF00FF')
ax2.set_xlabel("Depth (km)")
ax2.set_ylabel("Magnitude")
ax2.set_title("Depth vs. Magnitude")

plt.tight_layout()
plt.show()

fig2, (ax3,ax4) = plt.subplots(2,1)
ax3.bar(yearly.index, yearly.values, color='green')
ax3.set_xlabel('Year')
ax3.set_ylabel('Earthquake Count')
ax4.set_title('Earthquake Count over the years')

ax4.bar(monthly.index, monthly.values, color='orange')
ax4.set_label('Month')
ax4.set_ylabel('Earthquake Count')
ax4.set_title('Earthquake Count Per Month (All years)')
ax4.set_xticks(monthly.index)
ax4.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

plt.tight_layout()
plt.show()


# Normalize magnitudes to 0–1 range
norm = colors.Normalize(vmin=5, vmax=10)
cmap = cm.get_cmap('YlOrRd')  # Yellow -> Orange -> Red

map_center = [df['latitude'].mean(), df['longitude'].mean()]
m = folium.Map(location=[0, 0], zoom_start=2)

for _, row in df.iterrows():

    magnitude = row['magnitude']
    color_rgb = cmap(norm(magnitude))  # RGBA
    color_hex = colors.to_hex(color_rgb)

    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['magnitude'],  # scaled by magnitude
        popup=f"{row['location']}: M{row['magnitude']}",
        color=color_hex,
        fill=True,
        fill_color=color_hex,
        fill_opacity=0.4
    ).add_to(m)

# HTML Legend and title setup
legend_html = '''
<div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 160px;
    height: 160px;
    background-color: white;
    border:2px solid grey;
    z-index:9999;
    font-size:14px;
    padding: 10px;
">
<b>Magnitude Legend</b><br>
<i style="background: #ffffb2; width: 18px; height: 18px; float: left; margin-right: 8px;"></i>5.0 – 6.0<br>
<i style="background: #fecc5c; width: 18px; height: 18px; float: left; margin-right: 8px;"></i>6.0 – 7.0<br>
<i style="background: #fd8d3c; width: 18px; height: 18px; float: left; margin-right: 8px;"></i>7.0 – 8.0<br>
<i style="background: #f03b20; width: 18px; height: 18px; float: left; margin-right: 8px;"></i>8.0 – 9.0<br>
<i style="background: #bd0026; width: 18px; height: 18px; float: left; margin-right: 8px;"></i>9.0 – 10.0
</div>
'''

title_html = """
{% macro html(this, kwargs) %}
    <h3 style="position: fixed; 
               top: 10px; left: 50px; width: 100%; 
               z-index:9999;
               font-size:20px;
               font-weight:bold;
               background-color: white;
               padding: 10px;
               border-radius: 8px;
               box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">
        Global Earthquake Map (Magnitude ≥ 5, 2015–2025)
    </h3>
{% endmacro %}
"""

m.get_root().html.add_child(folium.Element(legend_html))

macro = MacroElement()
macro._template = Template(title_html)
m.get_root().add_child(macro)

m.save("earthquakes_map.html")


