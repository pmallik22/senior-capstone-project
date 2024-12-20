import sqlite3
import pandas as pd

def convert(database, output):
    conn = sqlite3.connect(database) 

    # Read the data from the SQLite database into a pandas DataFrame
    query = "SELECT * FROM reading_requirements" 
    df = pd.read_sql_query(query, conn)

    conn.close()  

    df.to_excel(output, index=False)  # Write the DataFrame to an Excel file
