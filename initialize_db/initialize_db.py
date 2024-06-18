#!/usr/bin/env python3
import psycopg2
import pandas as pd
from psycopg2 import sql
import time

# Try to connect to your postgres DB
while True:
    try:
        conn = psycopg2.connect("dbname=database user=database password=database host=db port=5432")
        cur = conn.cursor()
        break
    except psycopg2.OperationalError:
        print("Waiting for database to start...")
        time.sleep(5)


# Connect to your postgres DB
conn = psycopg2.connect("dbname=database user=database password=database host=db port=5432")
cur = conn.cursor()

# Create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        Name VARCHAR(255) UNIQUE NOT NULL PRIMARY KEY,
        GP INTEGER,
        MIN REAL,
        PTS REAL,
        FGM REAL,
        FGA REAL,
        FG_Perc REAL,
        THREE_Made REAL,
        THREE_A REAL,
        THREE_Perc REAL,
        FTM REAL,
        FTA REAL,
        FT_Perc REAL,
        OREB REAL,
        DREB REAL,
        REB REAL,
        AST REAL,
        STL REAL,
        BLK REAL,
        TOV REAL,
        TARGET_5Yrs INTEGER
    )
""")

conn.commit()


# Check if the table is empty
cur.execute("SELECT COUNT(*) FROM players")
count = cur.fetchone()[0]

if count == 0:
    # Read the CSV file
    players = pd.read_csv('nba.csv')
    players.columns = ['Name', 'GP', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_Perc', 'THREE_Made', 'THREE_A', 'THREE_Perc', 'FTM', 'FTA', 'FT_Perc', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'TARGET_5Yrs']
    players = players.drop_duplicates(subset='Name', keep='first')
    # Iterate over DataFrame rows
    for index, row in players.iterrows():
        # Prepare the SQL INSERT query
        query = """
            INSERT INTO players (Name, GP, MIN, PTS, FGM, FGA, FG_Perc, THREE_Made, THREE_A, THREE_Perc, FTM, FTA, FT_Perc, OREB, DREB, REB, AST, STL, BLK, TOV, TARGET_5Yrs)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Execute the SQL INSERT query
        cur.execute(query, tuple(row))

    conn.commit()

conn.close()
print("initialize_db.py completed successfully!")