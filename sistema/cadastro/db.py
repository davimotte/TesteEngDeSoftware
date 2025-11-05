import os
import psycopg

def get_conn():
    """
    Conexão simples (uma por requisição).
    Se quiser performance maior, depois troque para psycopg_pool.
    """
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db   = os.getenv("POSTGRES_DB",   "app")
    user = os.getenv("POSTGRES_USER", "postgres")
    pwd  = os.getenv("POSTGRES_PASSWORD", "postgres")

    dsn = f"host={host} port={port} dbname={db} user={user} password={pwd}"
    return psycopg.connect(dsn, autocommit=True)
