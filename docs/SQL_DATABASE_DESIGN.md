# SQL Database Design

Star Schema:
- **Dimensions**: `dim_country`, `dim_disease`, `dim_vaccine`
- **Facts**: `fact_vaccination_coverage`, `fact_disease_incidence`, `fact_reported_cases`, `fact_vaccine_introduction`, `fact_vaccine_schedule`
- Built on SQLite for reproducibility.