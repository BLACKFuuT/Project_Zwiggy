from app.core.celery_app import celery_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

@celery_app.task
def send_order_email(customer_email: str, order_id: int, total_amount: float):

    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_PASSWORD

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = customer_email
    message["Subject"] = "Order Confirmation - Zwiggy"

    body = f"""
    Your order has been successfully placed.

    Order ID: {order_id}
    Total Amount: {total_amount}

    Thank you for ordering with Zwiggy!
    """

    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender_email, sender_password)

    server.sendmail(sender_email, customer_email, message.as_string())

    server.quit()