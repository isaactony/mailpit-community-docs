import os
import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["From"] = "App <noreply@example.com>"
msg["To"] = "ada@example.com"
msg["Subject"] = "Welcome to the app"
msg.set_content("Thanks for signing up.")
msg.add_alternative("<p>Thanks for signing up.</p>", subtype="html")

host = os.environ.get("SMTP_HOST", "localhost")
port = int(os.environ.get("SMTP_PORT", "1025"))

# Mailpit accepts plain SMTP with no login by default.
with smtplib.SMTP(host, port) as smtp:
    smtp.send_message(msg)
print("Sent")
