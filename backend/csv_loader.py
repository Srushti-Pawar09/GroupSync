import pandas as pd

def load_destinations():
    df = pd.read_csv("backend/data/PROJECT_CSV.csv")
    return df
