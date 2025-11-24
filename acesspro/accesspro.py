import csv
from zk import ZK

# Configuración básica
conn = ZK('192.168.1.201', port=4370)

try:
    conn.connect()
    attendance = conn.get_attendance() # Bajamos los datos

    # Abrimos (o creamos) un archivo CSV
    with open('reporte_asistencia.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # 1. Escribimos los encabezados (Títulos de columna)
        writer.writerow(['ID Usuario', 'Fecha y Hora', 'Tipo de Checada', 'Estado'])
        
        # 2. Recorremos los datos del reloj y escribimos fila por fila
        for att in attendance:
            # att.status suele ser 0=Entrada, 1=Salida, etc.
            writer.writerow([att.user_id, att.timestamp, att.punch, att.status])

    print("¡Archivo CSV generado exitosamente!")

except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.disconnect()