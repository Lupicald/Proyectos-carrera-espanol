"""
Sistema de Registro de Ventas v2.0
Proyecto Final - Programación Avanzada en Python

Este programa funciona como un punto de venta simple, permitiendo registrar
ventas, crear reportes mensuales y visualizar los ingresos.
"""
# --- Importación de Módulos Necesarios ---
import time
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple, List, Optional

# Se intenta importar 'msvcrt' para una mejor experiencia en Windows
try:
    import msvcrt
    IS_WINDOWS = True
except ImportError:
    IS_WINDOWS = False

# --- Configuración Inicial ---
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "sistema_ventas.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


# --- Definición de Clases ---

class Usuario:
    """Representa al vendedor/cajero que usa el sistema."""
    def __init__(self, nickname: str) -> None:
        self.nickname = nickname.strip()

    def saludo(self) -> str:
        return f"¡Hola, {self.nickname}! Bienvenido/a al sistema de ventas."

class Venta:
    """Representa una única transacción de venta."""
    def __init__(self, producto: str, cantidad: float, precio: float, usuario: Usuario) -> None:
        self.producto = producto
        self.cantidad = cantidad
        self.precio_unitario = precio
        self.usuario = usuario

    @property
    def subtotal(self) -> float:
        """Calcula el subtotal de la venta."""
        return self.cantidad * self.precio_unitario
    
    def to_linea_reporte(self) -> str:
        """Formatea la venta como una línea para el archivo de reporte."""
        return (f"{self.usuario.nickname},{self.producto},{self.cantidad},"
                f"{self.precio_unitario:.2f},{self.subtotal:.2f}")

class GestorArchivos:
    """Gestiona los archivos de reporte de ventas y archivos generales."""
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self._crear_archivos_iniciales()

    def _crear_archivos_iniciales(self) -> None:
        """Crea 4 archivos iniciales si no existen."""
        archivos_base = [
            "inventario.txt",
            "proveedores.txt", 
            "clientes.txt",
            "configuracion.txt"
        ]
        for archivo in archivos_base:
            path = self.base_dir / archivo
            if not path.exists():
                path.write_text("# Archivo creado automáticamente\n", encoding="utf-8")

    def listar_todos_archivos(self) -> List[str]:
        """Lista todos los archivos .txt disponibles."""
        return [p.name for p in self.base_dir.glob("*.txt")]

    def crear_archivo_personalizado(self, nombre: str, contenido_inicial: str = "") -> Path:
        """Crea un nuevo archivo personalizado."""
        if not nombre.endswith('.txt'):
            nombre += '.txt'
        
        path_archivo = self.base_dir / nombre
        if path_archivo.exists():
            raise FileExistsError(f"ERROR: El archivo '{nombre}' ya existe.")
        
        path_archivo.write_text(contenido_inicial or "# Archivo nuevo\n", encoding="utf-8")
        logging.info(f"Archivo personalizado creado: {nombre}")
        return path_archivo

    def leer_archivo_general(self, nombre_archivo: str) -> str:
        """Lee cualquier archivo de texto."""
        path_archivo = self.base_dir / nombre_archivo
        if not path_archivo.exists():
            raise FileNotFoundError(f"ERROR: El archivo '{nombre_archivo}' no existe.")
        
        return path_archivo.read_text(encoding="utf-8")

    def escribir_archivo_general(self, nombre_archivo: str, contenido: str, modo: str = "w") -> None:
        """Escribe contenido en un archivo."""
        path_archivo = self.base_dir / nombre_archivo
        if not path_archivo.exists() and modo == "a":
            raise FileNotFoundError(f"ERROR: El archivo '{nombre_archivo}' no existe.")
        
        with path_archivo.open(modo, encoding="utf-8") as f:
            f.write(contenido)
        
        logging.info(f"Contenido {'agregado' if modo == 'a' else 'escrito'} en: {nombre_archivo}")

    def listar_reportes(self) -> List[str]:
        return [p.name for p in self.base_dir.glob("ventas_*.txt")]

    def crear_reporte_mensual(self, anio: int, mes: int) -> Path:
        nombre_reporte = f"ventas_{anio:04d}-{mes:02d}.txt"
        path_reporte = self.base_dir / nombre_reporte
        
        if path_reporte.exists():
            raise FileExistsError(f"ERROR: El reporte '{nombre_reporte}' ya existe.")
        
        path_reporte.touch()
        logging.info(f"Reporte mensual creado: {path_reporte.name}")
        return path_reporte

    def registrar_venta(self, nombre_reporte: str, venta: Venta, fecha: Tuple[int, int, int]) -> None:
        path_reporte = self.base_dir / nombre_reporte
        if not path_reporte.exists():
            raise FileNotFoundError(f"ERROR: El reporte '{nombre_reporte}' no existe.")
        
        dia, mes, anio = fecha
        timestamp = f"[{anio:04d}-{mes:02d}-{dia:02d}]: "
        
        with path_reporte.open("a", encoding="utf-8") as f:
            f.write(timestamp + venta.to_linea_reporte() + "\n")
            
        logging.info(f"Venta registrada en: {path_reporte.name}")

    def leer_reporte(self, nombre_reporte: str) -> Tuple[str, float]:
        path_reporte = self.base_dir / nombre_reporte
        if not path_reporte.exists():
            raise FileNotFoundError(f"ERROR: El reporte '{nombre_reporte}' no existe.")
            
        contenido = path_reporte.read_text(encoding="utf-8")
        total_ventas = 0.0
        for i, linea in enumerate(contenido.splitlines()):
            try:
                if "]: " not in linea:
                    continue
                partes = linea.split("]: ")[1]
                subtotal_str = partes.split(',')[-1]
                total_ventas += float(subtotal_str)
            except (IndexError, ValueError):
                logging.warning(f"Línea {i+1} mal formada en '{nombre_reporte}': '{linea}'")
                continue
        
        logging.info(f"Reporte leído: {path_reporte.name}")
        return contenido, total_ventas

class App:
    """Clase principal que controla el flujo de la aplicación de ventas."""
    def __init__(self) -> None:
        self.usuario: Optional[Usuario] = None
        self.gestor = GestorArchivos(DATA_DIR)
        self._sembrar_reportes_iniciales()

    # --- Métodos de Interfaz de Usuario (UI) ---
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola para una mejor legibilidad."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def pedir_usuario(self) -> None:
        """Solicita el nombre de usuario y crea el objeto correspondiente."""
        while not self.usuario:
            nick = input("Por favor, introduce tu nombre de vendedor: ").strip()
            if nick:
                self.usuario = Usuario(nick)
                print(self.usuario.saludo())
                logging.info(f"Vendedor activo: {self.usuario.nickname}")
            else:
                print("El nombre no puede estar vacío.")
    
    def carga(self, max_seg: int = 3) -> None:
        """Muestra un mensaje de carga simulado."""
        print("Iniciando sistema de punto de venta", end="", flush=True)
        for _ in range(max_seg):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print("\n¡Sistema listo!")

    def pedir_fecha(self) -> Tuple[int, int, int]:
        """Solicita una fecha y la valida."""
        while True:
            s = input("-> Ingresa la fecha de la transacción (dd/mm/aaaa): ").strip()
            try:
                dt = datetime.strptime(s, "%d/%m/%Y")
                return (dt.day, dt.month, dt.year)
            except ValueError:
                print("ERROR: Formato inválido. Ejemplo: 25/12/2023.")

    def mostrar_menu(self) -> None:
        """Muestra el menú principal de opciones."""
        print("\n" + "="*45)
        print(" " * 12 + "MENÚ PUNTO DE VENTA")
        print("="*45)
        print("[1] Registrar Nueva Venta | [2] Ver Reporte de Ventas")
        print("[3] Crear Reporte Mensual | [4] Gestionar Archivos")
        print("[5] Cambiar de Vendedor | [6] Salir del Sistema")
        print("="*45)

    def input_con_timeout(self, segundos: int) -> str:
        """Espera la entrada del usuario con un tiempo límite."""
        print(f"Selecciona una opción (tienes {segundos // 60} minutos): ", end="", flush=True)
        inicio = time.monotonic()
        if IS_WINDOWS:
            buffer = ""
            for _ in range(segundos):
                time.sleep(1)
                if msvcrt.kbhit():
                    char = msvcrt.getwch()
                    if char == '\r': print(); return buffer.strip()
                    elif char == '\b':
                        if buffer: buffer = buffer[:-1]; print('\b \b', end='', flush=True)
                    else: buffer += char; print(char, end='', flush=True)
        else:
            opcion = input()
            if (time.monotonic() - inicio) < segundos: return opcion
        print("\nEl tiempo de espera ha finalizado.")
        while True:
            seguir = input("¿Deseas continuar en el sistema? (si/no): ").strip().lower()
            if seguir == "si": return "continue"
            elif seguir == "no": return "4"
            else: print("Respuesta no válida.")
    
    # --- Lógica de Negocio de la Tienda ---
    def registrar_nueva_venta(self) -> None:
        """Lógica para registrar una nueva venta en un reporte."""
        print("\n--- Registrar Nueva Venta ---")
        reportes = self.gestor.listar_reportes()
        if not reportes:
            print("No hay reportes de ventas. Crea uno primero con la opción 3.")
            return
        
        print("Reportes disponibles:", ", ".join(reportes))
        nombre_reporte = input("-> Escribe el nombre del reporte para añadir la venta: ").strip()

        producto = input("-> Nombre del producto: ").strip()
        if not producto:
            print("\nEl nombre del producto no puede estar vacío. Venta cancelada.")
            return
            
        while True:
            try:
                cantidad = float(input("-> Cantidad vendida: "))
                break
            except ValueError:
                print("Error: la cantidad debe ser un número.")
        while True:
            try:
                precio = float(input("-> Precio unitario: $"))
                break
            except ValueError:
                print("Error: el precio debe ser un número.")
                
        try:
            fecha = self.pedir_fecha()
            venta = Venta(producto, cantidad, precio, self.usuario)
            self.gestor.registrar_venta(nombre_reporte, venta, fecha)
            print(f"\n¡Venta registrada exitosamente en '{nombre_reporte}'!")
            print(f"Subtotal: ${venta.subtotal:.2f}")
        except FileNotFoundError as e:
            print(e)

    def ver_reporte_ventas(self) -> None:
        """Muestra un reporte de ventas y el total de ingresos."""
        print("\n--- Ver Reporte de Ventas ---")
        reportes = self.gestor.listar_reportes()
        if not reportes:
            print("No hay reportes de ventas para mostrar.")
            return
        
        print("Reportes disponibles:", ", ".join(reportes))
        nombre_reporte = input("-> Escribe el nombre del reporte que quieres ver: ").strip()
        if not nombre_reporte:
            print("No se seleccionó ningún reporte.")
            return

        try:
            contenido, total = self.gestor.leer_reporte(nombre_reporte)
            self.limpiar_pantalla()
            print(f"\n--- Contenido de: {nombre_reporte} ---")
            print(contenido if contenido else "(Reporte vacío)")
            print("-" * (len(nombre_reporte) + 20))
            print(f"TOTAL DE INGRESOS EN ESTE REPORTE: ${total:.2f}")
            print("-" * (len(nombre_reporte) + 20))
        except FileNotFoundError as e:
            print(e)
            
    def crear_reporte_mensual(self) -> None:
        """Crea un nuevo archivo de reporte mensual."""
        print("\n--- Crear Nuevo Reporte Mensual ---")
        try:
            anio = int(input("-> Ingresa el año (ej: 2023): "))
            mes = int(input("-> Ingresa el mes (ej: 10 para Octubre): "))
            if not (1 <= mes <= 12 and 2000 < anio < 2100):
                print("Error: Mes (1-12) o año inválido.")
                return
            
            path = self.gestor.crear_reporte_mensual(anio, mes)
            print(f"¡Éxito! Reporte '{path.name}' creado.")
        except ValueError:
            print("Error: Año y mes deben ser números.")
        except FileExistsError as e:
            print(e)

    def cambiar_usuario(self) -> None:
        """Cierra la sesión del usuario actual y solicita uno nuevo."""
        print("\n--- Cambiando de Vendedor ---")
        self.usuario = None
        self.pedir_usuario()
        self.carga(2)

    def gestionar_archivos(self) -> None:
        """Menú para gestión general de archivos."""
        while True:
            print("\n--- Gestión de Archivos ---")
            print("[1] Listar archivos | [2] Crear archivo")
            print("[3] Leer archivo | [4] Escribir en archivo")
            print("[5] Volver al menú principal")
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == "1":
                archivos = self.gestor.listar_todos_archivos()
                print(f"\nArchivos disponibles ({len(archivos)}):")
                for i, archivo in enumerate(archivos, 1):
                    print(f"{i}. {archivo}")
                    
            elif opcion == "2":
                nombre = input("Nombre del archivo: ").strip()
                contenido = input("Contenido inicial (opcional): ").strip()
                try:
                    self.gestor.crear_archivo_personalizado(nombre, contenido)
                    print(f"¡Archivo '{nombre}' creado exitosamente!")
                except FileExistsError as e:
                    print(e)
                    
            elif opcion == "3":
                archivos = self.gestor.listar_todos_archivos()
                if not archivos:
                    print("No hay archivos disponibles.")
                    continue
                    
                print("Archivos disponibles:", ", ".join(archivos))
                nombre = input("Nombre del archivo a leer: ").strip()
                try:
                    contenido = self.gestor.leer_archivo_general(nombre)
                    print(f"\n--- Contenido de {nombre} ---")
                    print(contenido)
                    print("-" * (len(nombre) + 20))
                except FileNotFoundError as e:
                    print(e)
                    
            elif opcion == "4":
                archivos = self.gestor.listar_todos_archivos()
                print("Archivos disponibles:", ", ".join(archivos))
                nombre = input("Nombre del archivo: ").strip()
                modo = input("Modo (w=sobrescribir, a=agregar): ").strip().lower()
                if modo not in ['w', 'a']:
                    print("Modo inválido.")
                    continue
                    
                print("Escribe el contenido (termina con una línea vacía):")
                lineas = []
                while True:
                    linea = input()
                    if not linea:
                        break
                    lineas.append(linea)
                
                contenido = "\n".join(lineas) + "\n"
                try:
                    self.gestor.escribir_archivo_general(nombre, contenido, modo)
                    print("¡Contenido guardado exitosamente!")
                except FileNotFoundError as e:
                    print(e)
                    
            elif opcion == "5":
                break
            else:
                print("Opción no válida.")
            
            input("\nPresiona Enter para continuar...")

    # --- Bucle Principal y Arranque ---
    def _sembrar_reportes_iniciales(self) -> None:
        """Asegura que existan reportes de ejemplo."""
        now = datetime.now()
        mes_actual_file = f"ventas_{now.year:04d}-{now.month:02d}.txt"
        if not (DATA_DIR / mes_actual_file).exists():
            (DATA_DIR / mes_actual_file).touch()

    def run(self) -> None:
        """Bucle principal que ejecuta la aplicación."""
        self.limpiar_pantalla()
        print("--- Sistema de Registro de Ventas v2.0 ---")
        self.pedir_usuario()
        self.carga()
        
        while True:
            self.limpiar_pantalla()
            self.mostrar_menu()
            opcion = self.input_con_timeout(600)
            
            self.limpiar_pantalla()
            if opcion == "continue": continue
            if opcion == "1": self.registrar_nueva_venta()
            elif opcion == "2": self.ver_reporte_ventas()
            elif opcion == "3": self.crear_reporte_mensual()
            elif opcion == "4": self.gestionar_archivos()
            elif opcion == "5": self.cambiar_usuario()
            elif opcion == "6":
                print("Cerrando sistema. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Elige un número del 1 al 6.")
            
            input("\nPresiona Enter para volver al menú...")

# --- Punto de Entrada de la Aplicación ---
if __name__ == "__main__":
    app = App()
    app.run()
