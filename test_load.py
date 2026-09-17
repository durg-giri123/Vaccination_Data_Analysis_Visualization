import pandas as pd
import sys

print("Loading vaccine-schedule-data.xlsx...")
df = pd.read_excel("data/raw/vaccine-schedule-data.xlsx", engine="openpyxl")
print(f"Loaded. Shape: {df.shape}")
print(df.head())
