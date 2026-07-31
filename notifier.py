
import psycopg2
import smtplib
from email.message import EmailMessage

def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="airport_db",
        user="postgres",
        password="12345"
    )

def send_notification(flight_id, flight_no, status):
   
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT email FROM passengers WHERE flight_id = %s", (flight_id,))
    passengers = cur.fetchall()
    cur.close()
    conn.close()

    
    for p in passengers:
        email = p[0]
        
        print(f"Email sent to {email} for flight {flight_no}")