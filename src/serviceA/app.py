from fastapi import FastAPI
from pydantic import BaseModel
from business import get_users, add_user, remove_user
from contextlib import asynccontextmanager
import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(lifespan=lifespan)


class User(BaseModel):
    username: str
    email: str
    password: str


@app.get("/users")
def get_users_endoint():
    """
    Endpoint para listar los usuarios
    """
    return get_users()


@app.post("/users")
def new_user_endpoint(user: User):
    """
    Endpoint agregar usuarios
    """
    add_user(username=user.username, password=user.password, email=user.email)
    return {"message": "usuario creado"}


@app.delete("/users/{user_id}")
def remove_user_endpoint(user_id: int):
    """
    Endpoint para eliminar usuarios usando el id
    """
    remove_user(user_id=user_id)
    return {"message": "usuario eliminado"}
