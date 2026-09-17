# Data Cleaning

1. Dropped rows missing core keys (`code`, `year`, `disease` / `antigen`).
2. Standardized all column names to lowercase with underscores.
3. Imputed `<0` and `>100` percentages in `coverage` as NaN.
4. Handled negative `cases` and `incidence_rate` values by setting to NaN.
5. Normalized year to integer.