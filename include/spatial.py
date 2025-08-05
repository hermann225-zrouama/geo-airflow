import geopandas as gpd

def filter_european_universities(universities_df, shapefile_dir):
    universities = gpd.GeoDataFrame(
        universities_df,
        geometry=gpd.points_from_xy(universities_df.Longitude, universities_df.Latitude),
        crs="EPSG:4326"
    )

    world = gpd.read_file(f"{shapefile_dir}/ne_110m_admin_0_countries.shp")
    europe = world[world.CONTINENT == "Europe"]
    
    universities_in_europe = gpd.sjoin(universities, europe, how="inner", predicate="intersects")
    return universities_in_europe
