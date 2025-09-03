from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1️⃣ Cargar variables de entorno
load_dotenv(r"C:\Users\USER\Documents\GitHub\Proyectos-carrera-espanol\trackerforgames\.env", override=True)

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

# 2️⃣ Crear el mensaje
msg = MIMEMultipart()
msg['From'] = EMAIL_FROM
msg['To'] = EMAIL_TO
msg['Subject'] = "Prueba envío log Steam Tracker"
msg.attach(MIMEText("Este es un mensaje de prueba para verificar el envío de correos desde Python.", 'plain'))

# 3️⃣ Enviar el mensaje
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
    print("Correo de prueba enviado correctamente ✅")
except Exception as e:
    print(f"No se pudo enviar el correo de prueba ❌: {e}")
