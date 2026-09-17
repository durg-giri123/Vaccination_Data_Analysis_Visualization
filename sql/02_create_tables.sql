-- 02_create_tables.sql

-- DIMENSION TABLES

CREATE TABLE IF NOT EXISTS dim_country (
    code VARCHAR(3) PRIMARY KEY,
    name VARCHAR(255),
    group_name VARCHAR(100),
    who_region VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_disease (
    disease_code VARCHAR(50) PRIMARY KEY,
    disease_description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dim_vaccine (
    antigen VARCHAR(50) PRIMARY KEY,
    antigen_description VARCHAR(255)
);

-- FACT TABLES

CREATE TABLE IF NOT EXISTS fact_vaccination_coverage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code VARCHAR(3),
    year INTEGER,
    antigen VARCHAR(50),
    coverage_category VARCHAR(100),
    coverage_category_description VARCHAR(255),
    target_number REAL,
    dodge VARCHAR(50),
    coverage REAL,
    coverage_gap REAL,
    target_achieved BOOLEAN,
    yoy_coverage_change REAL,
    FOREIGN KEY (country_code) REFERENCES dim_country(code),
    FOREIGN KEY (antigen) REFERENCES dim_vaccine(antigen)
);

CREATE TABLE IF NOT EXISTS fact_disease_incidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code VARCHAR(3),
    year INTEGER,
    disease_code VARCHAR(50),
    denominator VARCHAR(255),
    incidence_rate REAL,
    FOREIGN KEY (country_code) REFERENCES dim_country(code),
    FOREIGN KEY (disease_code) REFERENCES dim_disease(disease_code)
);

CREATE TABLE IF NOT EXISTS fact_reported_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code VARCHAR(3),
    year INTEGER,
    disease_code VARCHAR(50),
    cases REAL,
    yoy_cases_change REAL,
    FOREIGN KEY (country_code) REFERENCES dim_country(code),
    FOREIGN KEY (disease_code) REFERENCES dim_disease(disease_code)
);

CREATE TABLE IF NOT EXISTS fact_vaccine_introduction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code VARCHAR(3),
    year INTEGER,
    vaccine_description VARCHAR(255),
    intro_status VARCHAR(50),
    FOREIGN KEY (country_code) REFERENCES dim_country(code)
);

CREATE TABLE IF NOT EXISTS fact_vaccine_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code VARCHAR(3),
    year INTEGER,
    vaccine_code VARCHAR(50),
    schedule_rounds VARCHAR(50),
    target_pop VARCHAR(100),
    target_pop_description VARCHAR(255),
    geoarea VARCHAR(100),
    age_administered VARCHAR(100),
    source_comment TEXT,
    FOREIGN KEY (country_code) REFERENCES dim_country(code),
    FOREIGN KEY (vaccine_code) REFERENCES dim_vaccine(antigen)
);
