-- 08_validation_queries.sql

-- 1. Check for negative cases
SELECT * FROM fact_reported_cases WHERE cases < 0;

-- 2. Check for invalid coverage percentages
SELECT * FROM fact_vaccination_coverage WHERE coverage < 0 OR coverage > 100;

-- 3. Check for orphan country codes in fact tables
SELECT DISTINCT country_code FROM fact_vaccination_coverage 
WHERE country_code NOT IN (SELECT code FROM dim_country);
