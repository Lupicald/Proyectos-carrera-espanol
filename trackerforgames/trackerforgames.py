# trackerforgames.py
from dotenv import load_dotenv
import os
import requests
import json
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import matplotlib.pyplot as plt

# -----------------------------
# 1️⃣ Cargar variables de entorno
# -----------------------------
load_dotenv(r"C:\Users\USER\Documents\GitHub\Proyectos-carrera-espanol\trackerforgames\.env", override=True)
api = os.getenv("STEAM_API_KEY")
steamid64 = os.getenv("STEAM_ID")
appid = os.getenv("APP_ID")

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

print("API Key:", api)
print("SteamID64:", steamid64)
print("AppID:", appid)

# -----------------------------
# 2️⃣ Preparar URL y parámetros del request
# -----------------------------
url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
params = {
    "key": api,
    "steamid": steamid64,
    "include_appinfo": 1,
    "include_played_free_games": 1,
    "appids_filter[0]": appid
}

# -----------------------------
# 3️⃣ Hacer request con try/except
# -----------------------------
try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print("Error en la request a Steam API:", e)
    data = None

# -----------------------------
# 4️⃣ Guardar respuesta cruda en data/raw/
# -----------------------------
raw_folder = "data/raw/"
os.makedirs(raw_folder, exist_ok=True)
date_str = datetime.datetime.now().strftime("%Y%m%d")
filename = os.path.join(raw_folder, f"raw_{date_str}.json")

if data is not None:
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"JSON guardado correctamente en {filename}")
else:
    print("No se guardó JSON porque la request falló.")

# -----------------------------
# 5️⃣ Procesar datos y calcular horas
# -----------------------------
processed_folder = "data/processed/"
os.makedirs(processed_folder, exist_ok=True)
processed_file = os.path.join(processed_folder, "total.json")

# Cargar histórico si existe
if os.path.exists(processed_file):
    with open(processed_file, "r") as f:
        historial = json.load(f)
else:
    historial = {}

# Inicializar juego si no existe
if appid not in historial:
    historial[appid] = {}

# Buscar info del juego en la API
summary_text = ""
tiempo_total_horas = 0
nombre = ""
if data and "response" in data and "games" in data["response"]:
    for juego in data["response"]["games"]:
        if str(juego.get("appid")) == str(appid):
            nombre = juego.get("name")
            tiempo_total = juego.get("playtime_forever", 0)
            tiempo_total_horas = tiempo_total / 60
            summary_text += f"Juego: {nombre}\nTotal acumulado: {tiempo_total_horas:.2f} horas\n"
            break

# Guardar total de hoy en historial
historial[appid][date_str] = tiempo_total_horas

# Calcular tiempo jugado hoy comparando con fecha anterior
fechas = sorted(historial[appid].keys())
if len(fechas) > 1:
    fecha_anterior = fechas[-2]
    total_ayer = historial[appid][fecha_anterior]
    tiempo_hoy = tiempo_total_horas - total_ayer
else:
    tiempo_hoy = tiempo_total_horas

summary_text += f"Tiempo jugado hoy: {tiempo_hoy:.2f} horas\n"

# Guardar histórico actualizado
with open(processed_file, "w") as f:
    json.dump(historial, f, indent=4)

print("\nResumen diario:")
print(summary_text)

# -----------------------------
# 6️⃣ Generar gráfica semanal
# -----------------------------
hoy = datetime.datetime.now()
start_of_week = hoy - datetime.timedelta(days=hoy.weekday()+1)  # domingo
semana = [(start_of_week + datetime.timedelta(days=i)).strftime("%Y%m%d") for i in range(7)]

horas_semana = [historial[appid].get(dia, 0) for dia in semana]

plt.figure(figsize=(10,5))
plt.bar(range(7), horas_semana, color='skyblue', label='Total acumulado')
plt.plot(range(7), horas_semana, color='orange', marker='o', label='Horas jugadas')
plt.xticks(range(7), [(start_of_week + datetime.timedelta(days=i)).strftime("%a") for i in range(7)])
plt.ylabel("Horas")
plt.title(f"Resumen semanal: {nombre}")
plt.legend()
plt.tight_layout()

# Guardar gráfica para adjuntar al correo
grafica_file = os.path.join(processed_folder, "semana.png")
plt.savefig(grafica_file)
plt.close()

# -----------------------------
# 7️⃣ Enviar correo con resumen y gráfica
# -----------------------------
try:
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = f"Steam Tracker - Resumen diario {date_str}"
    msg.attach(MIMEText(summary_text, 'plain'))

    # Adjuntar imagen
    with open(grafica_file, "rb") as f:
        attach_image = MIMEImage(f.read())
        attach_image.add_header('Content-Disposition', 'attachment', filename="semana.png")
        msg.attach(attach_image)

    # Enviar correo
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
    print("Resumen diario enviado por correo ✅")
except Exception as e:
    print(f"No se pudo enviar el correo ❌: {e}")
