import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FeatureEngineer:
    def __init__(self, data_dir: str = "../data/processed"):
        self.data_dir = Path(data_dir)
        self.data = {}
        
    def load_cleaned_data(self):
        for file in self.data_dir.glob("*_cleaned.csv"):
            name = file.stem.replace('_cleaned', '')
            self.data[name] = pd.read_csv(file)
            
    def engineer_coverage_features(self):
        if 'coverage' not in self.data: return
        df = self.data['coverage'].copy()
        
        # Coverage Gap to 95%
        df['coverage_gap'] = df['coverage'].apply(lambda x: 95 - x if pd.notnull(x) and x <= 95 else (0 if pd.notnull(x) else np.nan))
        df['target_achieved'] = (df['coverage'] >= 95).astype(int)
        
        # YoY Coverage Change
        df = df.sort_values(by=['code', 'antigen', 'year'])
        df['yoy_coverage_change'] = df.groupby(['code', 'antigen'])['coverage'].diff()
        
        self.data['coverage_engineered'] = df
        
    def engineer_cases_features(self):
        if 'cases' not in self.data: return
        df = self.data['cases'].copy()
        
        df = df.sort_values(by=['code', 'disease', 'year'])
        df['yoy_cases_change'] = df.groupby(['code', 'disease'])['cases'].diff()
        
        self.data['cases_engineered'] = df
        
    def engineer_incidence_features(self):
        if 'incidence' not in self.data: return
        df = self.data['incidence'].copy()
        
        df = df.sort_values(by=['code', 'disease', 'year'])
        df['yoy_incidence_change'] = df.groupby(['code', 'disease'])['incidence_rate'].diff()
        
        self.data['incidence_engineered'] = df

    def run_all(self):
        self.load_cleaned_data()
        self.engineer_coverage_features()
        self.engineer_cases_features()
        self.engineer_incidence_features()
        
        out_dir = Path(__file__).parent.parent / "data" / "exports"
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # Save engineered
        for name, df in self.data.items():
            if 'engineered' in name:
                df.to_csv(out_dir / f"{name}.csv", index=False)
                logging.info(f"Saved {name}.csv")
        
        # Also save intro and schedule directly to exports as they don't have row-level engineered features
        if 'intro' in self.data:
            self.data['intro'].to_csv(out_dir / "intro_engineered.csv", index=False)
        if 'schedule' in self.data:
            self.data['schedule'].to_csv(out_dir / "schedule_engineered.csv", index=False)

def main():
    engineer = FeatureEngineer(data_dir=Path(__file__).parent.parent / "data" / "processed")
    engineer.run_all()

if __name__ == "__main__":
    main()
