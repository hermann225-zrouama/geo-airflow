from sqlalchemy import create_engine

def load_to_postgis(gdf, table_name, db_url):
    engine = create_engine(db_url)
    gdf.to_postgis(name=table_name, con=engine, if_exists='replace')
