# Vaccination Data Analysis and Visualization

?? **Live Interactive Dashboard:** [Click here to view the deployed Streamlit Dashboard](https://vaccinationdataanalysisvisualization-covgggq6jasyvtfdk4nsf6.streamlit.app/)

## Project Overview
This project provides a comprehensive end-to-end analysis of global vaccination data to understand trends in coverage, disease incidence, reported cases, and the interrelationships between them.

## Problem Statement
The goal is to analyze global vaccination and disease data to evaluate the impact of vaccination efforts, identify geographic disparities, flag regions needing resource allocation, and support data-driven public health strategy.

## Business Use Cases
- **Public Health Strategy**: Assess the association of vaccination programs with disease reduction.
- **Disease Prevention**: Identify diseases with high incidence despite vaccination.
- **Resource Allocation**: Highlight areas with significant coverage gaps (e.g., target < 95%).
- **Global Health Policy**: Provide evidence to support policies and interventions.

## Dataset
Original datasets include:
1. `coverage-data.xlsx` (399k+ records)
2. `incidence-rate-data.xlsx` (84k+ records)
3. `reported-cases-data.xlsx` (84k+ records)
4. `vaccine-introduction-data.xlsx` (138k+ records)
5. `vaccine-schedule-data.xlsx` (8k+ records)

## Data Architecture
Raw Data (Excel) -> Python Cleaning (Pandas) -> Engineered Features -> Processed CSVs -> SQLite Normalized Database -> Python EDA (Matplotlib/Seaborn) -> Power BI (Mocked via Design Specs).

## Technologies
- **Python**: pandas, numpy, matplotlib, seaborn, sqlalchemy
- **Database**: SQLite (SQL for analytics and DDL)
- **Power BI**: Dashboard design & DAX specifications

## Project Workflow
1. **Data Loading**: Extracted 5 tables from Excel.
2. **Data Cleaning**: Handled missing values, standardized names, removed invalid negative counts, fixed boundaries (e.g., coverage > 100).
3. **Feature Engineering**: Coverage gap to 95%, target achievement flags, YoY changes.
4. **Database Design**: Star schema with `dim_country`, `dim_vaccine`, `dim_disease`, and 5 fact tables.
5. **EDA**: Generated 10+ plots on trends, disparities, drop-offs, and relationships.

## Data Cleaning
- Missing values handled (missing codes, missing years dropped).
- Coverage values > 100 or < 0 nulled out.
- Cases and incidence rates < 0 nulled out.

## EDA
Explored global coverage trends, dose drop-offs (DTP1 vs DTP3), coverage vs incidence scatter plots, and regional distributions. Plots saved in `reports/figures/`.

## Statistical Analysis
Descriptive aggregations and correlation mapping (Coverage vs Incidence). Found inverse relationships between high coverage and lower reported cases for specific diseases.

## SQL Database
See `sql/` for table creations and view definitions. Stored locally in `data/vaccination.db`.

## Power BI
See `docs/POWER_BI_DESIGN.md` for dashboard mapping and KPI definitions. 

## Key Questions
Answered in `docs/BUSINESS_INSIGHTS.md`. Note that demographic questions (gender, education, urban/rural) could not be answered as the datasets lacked these variables.

## Key Insights
1. **Coverage vs Disease**: Higher coverage is associated with lower incidence.
2. **Dose Drop-off**: Noticeable drop-off from 1st to subsequent doses.
3. **Measles Target**: Major gaps still exist in tracking to the 95% threshold.

## Scenario Analysis
Addressed resource allocation by ranking low-coverage regions and evaluating pre/post vaccination introduction effects.

## Recommendations
1. Prioritize resources to countries in the bottom quartile of coverage.
2. Investigate regions with high coverage but high incidence for potential vaccine inefficacy or reporting errors.
3. Implement booster tracking to combat dose drop-off.

## Limitations
- Observational data only (correlation, not definitive causation).
- Missing demographic variables (gender, urban/rural).
- Diverse reporting standards across countries affecting denominator bases for incidence.

## Project Structure
```
vaccination-data-analysis/
├── data/ (raw, processed, exports)
├── docs/ (Markdown documentation)
├── notebooks/ 
├── powerbi/ (Design docs)
├── reports/ (figures, insights)
├── sql/ (DDL and views)
├── src/ (Python pipeline code)
├── run_pipeline.py
└── requirements.txt
```

## Installation & Usage
1. Provide raw data in `data/raw/`.
2. `pip install -r requirements.txt`
3. `python run_pipeline.py`
