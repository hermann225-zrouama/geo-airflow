import folium
from folium import Marker

def generate_folium_map(gdf, output_path):
    m = folium.Map(location=[54, 15], tiles='openstreetmap', zoom_start=3)
    
    for _, row in gdf.iterrows():
        Marker(
            [row['Latitude'], row['Longitude']],
            popup=row['Name']
        ).add_to(m)

    m.save(output_path)
