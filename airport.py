from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import json
from confluent_kafka import Producer
from .producer import send_flight_status_event

# Kafka Producer setup
producer = Producer({'bootstrap.servers': 'kafka:9092'})

class FlightCreate(BaseModel):
    flight_no: str
    origin: str
    destination: str
    departure_time: str
    gate_no: str

class FlightResponse(FlightCreate):
    id: int
    class Config:
        from_attributes = True

class BaggageCreate(BaseModel):
    pass_id: int
    weight_kg: float
    status: str

class BaggageResponse(BaggageCreate):
    id: int
    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status: str
    flight_number: str
    old_status: str


airport_router = APIRouter(prefix="/airport", tags=["Airport"])

# flights
@airport_router.post("/flights/")
def create_flight(item: FlightCreate):
    return {"message": "Flight created"}

@airport_router.get("/flights/")
def get_all_flights():
    return {"message": "List all flights"}

@airport_router.get("/flights/{id}")
def get_flight(id: int):
    return {"message": f"Get flight {id}"}

@airport_router.put("/flights/{id}")
def update_flight(id: int, item: FlightCreate):
    return {"message": f"Updated flight {id}"}

@airport_router.patch("/flights/{id}")
def patch_flight(id: int, item: StatusUpdate):
    old_status = "On-Time"  
    new_status = item.status
    
    
    send_flight_status_event(id, "AI101", old_status, new_status)
    
    
    return {
        "message": "Flight status updated successfully",
        "details": {
            "flight_id": id,
            "flight_number": "AI101",
            "previous_status": old_status,
            "updated_status": new_status,
            "event_status": "Published to Kafka"
        }
    }
@airport_router.delete("/flights/{id}")
def delete_flight(id: int):
    return {"message": f"Deleted flight {id}"}

# baggage
@airport_router.post("/baggage/")
def create_baggage(item: BaggageCreate):
    return {"message": "Baggage checked-in successfully"}

@airport_router.get("/baggage/")
def get_all_baggage():
    return {"message": "List of all baggage records"}

@airport_router.get("/baggage/{id}")
def get_baggage(id: int):
    return {"message": f"Details of baggage {id}"}

@airport_router.put("/baggage/{id}")
def update_baggage(id: int, item: BaggageCreate):
    return {"message": f"Updated full details for baggage {id}"}

@airport_router.patch("/baggage/{id}")
def patch_baggage(id: int):
    return {"message": f"Updated status for baggage {id}"}

@airport_router.delete("/baggage/{id}")
def delete_baggage(id: int):
    return {"message": f"Baggage record {id} deleted"}