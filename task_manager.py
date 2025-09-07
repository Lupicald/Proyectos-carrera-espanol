#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Gestión de Tareas
============================
Un sistema simple y funcional para gestionar tareas diarias y proyectos.

Autor: Usuario
Fecha: 2025
"""

import json
import datetime
import os
import sys
from typing import List, Dict, Optional

# Códigos de colores ANSI para mejorar la interfaz
class Colors:
    """Códigos de colores ANSI para terminal."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    # Colores personalizados para la aplicación
    TITLE = '\033[1;96m'  # Cyan brillante
    SUCCESS = '\033[1;92m'  # Verde brillante
    WARNING = '\033[1;93m'  # Amarillo brillante
    ERROR = '\033[1;91m'  # Rojo brillante
    INFO = '\033[1;94m'  # Azul brillante
    MENU = '\033[1;95m'  # Magenta brillante
    TASK = '\033[1;97m'  # Blanco brillante

def safe_input(prompt: str) -> str:
    """Función segura para entrada de usuario que maneja problemas con sys.stdin."""
    try:
        return input(f"{Colors.CYAN}{prompt}{Colors.END}")
    except (EOFError, RuntimeError):
        # Si hay problemas con stdin, usar una alternativa
        print(f"\n{Colors.CYAN}{prompt}{Colors.END}", end="")
        try:
            # Intentar leer desde sys.stdin directamente
            return sys.stdin.readline().strip()
        except:
            # Si todo falla, devolver cadena vacía
            return ""

class TaskManager:
    """Gestor de tareas con funcionalidades básicas de CRUD."""
    
    def __init__(self, data_file: str = "tareas.json"):
        self.data_file = data_file
        self.tasks = self.load_tasks()
    
    def load_tasks(self) -> List[Dict]:
        """Cargar tareas desde archivo JSON."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_tasks(self) -> None:
        """Guardar tareas en archivo JSON."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)
    
    def add_task(self, title: str, description: str = "", priority: str = "media") -> int:
        """Agregar nueva tarea."""
        task_id = len(self.tasks) + 1
        new_task = {
            "id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "pendiente",
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed": None
        }
        self.tasks.append(new_task)
        self.save_tasks()
        return task_id
    
    def complete_task(self, task_id: int) -> bool:
        """Marcar tarea como completada."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completada"
                task["completed"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_tasks()
                return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Eliminar tarea."""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False
    
    def get_tasks(self, status: Optional[str] = None) -> List[Dict]:
        """Obtener tareas filtradas por estado."""
        if status:
            return [task for task in self.tasks if task["status"] == status]
        return self.tasks
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """Obtener tarea por ID."""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        """Actualizar tarea existente."""
        for task in self.tasks:
            if task["id"] == task_id:
                for key, value in kwargs.items():
                    if key in task:
                        task[key] = value
                self.save_tasks()
                return True
        return False
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas de tareas."""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["status"] == "completada"])
        pending = total - completed
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }
    
    def display_tasks(self, status: Optional[str] = None) -> None:
        """Mostrar tareas en consola con colores."""
        tasks = self.get_tasks(status)
        
        if not tasks:
            print(f"{Colors.WARNING}📝 No hay tareas para mostrar.{Colors.END}")
            return
        
        status_text = f"({len(tasks)} tareas)"
        if status:
            status_text = f"- {status.title()} {status_text}"
        
        print(f"\n{Colors.TITLE}📋 Lista de Tareas {status_text}{Colors.END}")
        print(f"{Colors.BLUE}{'=' * 60}{Colors.END}")
        
        for task in tasks:
            status_icon = f"{Colors.SUCCESS}✅" if task["status"] == "completada" else f"{Colors.WARNING}⏳"
            priority_icon = {
                "alta": f"{Colors.ERROR}🔴",
                "media": f"{Colors.WARNING}🟡", 
                "baja": f"{Colors.SUCCESS}🟢"
            }.get(task["priority"], f"{Colors.WHITE}⚪")
            
            print(f"{status_icon} {Colors.TASK}[{task['id']}]{Colors.END} {priority_icon} {Colors.TASK}{task['title']}{Colors.END}")
            if task['description']:
                print(f"   {Colors.INFO}📄 {task['description']}{Colors.END}")
            print(f"   {Colors.INFO}📅 Creada: {task['created']}{Colors.END}")
            if task['completed']:
                print(f"   {Colors.SUCCESS}✅ Completada: {task['completed']}{Colors.END}")
            print()

def main():
    """Función principal con menú interactivo."""
    try:
        task_manager = TaskManager()
        
        while True:
            # Limpiar pantalla (funciona en Windows y Linux/Mac)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Banner principal con colores
            print(f"\n{Colors.TITLE}{'='*70}{Colors.END}")
            print(f"{Colors.TITLE}🎯 GESTOR DE TAREAS PROFESIONAL{Colors.END}")
            print(f"{Colors.TITLE}{'='*70}{Colors.END}")
            print(f"{Colors.INFO}📊 Estadísticas rápidas:{Colors.END}")
            stats = task_manager.get_stats()
            print(f"   {Colors.SUCCESS}✅ Completadas: {stats['completed']}{Colors.END} | {Colors.WARNING}⏳ Pendientes: {stats['pending']}{Colors.END} | {Colors.TASK}📈 Progreso: {stats['completion_rate']:.1f}%{Colors.END}")
            print(f"{Colors.BLUE}{'='*70}{Colors.END}")
            
            # Menú con colores
            print(f"{Colors.MENU}📋 MENÚ PRINCIPAL{Colors.END}")
            print(f"{Colors.WHITE}1.{Colors.END} {Colors.SUCCESS}📝 Agregar nueva tarea{Colors.END}")
            print(f"{Colors.WHITE}2.{Colors.END} {Colors.INFO}📋 Ver todas las tareas{Colors.END}")
            print(f"{Colors.WHITE}3.{Colors.END} {Colors.WARNING}⏳ Ver tareas pendientes{Colors.END}")
            print(f"{Colors.WHITE}4.{Colors.END} {Colors.SUCCESS}✅ Ver tareas completadas{Colors.END}")
            print(f"{Colors.WHITE}5.{Colors.END} {Colors.SUCCESS}✅ Marcar tarea como completada{Colors.END}")
            print(f"{Colors.WHITE}6.{Colors.END} {Colors.INFO}✏️  Editar tarea existente{Colors.END}")
            print(f"{Colors.WHITE}7.{Colors.END} {Colors.ERROR}🗑️  Eliminar tarea{Colors.END}")
            print(f"{Colors.WHITE}8.{Colors.END} {Colors.CYAN}📊 Estadísticas detalladas{Colors.END}")
            print(f"{Colors.WHITE}9.{Colors.END} {Colors.ERROR}🚪 Salir del programa{Colors.END}")
            print(f"{Colors.BLUE}{'='*70}{Colors.END}")
            
            choice = safe_input("Selecciona una opción (1-9): ").strip()
            
            if choice == "1":
                print(f"\n{Colors.SUCCESS}📝 AGREGAR NUEVA TAREA{Colors.END}")
                print(f"{Colors.BLUE}{'='*40}{Colors.END}")
                title = safe_input("📝 Título de la tarea: ").strip()
                description = safe_input("📄 Descripción (opcional): ").strip()
                priority = safe_input("🎯 Prioridad (alta/media/baja) [media]: ").strip().lower()
                if not priority:
                    priority = "media"
                
                task_id = task_manager.add_task(title, description, priority)
                print(f"\n{Colors.SUCCESS}✅ ¡Tarea agregada exitosamente con ID: {task_id}!{Colors.END}")
                input(f"\n{Colors.INFO}Presiona Enter para continuar...{Colors.END}")
            
            elif choice == "2":
                task_manager.display_tasks()
                input(f"\n{Colors.INFO}Presiona Enter para continuar...{Colors.END}")
            
            elif choice == "3":
                task_manager.display_tasks("pendiente")
                input(f"\n{Colors.INFO}Presiona Enter para continuar...{Colors.END}")
            
            elif choice == "4":
                task_manager.display_tasks("completada")
                input(f"\n{Colors.INFO}Presiona Enter para continuar...{Colors.END}")
            
            elif choice == "5":
                print(f"\n{Colors.SUCCESS}✅ COMPLETAR TAREA{Colors.END}")
                print(f"{Colors.BLUE}{'='*30}{Colors.END}")
                task_manager.display_tasks("pendiente")
                try:
                    task_id = int(safe_input("ID de la tarea a completar: "))
                    if task_manager.complete_task(task_id):
                        print(f"\n{Colors.SUCCESS}✅ ¡Tarea marcada como completada exitosamente!{Colors.END}")
                    else:
                        print(f"\n{Colors.ERROR}❌ Tarea no encontrada{Colors.END}")
                except ValueError:
                    print(f"\n{Colors.ERROR}❌ ID inválido{Colors.END}")
                input(f"\n{Colors.INFO}Presiona Enter para continuar...{Colors.END}")
            
            elif choice == "6":
                print(f"\n{Colors.INFO}✏️ EDITAR TAREA{Colors.END}")
                print(f"{Colors.BLUE}{'='*25}{Colors.END}")
                task_manager.display_tasks()
                try:
                    task_id = int(safe_input("ID de la tarea a editar: "))
                    task = task_manager.get_task_by_id(task_id)
                    if task:
                        print(f"\n{Colors.INFO}Editando: {Colors.TASK}{task['title']}{Colors.END}")
                        new_title = safe_input(f"Nuevo título [{task['title']}]: ").strip()
                        new_desc = safe_input(f"Nueva descripción [{task['description']}]: ").strip()
                        new_priority = safe_input(f"Nueva prioridad [{task['priority']}]: ").strip().lower()
                        
                        updates = {}
                        if new_title:
                            updates['title'] = new_title
                        if new_desc:
                            updates['description'] = new_desc
                        if new_priority:
                            updates['priority'] = new_priority
                        
                        if updates:
                            task_manager.update_task(task_id, **updates)
                            print(f"\n{Colors.SUCCESS}✅ ¡Tarea actualizada exitosamente!{Colors.END}")
                        else:
                            print(f"\n{Colors.WARNING}ℹ️ No se realizaron cambios{Colors.END}")
                    else:
                        print(f"\n{Colors.ERROR}❌ Tarea no encontrada{Colors.END}")
                except ValueError:
                    print(f"\n{Colors.ERROR}❌ ID inválido{Colors.END}")
                input(f"\n{Colors.INFO}Presiona Enter para continuar...{Colors.END}")
            
            elif choice == "7":
                print(f"\n{Colors.ERROR}🗑️ ELIMINAR TAREA{Colors.END}")
                print(f"{Colors.BLUE}{'='*25}{Colors.END}")
                task_manager.display_tasks()
                try:
                    task_id = int(safe_input("ID de la tarea a eliminar: "))
                    if task_manager.delete_task(task_id):
                        print(f"\n{Colors.SUCCESS}🗑️ ¡Tarea eliminada exitosamente!{Colors.END}")
                    else:
                        print(f"\n{Colors.ERROR}❌ Tarea no encontrada{Colors.END}")
                except ValueError:
                    print(f"\n{Colors.ERROR}❌ ID inválido{Colors.END}")
                input(f"\n{Colors.INFO}Presiona Enter para continuar...{Colors.END}")
            
            elif choice == "8":
                stats = task_manager.get_stats()
                print(f"\n{Colors.CYAN}📊 ESTADÍSTICAS DETALLADAS{Colors.END}")
                print(f"{Colors.BLUE}{'='*35}{Colors.END}")
                print(f"{Colors.TASK}📈 Total de tareas: {stats['total']}{Colors.END}")
                print(f"{Colors.SUCCESS}✅ Completadas: {stats['completed']}{Colors.END}")
                print(f"{Colors.WARNING}⏳ Pendientes: {stats['pending']}{Colors.END}")
                print(f"{Colors.INFO}📊 Tasa de completado: {stats['completion_rate']:.1f}%{Colors.END}")
                
                # Barra de progreso visual
                if stats['total'] > 0:
                    progress_bar = "█" * int(stats['completion_rate'] / 5) + "░" * (20 - int(stats['completion_rate'] / 5))
                    print(f"\n{Colors.INFO}Progreso: [{Colors.SUCCESS}{progress_bar}{Colors.INFO}] {stats['completion_rate']:.1f}%{Colors.END}")
                
                input(f"\n{Colors.INFO}Presiona Enter para continuar...{Colors.END}")
            
            elif choice == "9":
                print(f"\n{Colors.SUCCESS}👋 ¡Gracias por usar el Gestor de Tareas!{Colors.END}")
                print(f"{Colors.INFO}¡Hasta la próxima!{Colors.END}")
                break
            
            else:
                print(f"\n{Colors.ERROR}❌ Opción inválida. Por favor, selecciona un número del 1 al 9.{Colors.END}")
                input(f"\n{Colors.INFO}Presiona Enter para continuar...{Colors.END}")
    
    except (EOFError, RuntimeError, KeyboardInterrupt) as e:
        print(f"\n{Colors.ERROR}❌ Error: {e}{Colors.END}")
        print(f"{Colors.INFO}👋 Cerrando aplicación...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.ERROR}❌ Error inesperado: {e}{Colors.END}")
        print(f"{Colors.INFO}👋 Cerrando aplicación...{Colors.END}")

if __name__ == "__main__":
    main()
