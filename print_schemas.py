import pandas as pd
from data_loader import DataLoader
from pathlib import Path

loader = DataLoader(data_dir=Path("data/raw"))
data = loader.load_all()

for name, df in data.items():
    print(f"--- {name.upper()} ---")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Shape: {df.shape}")
    print()
