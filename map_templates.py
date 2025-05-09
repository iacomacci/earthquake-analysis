#HTML templates for Folium map
# These templates are used to create a legend and title for the Folium map.

earthquakes_map_legend_html = '''
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

earthquakes_map_title_html = """
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

earthquakes_DBSCAN_map_title_html = """
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
        Global Earthquake Cluster Map (Magnitude ≥ 5, 2015–2025)
    </h3>
{% endmacro %}
"""

def earthquakes_DBSCAN_map_build_legend_html(color_dict):
    items = ""
    for cluster_id, color in color_dict.items():
        items += f'<i style="background:{color}; width:10px; height:10px; display:inline-block;"></i> Cluster {cluster_id}<br>'
    return f"""
    {{% macro html(this, kwargs) %}}
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        z-index: 9999;
        background-color: white;
        padding: 10px;
        border: 2px solid black;
        font-size: 14px;
    ">
        <b>Earthquake Clusters</b><br>
        {items}
    </div>
    {{% endmacro %}}
    """