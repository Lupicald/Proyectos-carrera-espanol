"""
Sistema de registro con POO (v2).
Objetivo: mejorar estructura, reutilización, manejo de archivos y excepciones.
"""

from __future__ import annotations
import os
from pathlib import Path
import time
import logging
from datetime import datetime
from typing import Tuple, List, Optional

# Windows: entrada no bloqueante para el timeout opcional
try:
    import msvcrt  # Solo Windows
    WINDOWS = True
except Exception:
    WINDOWS = False

# --- Configuración de logging ---
LOG_DIR = Path(__file__).with_name("logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

DATA_DIR = Path(__file__).with_name("data")  # Carpeta para archivos de ejemplo
DATA_DIR.mkdir(exist_ok=True)


class Usuario:
    """Representa a un usuario del sistema."""

    def __init__(self, nickname: str) -> None:
        self.nickname = nickname.strip()

    def saludo(self) -> str:
        return f"Bienvenido/a, {self.nickname}."


class Venta:
    """Entidad de Venta. Mantén simple: producto, precio, cantidad, fecha, usuario."""

    def __init__(
        self,
        producto: str,
        precio: float,
        cantidad: float,
        fecha: Tuple[int, int, int],
        usuario: Usuario,
    ) -> None:
        self.producto = producto
        self.precio = precio
        self.cantidad = cantidad
        self.fecha = fecha  # (día, mes, año)
        self.usuario = usuario

    @property
    def subtotal(self) -> float:
        return self.precio * self.cantidad

    def to_line(self) -> str:
        d, m, a = self.fecha
        return f"{a:04d}-{m:02d}-{d:02d},{self.usuario.nickname},{self.producto},{self.cantidad},{self.precio},{self.subtotal}\n"


class GestorArchivos:
    """Operaciones de crear, escribir y leer archivos con manejo de errores."""

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    def listar(self) -> List[str]:
        return [p.name for p in self.base_dir.glob("*.txt")]

    def crear(self, nombre: str, fecha: Tuple[int, int, int]) -> Path:
        d, m, a = fecha
        # Sugerencia: incorpora la fecha al nombre
        fname = f"{nombre}_{a:04d}{m:02d}{d:02d}.txt"
        path = self.base_dir / fname
        if path.exists():
            raise FileExistsError(f"El archivo {fname} ya existe.")
        path.write_text("")  # crea vacío
        logging.info("Archivo creado: %s", path)
        return path

    def escribir(self, nombre: str, contenido: str) -> None:
        path = self.base_dir / nombre
        if not path.exists():
            raise FileNotFoundError(f"No existe: {nombre}")
        with path.open("a", encoding="utf-8") as f:
            f.write(contenido)
        logging.info("Escritura OK en: %s", path)

    def leer(self, nombre: str) -> str:
        path = self.base_dir / nombre
        if not path.exists():
            raise FileNotFoundError(f"No existe: {nombre}")
        data = path.read_text(encoding="utf-8")
        logging.info("Lectura OK de: %s", path)
        return data


class App:
    """Controla el flujo de la aplicación."""

    def __init__(self) -> None:
        self.usuario: Optional[Usuario] = None
        self.archivos = GestorArchivos(DATA_DIR)
        self._sembrar_archivos()  # Tener 4+ archivos para lectura

    # ---------- Utilidades de UI ----------
    def pedir_usuario(self) -> None:
        nick = input("Escribe tu nombre o nickname: ").strip()
        self.usuario = Usuario(nick)
        print(self.usuario.saludo())
        logging.info("Usuario activo: %s", self.usuario.nickname)

    def carga(self, max_seg: int = 5) -> None:
        """Mensaje de espera (máx. 5s)."""
        max_seg = min(max_seg, 5)
        print("Cargando programa", end="", flush=True)
        for _ in range(max_seg):
            time.sleep(1)
            print(".", end="", flush=True)
        print()

    def pedir_fecha(self) -> Tuple[int, int, int]:
        """Solicita fecha dd/mm/aaaa y retorna tupla (d, m, a) con validación."""
        while True:
            s = input("Ingresa la fecha (dd/mm/aaaa): ").strip()
            try:
                dt = datetime.strptime(s, "%d/%m/%Y")
                return (dt.day, dt.month, dt.year)
            except ValueError:
                print("Formato inválido. Ejemplo: 12/06/2023")

    # ---------- Menú con timeout ----------
    def mostrar_menu(self) -> None:
        # Matriz de opciones (fila x columna)
        print("\n=== Menú Principal ===")
        print("[1] Crear archivo    | [2] Escribir archivo")
        print("[3] Leer archivo     | [4] Cambiar usuario")
        print("[5] Salir")

    def input_con_timeout(self, segundos: int = 600) -> Optional[str]:
        """
        Lee la opción con un for que mide el tiempo.
        Si pasan 'segundos' sin elegir, pregunta si desea continuar.
        En Windows, usa entrada no bloqueante (msvcrt) para cumplir el enunciado.
        """
        if WINDOWS:
            print("Selecciona una opción (tienes 10 minutos): ", end="", flush=True)
            buffer = ""
            for _ in range(segundos):
                time.sleep(1)
                # Si hay teclas presionadas, acumular
                while msvcrt.kbhit():
                    ch = msvcrt.getwch()
                    if ch == "\r":  # Enter
                        print()
                        return buffer.strip()
                    elif ch == "\b":
                        buffer = buffer[:-1]
                    else:
                        buffer += ch
                # (Opcional) mostrar un pequeño indicador cada 30s
                # TODO: mostrar progreso si lo deseas
            # Timeout
            print("\nHan pasado 10 minutos sin seleccionar.")
            seguir = input("¿Deseas continuar? (si/no): ").strip().lower()
            if seguir == "si":
                return None  # vuelve al menú
            else:
                return "5"  # salir
        else:
            # Fallback simple: medir el tiempo entre prompt y respuesta.
            inicio = time.monotonic()
            op = input("Selecciona una opción: ").strip()
            transcurrido = time.monotonic() - inicio
            if transcurrido >= segundos:
                seguir = input("¿Deseas continuar? (si/no): ").strip().lower()
                if seguir != "si":
                    return "5"
            return op

    # ---------- Casos de uso ----------
    def crear_archivo(self) -> None:
        fecha = self.pedir_fecha()
        nombre = input("Nombre base del archivo: ").strip()
        try:
            path = self.archivos.crear(nombre, fecha)
            print(f"Archivo creado: {path.name}")
        except FileExistsError as e:
            print(e)

    def escribir_archivo(self) -> None:
        files = self.archivos.listar()
        if not files:
            print("No hay archivos. Crea uno primero.")
            return
        print("Archivos disponibles:", files)
        nombre = input("¿A cuál escribir? (exacto): ").strip()
        # Ejemplo de contenido: registro de venta (puedes cambiarlo)
        fecha = self.pedir_fecha()
        # TODO: pide datos reales de la venta si tu caso de uso lo requiere
        producto = input("Producto: ")
        try:
            precio = float(input("Precio: "))
            cantidad = float(input("Cantidad: "))
        except ValueError:
            print("Precio y cantidad deben ser numéricos.")
            return
        venta = Venta(producto, precio, cantidad, fecha, self.usuario or Usuario("anon"))
        try:
            self.archivos.escribir(nombre, venta.to_line())
            print("Escritura realizada.")
        except FileNotFoundError as e:
            print(e)

    def leer_archivo(self) -> None:
        files = self.archivos.listar()
        if not files:
            print("No hay archivos para leer.")
            return
        print("Archivos disponibles:", files)
        nombre = input("¿Cuál deseas abrir? (exacto): ").strip()
        try:
            contenido = self.archivos.leer(nombre)
            print("\n--- Contenido ---")
            print(contenido if contenido else "(vacío)")
        except FileNotFoundError as e:
            print(e)

    def cambiar_usuario(self) -> None:
        self.pedir_usuario()

    # ---------- Bootstrapping ----------
    def _sembrar_archivos(self) -> None:
        """Garantiza que existan ≥4 archivos para pruebas de lectura."""
        base = ["inventario", "precios", "ventas", "notas"]
        for n in base:
            p = DATA_DIR / f"{n}.txt"
            if not p.exists():
                p.write_text("", encoding="utf-8")

    # ---------- Loop principal ----------
    def run(self) -> None:
        print("Sistema de Registro (POO)")
        self.pedir_usuario()
        self.carga(5)
        while True:
            self.mostrar_menu()
            op = self.input_con_timeout(600)
            if op is None:
                # Usuario eligió continuar tras timeout
                continue
            if op == "1":
                self.crear_archivo()
            elif op == "2":
                self.escribir_archivo()
            elif op == "3":
                self.leer_archivo()
            elif op == "4":
                self.cambiar_usuario()
            elif op == "5":
                print("Saliendo. ¡Hasta luego!")
                break
            else:
                print("Opción inválida.")

if __name__ == "__main__":
    app = App()
    app.run()