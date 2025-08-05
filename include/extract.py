import pandas as pd

def load_universities(csv_path):
    return pd.read_csv(csv_path, encoding="latin-1")
