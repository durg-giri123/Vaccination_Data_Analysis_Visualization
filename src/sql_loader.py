import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_to_sql():
    db_path = Path(__file__).parent.parent / "data" / "vaccination.db"
    engine = create_engine(f"sqlite:///{db_path}")
    
    exports_dir = Path(__file__).parent.parent / "data" / "exports"
    
    # Load engineered coverage
    if (exports_dir / "coverage_engineered.csv").exists():
        df_cov = pd.read_csv(exports_dir / "coverage_engineered.csv")
        df_cov.to_sql('fact_vaccination_coverage', engine, if_exists='replace', index=False)
        logging.info("Loaded fact_vaccination_coverage")
        
        # Dimension table: dim_country
        dim_country = df_cov[['code', 'name', 'group']].drop_duplicates().dropna(subset=['code'])
        dim_country = dim_country.rename(columns={'group': 'group_name'})
        dim_country.to_sql('dim_country', engine, if_exists='replace', index=False)
        logging.info("Loaded dim_country")
        
        # Dimension table: dim_vaccine
        dim_vaccine = df_cov[['antigen', 'antigen_description']].drop_duplicates().dropna(subset=['antigen'])
        dim_vaccine.to_sql('dim_vaccine', engine, if_exists='replace', index=False)
        logging.info("Loaded dim_vaccine")
        
    # Load engineered cases
    if (exports_dir / "cases_engineered.csv").exists():
        df_cases = pd.read_csv(exports_dir / "cases_engineered.csv")
        df_cases.to_sql('fact_reported_cases', engine, if_exists='replace', index=False)
        logging.info("Loaded fact_reported_cases")
        
        # Dimension table: dim_disease
        dim_disease = df_cases[['disease', 'disease_description']].drop_duplicates().dropna(subset=['disease'])
        dim_disease = dim_disease.rename(columns={'disease': 'disease_code'})
        dim_disease.to_sql('dim_disease', engine, if_exists='replace', index=False)
        logging.info("Loaded dim_disease")
        
    # Load incidence
    if (exports_dir / "incidence_engineered.csv").exists():
        df_inc = pd.read_csv(exports_dir / "incidence_engineered.csv")
        df_inc.to_sql('fact_disease_incidence', engine, if_exists='replace', index=False)
        logging.info("Loaded fact_disease_incidence")

    # Load intro
    if (exports_dir / "intro_engineered.csv").exists():
        df_intro = pd.read_csv(exports_dir / "intro_engineered.csv")
        df_intro.to_sql('fact_vaccine_introduction', engine, if_exists='replace', index=False)
        logging.info("Loaded fact_vaccine_introduction")

    # Load schedule
    if (exports_dir / "schedule_engineered.csv").exists():
        df_sched = pd.read_csv(exports_dir / "schedule_engineered.csv")
        df_sched.to_sql('fact_vaccine_schedule', engine, if_exists='replace', index=False)
        logging.info("Loaded fact_vaccine_schedule")

if __name__ == "__main__":
    load_to_sql()
