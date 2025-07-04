from fastapi import FastAPI, Request, HTTPException
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.get("/")
def root():
    return {"message": "Affiliate backend is working!"}

@app.get("/click")
def track_click(subid: str = "", offer_id: int = 0, ip: str = None):
    ip = ip or "unknown"

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO clicks (subid)
            VALUES (%s)
            """,
            (subid)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Database error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    return {"status": "click logged", "subid": subid, "offer_id": offer_id}
