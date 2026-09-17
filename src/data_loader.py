import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLoader:
    def __init__(self, data_dir: str = "../data/raw"):
        self.data_dir = Path(data_dir)
        self.datasets = {
            'coverage': 'coverage-data.xlsx',
            'incidence': 'incidence-rate-data.xlsx',
            'cases': 'reported-cases-data.xlsx',
            'intro': 'vaccine-introduction-data.xlsx',
            'schedule': 'vaccine-schedule-data.xlsx'
        }
        self.data = {}

    def load_all(self):
        for name, filename in self.datasets.items():
            filepath = self.data_dir / filename
            if filepath.exists():
                logging.info(f"Loading {filename}...")
                self.data[name] = pd.read_excel(filepath)
                logging.info(f"Loaded {name} with shape {self.data[name].shape}")
            else:
                logging.error(f"File not found: {filepath}")
        return self.data
