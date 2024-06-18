import psycopg2
import time
from kafka.errors import NoBrokersAvailable
from kafka import KafkaConsumer
import json

print("Waiting for initialization to finish...")

def create_consumer():
    while True:
        try:
            consumer = KafkaConsumer(bootstrap_servers='kafka:9092',
                                     auto_offset_reset='earliest',
                                     enable_auto_commit=True,
                                     group_id='my-group',
                                     value_deserializer=lambda x: json.loads(x.decode('utf-8')))
            consumer.subscribe(['initialization_finished'])
            print("Broker initialized, consumer created")
            return consumer
        except NoBrokersAvailable:
            print("Broker not available, retrying...")
            time.sleep(3)
def consume_messages(consumer):
    # Connect to the database
    conn = psycopg2.connect(database="database", user="database", password="database", host="db", port="5432")
    cur = conn.cursor()

    try:
        for message in consumer:
            print(f"Received message: {message.value}")

            # Execute the query
            cur.execute("SELECT image_path FROM players")

            # Fetch all the rows
            rows = cur.fetchall()

            # Print each row
            for row in rows:
                print(row[0])
            return(rows)
    except KeyboardInterrupt:
        print("Stopped consuming")
    finally:
        # Close the connection
        conn.close()
# Try to connect to your postgres DB
while True:
    try:
        conn = psycopg2.connect("dbname=database user=database password=database host=db port=5432")
        cur = conn.cursor()
        print("Connected to database")
        break
    except psycopg2.OperationalError:
        print("Waiting for database to start...")
        time.sleep(5)

consumer = create_consumer()
rows=consume_messages(consumer)
print([r[0] for r in rows])