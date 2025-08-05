def clean_data(gdf):
    gdf = gdf.to_crs(epsg=4326)
    gdf["area_km2"] = gdf.geometry.to_crs(epsg=3857).area / 1e6
    gdf["centroid"] = gdf.geometry.centroid
    return gdf

