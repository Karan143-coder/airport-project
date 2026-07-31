from fastapi import APIRouter
from pydantic import BaseModel,EmailStr


class PassengerCreate(BaseModel):
    full_name: str
    email: EmailStr
    passport_no: str

class PassengerResponse(BaseModel):
    id: int
    full_name: str
    
    email: EmailStr
    class Config:
        from_attributes = True

class StaffCreate(BaseModel):
    name: str
    role: str
    shift: str

class StaffResponse(BaseModel):
    id: int
    name: str
    role: str
    class Config:
        from_attributes = True
user_router = APIRouter(prefix="/users", tags=["Users"])

# passangers 
@user_router.post("/passengers/")
def create_passenger(item: PassengerCreate):
    return {"message": "Passenger created"}

@user_router.get("/passengers/")
def get_all_passengers():
    return {"message": "List all passengers"}

@user_router.get("/passengers/{id}")
def get_passenger(id: int):
    return {"message": f"Get passenger {id}"}

@user_router.put("/passengers/{id}")
def update_passenger(id: int, item: PassengerCreate):
    return {"message": f"Updated passenger {id}"}

@user_router.patch("/passengers/{id}")
def patch_passenger(id: int):
    return {"message": f"Patched passenger {id}"}

@user_router.delete("/passengers/{id}")
def delete_passenger(id: int):
    return {"message": f"Deleted passenger {id}"}

# staff

@user_router.post("/staff/")
def create_staff(item: StaffCreate):
    return {"message": "Staff created"}

@user_router.get("/staff/")
def get_all_staff():
    return {"message": "List all staff members"}

@user_router.get("/staff/{id}")
def get_staff(id: int):
    return {"message": f"Get staff {id}"}

@user_router.put("/staff/{id}")
def update_staff(id: int, item: StaffCreate):
    return {"message": f"Updated staff {id}"}

@user_router.patch("/staff/{id}")
def patch_staff(id: int):
    return {"message": f"Patched staff {id}"}

@user_router.delete("/staff/{id}")

def delete_staff(id: int):
    return {"message": f"Deleted staff {id}"}