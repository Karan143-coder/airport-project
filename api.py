from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from pydantic import BaseModel

app = FastAPI()

engine = create_engine('postgresql://postgres:12345@db:5432/API_project')

class User(BaseModel):
    username: str
    email: str
    phone: str
    address: str

# GET all users
@app.get("/users")
def get_all_users(limit: int = 10, offset: int = 0):
    with engine.connect() as conn:
        query = text("SELECT * FROM users LIMIT :l OFFSET :o")
        result = conn.execute(query, {"l": limit, "o": offset})
        return [dict(row._mapping) for row in result]

# GET single user
@app.get("/users/{user_id}")
def get_user(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
        row = result.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="User not found")
        return dict(row._mapping)

# POST
@app.post("/users")
def create_user(user: User):
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO users (username, email, phone_no, address) VALUES (:u, :e, :p, :a)"),
            {"u": user.username, "e": user.email, "p": user.phone, "a": user.address})
        conn.commit()
    return {"message": "User created successfully"}

# DELETE
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
        conn.commit()
    return {"message": "User deleted successfully"}

# PUT
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    with engine.connect() as conn:
        conn.execute(text("UPDATE users SET username=:u, email=:e, phone_no=:p, address=:a WHERE id=:id"),
            {"u": user.username, "e": user.email, "p": user.phone, "a": user.address, "id": user_id})
        conn.commit()
    return {"message": "User fully updated"}

# PATCH
@app.patch("/users/{user_id}")
def patch_user(user_id: int, phone: str):
    with engine.connect() as conn:
        conn.execute(text("UPDATE users SET phone_no=:p WHERE id=:id"), {"p": phone, "id": user_id})
        conn.commit()
    return {"message": "Phone number partially updated"}