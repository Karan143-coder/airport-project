import json
from confluent_kafka import Producer

# Kafka producer setup
producer = Producer({'bootstrap.servers': 'kafka'
':9092'})

def send_flight_status_event(flight_id, flight_number, old_status, new_status):
    event = {
        "flight_id": flight_id,
        "flight_number": flight_number,
        "old_status": old_status,
        "new_status": new_status
    }
    
    print(f"Inside Producer: Sending event for flight {flight_id}", flush=True)
    
    
    producer.produce('flight_status_events', json.dumps(event).encode('utf-8'))
    producer.flush()
    
    print("Kafka Event Published!", flush=True) 