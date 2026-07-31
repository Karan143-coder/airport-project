from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

DB_CONFIG = "dbname=API_project user=postgres password=12345 host=localhost port=5432"

# --- API 1: 
@app.put("/update-flight-slow/{flight_id}")
def update_flight_slow(flight_id: int, new_status: str):
    conn = psycopg2.connect(DB_CONFIG)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        print("[API 1] Transaction started...")
        
        cur.execute("SELECT * FROM public.flights WHERE id = %s FOR UPDATE;", (flight_id,))
        flight = cur.fetchone()
        
        if not flight:
            raise HTTPException(status_code=404, detail="Flight record not found")
        
      
        cur.execute("UPDATE public.flights SET status = %s WHERE id = %s;", (new_status, flight_id))
        print("[API 1] Flight status updated and row locked. Entering sleep state for 10 seconds...")
        
       
        time.sleep(10)
        
        conn.commit()
        print("[API 1] Transaction committed successfully and row lock released.")
        return {"status": "success", "msg": "API 1 successfully completed the transaction"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


# --- API 2: 
@app.put("/update-flight-fast/{flight_id}")
def update_flight_fast(flight_id: int, new_status: str):
    conn = psycopg2.connect(DB_CONFIG)
    cur = conn.cursor()
    try:
        print("[API 2] Attempting instant data modification...")
        start_time = time.time()
        
        
        cur.execute("UPDATE public.flights SET status = %s WHERE id = %s;", (new_status, flight_id))
        
        conn.commit()
        end_time = time.time()
        
        wait_time = round(end_time - start_time, 2)
        print(f"[API 2] Transaction completed. Blocked for {wait_time} seconds before acquiring lock.")
        return {"status": "success", "waited_seconds": wait_time}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()