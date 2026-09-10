from utils.db_connection import get_connection
import pandas as pd


conn = get_connection()

query = """
SELECT *
FROM players
"""

df = pd.read_sql_query(query, conn)

print(df)

conn.close()