from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.append('/opt/airflow/src')

from include.extract import load_universities
from include.geocode import geocode_dataframe
from include.spatial import filter_european_universities
from include.viz import generate_folium_map

with DAG(
    dag_id="university_geo_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["universities", "geospatial"]
) as dag:

    def extract_task():
        gdf = load_universities("/usr/local/airflow/include/data/top_universities.csv")
        gdf.to_pickle("/tmp/universities_raw.pkl")

    def geocode_task():
        import pandas as pd
        from include.geocode import geocode_dataframe
        gdf = pd.read_pickle("/tmp/universities_raw.pkl")
        gdf_geo = geocode_dataframe(gdf)
        gdf_geo.to_pickle("/tmp/universities_geocoded.pkl")

    def spatial_join_task():
        import pandas as pd
        gdf = pd.read_pickle("/tmp/universities_geocoded.pkl")
        europe = filter_european_universities(gdf, "/usr/local/airflow/include/data/ne_110m_admin_0_countries")
        europe.to_pickle("/tmp/european_universities.pkl")
        europe.to_csv("/usr/local/airflow/include/data/european_universities.csv", index=False)

    def folium_map_task():
        import pandas as pd
        gdf = pd.read_pickle("/tmp/european_universities.pkl")
        generate_folium_map(gdf, "/usr/local/airflow/include/data/universities_map.html")

    extract = PythonOperator(task_id="extract", python_callable=extract_task)
    geocode = PythonOperator(task_id="geocode", python_callable=geocode_task)
    spatial = PythonOperator(task_id="spatial_join", python_callable=spatial_join_task)
    visualize = PythonOperator(task_id="generate_map", python_callable=folium_map_task)

    extract >> geocode >> spatial >> visualize
