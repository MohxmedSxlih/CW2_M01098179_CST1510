import pandas as pd
from pathlib import Path

DATA_DIR = Path("DATA")

print("CYBER_INCIDENTS.CSV:")
df = pd.read_csv(DATA_DIR / "cyber_incidents.csv")
print(df.head(2))
print(f"Columns: {list(df.columns)}\n")

print("DATASETS_METADATA.CSV:")
df = pd.read_csv(DATA_DIR / "datasets_metadata.csv")
print(df.head(2))
print(f"Columns: {list(df.columns)}\n")

print("IT_TICKETS.CSV:")
df = pd.read_csv(DATA_DIR / "it_tickets.csv")
print(df.head(2))
print(f"Columns: {list(df.columns)}")