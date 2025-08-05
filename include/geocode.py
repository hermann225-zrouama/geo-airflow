import pandas as pd
from geopy.geocoders import Nominatim
import time

def geocode_dataframe(df):
    geolocator = Nominatim(user_agent="geo_pipeline")
    
    def my_geocoder(name):
        try:
            loc = geolocator.geocode(name, timeout=10)
            if loc:
                return pd.Series({'Latitude': loc.latitude, 'Longitude': loc.longitude})
        except:
            pass
        return pd.Series({'Latitude': None, 'Longitude': None})
    
    geo_df = df.copy()
    geo_df[['Latitude', 'Longitude']] = geo_df['Name'].apply(my_geocoder)
    geo_df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    return geo_df
