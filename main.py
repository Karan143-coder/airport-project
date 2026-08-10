from fastapi import FastAPI
from routers import users, airport


app = FastAPI(title="Airport Management System")


app.include_router(users.user_router)
app.include_router(airport.airport_router)


@app.get("/")
def root():
    return {"message": "Airport System is Live!"}
