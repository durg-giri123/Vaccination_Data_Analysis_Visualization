import sqlite3
import pandas as pd

conn = sqlite3.connect('data/vaccination.db')

for table in ['fact_vaccination_coverage', 'fact_vaccine_schedule', 'fact_vaccine_introduction']:
    df = pd.read_sql(f'SELECT * FROM {table}', conn)
    # Convert empty strings or whitespace to None (NULL)
    df = df.replace(r'^\s*$', None, regex=True)
    
    # Save it back, replacing the table
    df.to_sql(table, conn, if_exists='replace', index=False)
    print(f'Cleaned {table}')

conn.close()
