import pandas as pd
import numpy as np
from pathlib import Path
import logging
from data_loader import DataLoader
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataCleaner:
    def __init__(self, data: dict):
        self.data = data
        self.cleaned_data = {}
        self.report = {}

    def _standardize_columns(self, df):
        df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]
        return df

    def clean_coverage(self):
        df = self.data['coverage'].copy()
        df = self._standardize_columns(df)
        initial_rows = len(df)
        
        # Missing values handling
        missing_code = df['code'].isnull().sum()
        df = df.dropna(subset=['code', 'year', 'antigen'])
        self.report['coverage_missing_key_dropped'] = int(missing_code)
        
        # Coverage percentage validation (0-100)
        df['coverage'] = pd.to_numeric(df['coverage'], errors='coerce')
        invalid_cov = df[(df['coverage'] < 0) | (df['coverage'] > 100)]
        self.report['coverage_invalid_percentage'] = int(len(invalid_cov))
        df.loc[(df['coverage'] < 0) | (df['coverage'] > 100), 'coverage'] = np.nan
        
        df['year'] = df['year'].astype(int)
        
        self.cleaned_data['coverage'] = df
        self.report['coverage_final_rows'] = len(df)

    def clean_incidence(self):
        df = self.data['incidence'].copy()
        df = self._standardize_columns(df)
        df = df.dropna(subset=['code', 'year', 'disease'])
        df['incidence_rate'] = pd.to_numeric(df['incidence_rate'], errors='coerce')
        df.loc[df['incidence_rate'] < 0, 'incidence_rate'] = np.nan
        df['year'] = df['year'].astype(int)
        self.cleaned_data['incidence'] = df

    def clean_cases(self):
        df = self.data['cases'].copy()
        df = self._standardize_columns(df)
        df = df.dropna(subset=['code', 'year', 'disease'])
        df['cases'] = pd.to_numeric(df['cases'], errors='coerce')
        invalid_cases = df[df['cases'] < 0]
        self.report['cases_negative_dropped'] = int(len(invalid_cases))
        df.loc[df['cases'] < 0, 'cases'] = np.nan
        df['year'] = df['year'].astype(int)
        self.cleaned_data['cases'] = df

    def clean_intro(self):
        df = self.data['intro'].copy()
        df = self._standardize_columns(df)
        df = df.dropna(subset=['iso_3_code', 'year'])
        df['year'] = df['year'].astype(int)
        df = df.rename(columns={'iso_3_code': 'code', 'countryname': 'name'})
        self.cleaned_data['intro'] = df

    def clean_schedule(self):
        df = self.data['schedule'].copy()
        df = self._standardize_columns(df)
        df = df.dropna(subset=['iso_3_code', 'year', 'vaccinecode'])
        df['year'] = df['year'].astype(int)
        df = df.rename(columns={'iso_3_code': 'code', 'countryname': 'name'})
        self.cleaned_data['schedule'] = df

    def run_all(self):
        logging.info("Starting cleaning process...")
        if 'coverage' in self.data: self.clean_coverage()
        if 'incidence' in self.data: self.clean_incidence()
        if 'cases' in self.data: self.clean_cases()
        if 'intro' in self.data: self.clean_intro()
        if 'schedule' in self.data: self.clean_schedule()
        
        return self.cleaned_data, self.report

def main():
    loader = DataLoader(data_dir=Path(__file__).parent.parent / "data" / "raw")
    data = loader.load_all()
    
    cleaner = DataCleaner(data)
    cleaned_data, report = cleaner.run_all()
    
    out_dir = Path(__file__).parent.parent / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for name, df in cleaned_data.items():
        df.to_csv(out_dir / f"{name}_cleaned.csv", index=False)
        logging.info(f"Saved {name}_cleaned.csv")
        
    report_dir = Path(__file__).parent.parent / "reports" / "insights"
    with open(report_dir / "cleaning_report.json", "w") as f:
        json.dump(report, f, indent=4)

if __name__ == "__main__":
    main()
