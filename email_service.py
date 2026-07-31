import smtplib
import os
from email.message import EmailMessage

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")

def send_email(receiver_email, passenger_name, flight_id, status):
    msg = EmailMessage()
    msg['Subject'] = f"Flight Status Update: {flight_id}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email\
    

    try:
       
        with open("routers/email_template.html", "r") as file:
            template_str = file.read()

        
        dynamic_html = template_str.format(
            passenger_name=passenger_name,
            flight_id=flight_id,
            new_status=status
        )

    
        msg.set_content(dynamic_html, subtype='html')

        
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
            print(f"Email sent to {receiver_email}")

    except Exception as e:
        print(f"Error sending email to {receiver_email}: {str(e)}")