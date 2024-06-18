#!/usr/bin/env python3
import psycopg2
import pandas as pd
from psycopg2 import sql
import time
from kafka.errors import NoBrokersAvailable
from kafka import KafkaProducer
import json


def create_producer():
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers='kafka:9092',
                                     value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            return producer
        except NoBrokersAvailable:
            print("Broker not available, retrying...")
            time.sleep(3)

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
        TARGET_5Yrs INTEGER,
        image_path VARCHAR(255)
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
    players.fillna(0.0, inplace=True)
    # Iterate over DataFrame rows
    for index, row in players.iterrows():
        # Prepare the SQL INSERT query
        query = """
            INSERT INTO players (Name, GP, MIN, PTS, FGM, FGA, FG_Perc, THREE_Made, THREE_A, THREE_Perc, FTM, FTA, FT_Perc, OREB, DREB, REB, AST, STL, BLK, TOV, TARGET_5Yrs, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        name = row[0]
        image_path = '/images/' + str(name) + '.jpg'
        values = list(row) + [name]
        # Execute the SQL INSERT query
        cur.execute(query, values)

    conn.commit()

conn.close()
producer = create_producer()
producer.send('initialization_finished', value='initialize_db.py completed successfully!')
producer.flush()
print("Sent data to Kafka topics")
print("initialize_db.py completed successfully!")