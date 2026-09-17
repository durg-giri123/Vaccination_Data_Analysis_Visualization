import os

docs = {
    "PROJECT_OVERVIEW.md": "# Project Overview\n\nThis project analyzes global vaccination data to understand vaccination coverage, disease incidence, reported cases, and their interrelationships. The pipeline includes data ingestion, cleaning, feature engineering, SQL database modeling, EDA, and Power BI visualization preparation.",
    "DATA_DICTIONARY.md": "# Data Dictionary\n\n## coverage-data\n- `code`: ISO-3 Country Code\n- `name`: Country Name\n- `year`: Year of record\n- `antigen`: Vaccine antigen\n- `coverage`: % coverage\n\n## incidence-rate-data\n- `code`: ISO-3 Country Code\n- `year`: Year\n- `disease`: Disease code\n- `incidence_rate`: Incidence rate based on denominator\n\n## reported-cases-data\n- `cases`: Number of reported cases\n\n## vaccine-introduction-data\n- `intro`: Introduction status\n\n## vaccine-schedule-data\n- `schedulerounds`: Dose count for schedule",
    "DATA_CLEANING.md": "# Data Cleaning\n\n1. Dropped rows missing core keys (`code`, `year`, `disease` / `antigen`).\n2. Standardized all column names to lowercase with underscores.\n3. Imputed `<0` and `>100` percentages in `coverage` as NaN.\n4. Handled negative `cases` and `incidence_rate` values by setting to NaN.\n5. Normalized year to integer.",
    "DATA_VALIDATION.md": "# Data Validation\n\n- Ensure `coverage` is between 0 and 100.\n- Ensure `cases` and `incidence_rate` are non-negative.\n- Ensure referential integrity between fact tables and dimension tables.",
    "EDA_METHODOLOGY.md": "# EDA Methodology\n\n1. Univariate analysis on coverage and incidence.\n2. Trend analysis (year-over-year) globally and by region.\n3. Bivariate analysis (scatter plots) of coverage vs. incidence/cases.\n4. Ranking countries and identifying disparities.",
    "STATISTICAL_ANALYSIS.md": "# Statistical Analysis\n\n- Descriptive Statistics: Mean coverage, total cases, incidence rates.\n- Correlation Analysis: Scatter plots and aggregations show an inverse association between coverage and incidence/cases for specific diseases like Measles.",
    "SQL_DATABASE_DESIGN.md": "# SQL Database Design\n\nStar Schema:\n- **Dimensions**: `dim_country`, `dim_disease`, `dim_vaccine`\n- **Facts**: `fact_vaccination_coverage`, `fact_disease_incidence`, `fact_reported_cases`, `fact_vaccine_introduction`, `fact_vaccine_schedule`\n- Built on SQLite for reproducibility.",
    "SQL_ANALYTICS.md": "# SQL Analytics\n\nAnalytical views created for easy Power BI consumption:\n- Global trend views\n- Regional summary views\n- Vaccine introduction timeline\n- Measles 95% target tracking",
    "POWER_BI_DESIGN.md": "# Power BI Design\n\n## Data Model\nConnected Fact tables to Dimension tables via `country_code`, `disease_code`, and `antigen_code`.\n\n## Dashboards\n1. Global Health Overview\n2. Vaccination Coverage\n3. Disease Burden\n4. Vaccination vs Disease\n5. Vaccine Introduction\n6. Priority Resource Allocation",
    "KPI_DEFINITIONS.md": "# KPI Definitions\n\n- **Overall Vaccination Coverage**: Average of coverage percentages.\n- **Coverage Gap**: `95 - Coverage` (if <= 95).\n- **Target Achieved**: Flag if Coverage >= 95%.\n- **YoY Change**: Current year - Previous year.",
    "BUSINESS_INSIGHTS.md": "# Business Insights\n\n1. **Coverage vs Disease**: Regions with high coverage generally exhibit lower incidence.\n2. **Dose Drop-off**: DTP1 coverage is consistently higher than DTP3, showing retention issues.\n3. **Target 95%**: Many regions still fall short of the 95% target for Measles.",
    "SCENARIO_ANALYSIS.md": "# Scenario Analysis\n\n1. **Resource Allocation**: Dashboard page designed to highlight low-coverage, high-incidence countries.\n2. **Target Tracking**: Specific tracking for Measles (MCV1/MCV2) 95% goal.",
    "LIMITATIONS.md": "# Limitations\n\n- **Observational Data**: Cannot definitively prove causality.\n- **Missing Variables**: No demographic, urban/rural, or socio-economic data available in raw files (unanswerable questions documented).\n- **Reporting Quality**: Different countries have different denominators and reporting standards.",
    "CHALLENGES_AND_SOLUTIONS.md": "# Challenges and Solutions\n\n**Challenge**: Large Excel files (13MB) slow to process.\n**Solution**: Converted to CSV inside `data/processed` and engineered pipeline to read CSVs for EDA and SQL.\n\n**Challenge**: Missing values in cases and negative numbers.\n**Solution**: Replaced negative cases with NaN to preserve valid rows while discarding invalid case counts.",
    "REPRODUCIBILITY.md": "# Reproducibility\n\n1. Place raw Excel files in `data/raw/`.\n2. Create venv: `python -m venv venv` and `pip install -r requirements.txt`.\n3. Run pipeline: `python run_pipeline.py` to generate SQLite DB, processed CSVs, and plots."
}

for name, content in docs.items():
    path = f"docs/{name}"
    with open(path, "w") as f:
        f.write(content)
        
print("Docs generated.")
