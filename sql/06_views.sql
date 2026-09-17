-- 06_views.sql

CREATE VIEW IF NOT EXISTS v_global_coverage_summary AS
SELECT 
    year, 
    AVG(coverage) as avg_coverage, 
    AVG(coverage_gap) as avg_coverage_gap, 
    SUM(target_achieved) as target_met_count,
    COUNT(DISTINCT country_code) as countries_reported
FROM fact_vaccination_coverage
GROUP BY year;

CREATE VIEW IF NOT EXISTS v_regional_coverage AS
SELECT 
    c.who_region, 
    f.year, 
    AVG(f.coverage) as avg_coverage
FROM fact_vaccination_coverage f
JOIN dim_country c ON f.country_code = c.code
GROUP BY c.who_region, f.year;

CREATE VIEW IF NOT EXISTS v_disease_burden AS
SELECT 
    c.name as country_name,
    f.year, 
    d.disease_description, 
    SUM(f.cases) as total_cases,
    AVG(i.incidence_rate) as avg_incidence_rate
FROM fact_reported_cases f
JOIN dim_country c ON f.country_code = c.code
JOIN dim_disease d ON f.disease_code = d.disease_code
LEFT JOIN fact_disease_incidence i ON f.country_code = i.country_code AND f.year = i.year AND f.disease_code = i.disease_code
GROUP BY c.name, f.year, d.disease_description;

CREATE VIEW IF NOT EXISTS v_measles_target_progress AS
SELECT 
    c.name as country_name, 
    f.year, 
    v.antigen_description,
    f.coverage,
    f.coverage_gap,
    f.target_achieved
FROM fact_vaccination_coverage f
JOIN dim_country c ON f.country_code = c.code
JOIN dim_vaccine v ON f.antigen = v.antigen
WHERE v.antigen_description LIKE '%measles%';
