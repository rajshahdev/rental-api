from fastapi import FastAPI
from . import models
from .database import engine
from . import user, inventory, rent, employee, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="rental-api",
    version="0.0.1",
    contact={
        "name": "Raj Shah",
        "email": "be.rajshah@gmail.com",
    },
)
app.include_router(user.router)
app.include_router(inventory.router)
app.include_router(rent.router)
app.include_router(employee.router)
app.include_router(auth.router)
