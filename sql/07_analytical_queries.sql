-- 07_analytical_queries.sql

-- 1. Countries below the 95% target in the most recent year
SELECT c.name, v.antigen_description, f.coverage
FROM fact_vaccination_coverage f
JOIN dim_country c ON f.country_code = c.code
JOIN dim_vaccine v ON f.antigen = v.antigen
WHERE f.year = 2023 AND f.coverage < 95
ORDER BY f.coverage ASC;

-- 2. Dose drop-off (DTP1 vs DTP3) per country
SELECT 
    d1.country_code,
    d1.year,
    d1.coverage as dtp1_coverage,
    d3.coverage as dtp3_coverage,
    (d1.coverage - d3.coverage) as dose_dropoff
FROM fact_vaccination_coverage d1
JOIN fact_vaccination_coverage d3 
  ON d1.country_code = d3.country_code 
  AND d1.year = d3.year
WHERE d1.antigen = 'DTP1' AND d3.antigen = 'DTP3';

-- 3. High-coverage/high-incidence flag (using views)
SELECT 
    db.country_name,
    db.disease_description,
    db.total_cases,
    c.coverage
FROM v_disease_burden db
JOIN fact_vaccination_coverage c ON db.country_name = c.country_code AND db.year = c.year
WHERE c.coverage > 95 AND db.avg_incidence_rate > 10;
