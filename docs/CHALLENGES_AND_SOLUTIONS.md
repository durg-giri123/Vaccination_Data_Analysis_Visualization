# Challenges and Solutions

**Challenge**: Large Excel files (13MB) slow to process.
**Solution**: Converted to CSV inside `data/processed` and engineered pipeline to read CSVs for EDA and SQL.

**Challenge**: Missing values in cases and negative numbers.
**Solution**: Replaced negative cases with NaN to preserve valid rows while discarding invalid case counts.