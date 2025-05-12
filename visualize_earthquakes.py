import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import folium
from folium import Popup
from branca.element import Template, MacroElement
from fetch_earthquakes import get_earthquake_data
from map_templates import earthquakes_map_legend_html, earthquakes_map_title_html

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
plt.show(block=False)
plt.pause(5)  # Pause for 5 seconds
plt.close()

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
plt.show(block=False)
plt.pause(5)  # Pause for 5 seconds
plt.close()

# Normalize magnitudes to 0–1 range
norm = colors.Normalize(vmin=5, vmax=10)
cmap = cm.get_cmap('YlOrRd')  # Yellow -> Orange -> Red

map_center = [df['latitude'].mean(), df['longitude'].mean()]
map_earthquakes = folium.Map(location=[0, 0], zoom_start=2)

def create_popup(row):
    #Popup html setup
    return Popup(f"""
        <table style="font-size: 12px;">
        <tr><td><strong>Location:</strong></td><td>{row['location']}</td></tr>
        <tr><td><strong>Magnitude:</strong></td><td>{row['magnitude']}</td></tr>
        <tr><td><strong>Depth:</strong></td><td>{row['depth_km']} km</td></tr>
        </table>
    """, max_width=250)

def add_markers(map_obj, data):
    for _, row in data.iterrows():
        magnitude = row['magnitude']
        color_rgb = cmap(norm(magnitude))  # RGBA
        color_hex = colors.to_hex(color_rgb)
        popup = create_popup(row)
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['magnitude'],
            color=color_hex,
            fill=True,
            fill_color=color_hex,
            fill_opacity=0.4,
            popup=popup
        ).add_to(map_obj)

add_markers(map_earthquakes, df)


map_earthquakes.get_root().html.add_child(folium.Element(earthquakes_map_legend_html))

macro = MacroElement()
macro._template = Template(earthquakes_map_title_html)
map_earthquakes.get_root().add_child(macro)

map_earthquakes.save("earthquakes_map.html")


