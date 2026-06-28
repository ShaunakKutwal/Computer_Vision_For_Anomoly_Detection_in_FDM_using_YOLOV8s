import smtplib
from email.message import EmailMessage
import os
import threading
from dotenv import load_dotenv

# Load .env explicitly from root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

def _send_email_worker(defect_name, confidence, image_path):
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("APP_PASSWORD")
    receiver = os.getenv("RECEIVER_EMAIL")

    if not sender or not password:
        print(f"❌ ERROR: Credentials missing! Sender: {sender}")
        return

    try:
        msg = EmailMessage()
        msg['Subject'] = f"ALERT: {defect_name.upper()}"
        msg['From'] = sender
        msg['To'] = receiver
        msg.set_content(f"Defect: {defect_name} ({confidence:.2%})")

        with open(image_path, 'rb') as f:
            msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=os.path.basename(image_path))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("📧 SUCCESS: Email Sent!")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def trigger_email_alert(defect, conf, path):
    threading.Thread(target=_send_email_worker, args=(defect, conf, path)).start()