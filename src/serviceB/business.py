import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv
from fastapi import HTTPException

connection = psycopg2.connect(
    host=getenv("DB_HOST"),
    port=getenv("DB_PORT"),
    database=getenv("DB_NAME"),
    user=getenv("DB_USER"),
    password=getenv("DB_PASSWORD"),
    cursor_factory=RealDictCursor
)

cursor = connection.cursor()


def get_products() -> list:
    """_summary_

    Raises:
        HTTPException: No hay conexión con la base de datos

    Returns:
        list: la lista de productos
    """
    try:
        cursor.execute(
            "SELECT id,name,quantity FROM products")
        return cursor.fetchall()
    except psycopg2.Error as e:
        print("Error al obtener los productos", e)
        connection.rollback()
        raise HTTPException(
            500, detail='Surgió un error en la base de datos al obtener los productos')


def add_product(name: str, quantity: int):
    """_summary_

    Args:
        name (str): nombre del producto
        quantity (int): cantidad del producto

    Raises:
        HTTPException: ya existe el producto
        HTTPException: problema de conexión con la base de datos
    """
    try:
        cursor.execute(
            "INSERT INTO products(name, quantity) VALUES (%s, %s)",
            (name, quantity)
        )
        connection.commit()

    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        raise HTTPException(
            404, detail='Ya existe un producto con ese nombre')

    except psycopg2.Error as e:
        print("Error al agregar el producto: ", e)
        connection.rollback()
        raise HTTPException(
            500, detail='Surgió un error en la base de datos durante la inserción')


def update_product(id: int, quantity: int):
    """_summary_

    Args:
        id (int): id del producto
        quantity (int): la nueva cantidad del producto

    Raises:
        HTTPException: No existe un producto con ese id
        HTTPException: problema de la conexión con la base de datos
    """
    try:
        cursor.execute(
            "UPDATE products SET quantity = %s WHERE id = %s",
            (quantity, id)
        )
        connection.commit()

        if (cursor.rowcount == 0):
            raise HTTPException(
                404, detail=f'No hay una producto con el id {id}')

    except psycopg2.Error as e:
        connection.rollback()
        print("Error al actualizar el producto:", e)
        raise HTTPException(
            500, detail='Surgió un error en la base de datos durante la actualizacion')
