import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv


def init_db():
    """
    Arranca la base de datos 
    crea la tabla users
    """
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id serial primary key,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                );
            """)
            conn.commit()
        conn.close()
        print("Tabla 'users' creada")
    except Exception as e:
        print("Error al crear la tabla:", e)


def get_connection():
    return psycopg2.connect(
        host=getenv("DB_HOST"),
        port=getenv("DB_PORT"),
        database=getenv("DB_NAME"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor
    )
