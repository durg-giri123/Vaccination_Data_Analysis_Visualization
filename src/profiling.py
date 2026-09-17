import pandas as pd
from pathlib import Path
import logging
from data_loader import DataLoader
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def profile_data(df: pd.DataFrame, name: str) -> dict:
    profile = {
        'name': name,
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_records': int(df.duplicated().sum())
    }
    
    # Analyze min/max for year if available
    year_cols = [c for c in df.columns if 'year' in c.lower()]
    if year_cols:
        y_col = year_cols[0]
        try:
            profile['year_min'] = int(df[y_col].min())
            profile['year_max'] = int(df[y_col].max())
        except:
            pass
            
    # Count unique countries if available
    country_cols = [c for c in df.columns if 'code' in c.lower() or 'iso' in c.lower()]
    if country_cols:
        c_col = country_cols[0]
        profile['unique_countries'] = int(df[c_col].nunique())
        
    return profile

def main():
    loader = DataLoader(data_dir=Path(__file__).parent.parent / "data" / "raw")
    data = loader.load_all()
    
    profiles = {}
    for name, df in data.items():
        profiles[name] = profile_data(df, name)
        
    out_dir = Path(__file__).parent.parent / "reports" / "insights"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with open(out_dir / "data_inventory.json", "w") as f:
        json.dump(profiles, f, indent=4)
        
    logging.info("Data inventory saved to reports/insights/data_inventory.json")

if __name__ == "__main__":
    main()
