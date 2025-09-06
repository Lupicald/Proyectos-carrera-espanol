#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear ejecutables con PyInstaller
=============================================
Facilita la creación de ejecutables para diferentes proyectos.

Uso:
    python build_exe.py task_manager.py
    python build_exe.py trackerforgames/trackerforgames.py
"""

import subprocess
import sys
import os
from pathlib import Path

def create_exe(script_path, exe_name=None, console=True):
    """
    Crear ejecutable usando PyInstaller.
    
    Args:
        script_path (str): Ruta al script Python
        exe_name (str): Nombre del ejecutable (opcional)
        console (bool): Si mostrar consola (True) o ventana (False)
    """
    
    if not os.path.exists(script_path):
        print(f"❌ Error: El archivo {script_path} no existe")
        return False
    
    # Generar nombre del ejecutable si no se proporciona
    if not exe_name:
        exe_name = Path(script_path).stem
    
    # Construir comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",  # Un solo archivo
        "--name", exe_name,
        "--clean"     # Limpiar archivos temporales
    ]
    
    # Agregar opción de ventana o consola
    if not console:
        cmd.append("--windowed")
    else:
        cmd.append("--console")
    
    # Agregar el script
    cmd.append(script_path)
    
    print(f"🔨 Creando ejecutable: {exe_name}.exe")
    print(f"📁 Script: {script_path}")
    print(f"🖥️  Consola: {'Sí' if console else 'No'}")
    print("-" * 50)
    
    try:
        # Ejecutar PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Ejecutable creado exitosamente!")
        print(f"📂 Ubicación: dist/{exe_name}.exe")
        
        # Mostrar tamaño del archivo
        exe_path = f"dist/{exe_name}.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📏 Tamaño: {size_mb:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear ejecutable:")
        print(f"   Código: {e.returncode}")
        print(f"   Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller no está instalado. Instálalo con:")
        print("   pip install pyinstaller")
        return False

def main():
    """Función principal."""
    if len(sys.argv) < 2:
        print("📋 Uso: python build_exe.py <script.py> [nombre_ejecutable] [--windowed]")
        print("\nEjemplos:")
        print("  python build_exe.py task_manager.py")
        print("  python build_exe.py trackerforgames/trackerforgames.py")
        print("  python build_exe.py task_manager.py MiGestorTareas --windowed")
        return
    
    script_path = sys.argv[1]
    exe_name = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    console = '--windowed' not in sys.argv
    
    success = create_exe(script_path, exe_name, console)
    
    if success:
        print("\n🎉 ¡Listo! Puedes ejecutar el programa desde:")
        print(f"   dist/{exe_name or Path(script_path).stem}.exe")

if __name__ == "__main__":
    main()
