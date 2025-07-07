import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from os import getenv
from fastapi import HTTPException

load_dotenv()

connection = psycopg2.connect(
    host=getenv("DB_HOST"),
    port=getenv("DB_PORT"),
    database=getenv("DB_NAME"),
    user=getenv("DB_USER"),
    password=getenv("DB_PASSWORD"),
    cursor_factory=RealDictCursor
)

cursor = connection.cursor()


def get_users() -> list:
    """
    Retorna la lista de usuarios de la tabla users
    """
    try:
        cursor.execute(
            "SELECT id,username,email FROM users")
        return cursor.fetchall()
    except psycopg2.Error as e:
        print("Error al obtener los usuarios", e)
        connection.rollback()
        raise HTTPException(
            500, detail='Surgió un error en la base de datos al obtener los usuarios')


def add_user(username: str, email: str, password: str):
    """
    Agrega un nuevo usuario a la tabla users
    """
    try:
        cursor.execute(
            "INSERT INTO users(username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        connection.commit()

    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        raise HTTPException(
            404, detail='Ya existe una usuario con ese nombre y email')

    except psycopg2.Error as e:
        print("Error al agregar el usuario: ", e)
        connection.rollback()
        raise HTTPException(
            500, detail='Surgió un error en la base de datos durante la inserción')


def remove_user(user_id: int):
    """
    Elimina un usuario de la tabla users
    """
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()

        if (cursor.rowcount == 0):
            raise HTTPException(
                404, detail=f'No existe una tarea con el id {user_id}')
    except psycopg2.Error as e:
        print("Error al eliminar la tarea : ", e)
        connection.rollback()
        raise HTTPException(
            500, detail='Surgió un error en la base de datos durante la eliminación')
