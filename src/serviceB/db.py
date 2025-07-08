import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv


def init_db():
    """
    Punto de Inicio de la base de datos \n
    Crea la tabla Products(id,name,quantity)
    """
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id serial primary key,
                    name TEXT UNIQUE NOT NULL,
                    quantity int NOT NULL
                );
            """)
            conn.commit()
        conn.close()
        print("Tabla 'products' creada")
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
