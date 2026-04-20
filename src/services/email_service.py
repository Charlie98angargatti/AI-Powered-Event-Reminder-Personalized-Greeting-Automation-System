import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
# Load environment variables from .env file
load_dotenv()

# Fetch sender email and app password from environment
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# print("DEBUG EMAIL:", SENDER_EMAIL)
# print("DEBUG PASS:", APP_PASSWORD)

if not SENDER_EMAIL or not APP_PASSWORD:
    raise ValueError("SENDER_EMAIL and APP_PASSWORD must be set in .env file.")

def send_email(to_email: str, message: str):
    """
    Send an email with the given message to the specified recipient.
    """
    try:
        msg = MIMEText(message)
        msg["Subject"] = "Special Wishes 🎉"
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()

        print(f"✅ Email sent to: {to_email}")

    except smtplib.SMTPAuthenticationError:
        print(f"❌ Authentication failed. Check your SENDER_EMAIL and APP_PASSWORD.")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

