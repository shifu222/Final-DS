from fastapi import FastAPI
from pydantic import BaseModel
from business import get_products, add_product, update_product
from contextlib import asynccontextmanager
import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(lifespan=lifespan)


class Product(BaseModel):
    name: str
    quantity: int


@app.get("/products")
def get_products_endoint():
    """
    Endpoint para listar productos
    """
    return get_products()


@app.post("/products")
def new_product_endpoint(product: Product):
    """
    Endpoint para aregar productos
    """
    add_product(name=product.name, quantity=product.quantity)
    return {"message": "Producto creado"}


@app.put("/products/{product_id}")
def update_task_endpoint(product_id: int, product: Product):
    """
    Endpoint para actualizar un producto 
    """
    update_product(id=product_id, quantity=product.quantity)
    return {"message": "Producto actualizada"}
