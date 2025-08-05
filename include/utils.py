import os

def get_db_url():
    return os.getenv("DB_URL", "postgresql://geouser:geopass@postgres:5432/geodb")
