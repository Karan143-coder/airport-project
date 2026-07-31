import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from confluent_kafka import Consumer
from email_service import send_email

# Kafka Consumer Setup
conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'flight-status-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['flight_status_events'])

print("Consumer started, waiting for events...", flush=True)

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        if msg.error():
            print(f"Consumer error: {msg.error()}", flush=True)
            continue

        data = json.loads(msg.value().decode('utf-8'))

        print("--- NOTIFICATION RECEIVED ---", flush=True)
        print(f"SMS: Flight {data['flight_number']} status changed to {data['new_status']}", flush=True)
        print("--------------------------------", flush=True)

        
        try:
            conn = psycopg2.connect(
                host="db",
                database="API_project",
                user=os.environ.get("POSTGRES_USER", "postgres"),
                password=os.environ.get("POSTGRES_PASSWORD", "12345")
            )
            
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            
            query = "SELECT full_name, email FROM public.passengers;"
            cur.execute(query)
            
            passengers = cur.fetchall()
            
            cur.close()
            conn.close()
            
        except Exception as db_err:
            print(f"Database Fetch Error: {str(db_err)}", flush=True)
            passengers = [] 
        
        for passenger in passengers:
            send_email(
                receiver_email=passenger["email"],
                passenger_name=passenger["full_name"],
                flight_id=data['flight_number'],
                status=data['new_status']
            )

except KeyboardInterrupt:
    pass
finally:
    consumer.close()