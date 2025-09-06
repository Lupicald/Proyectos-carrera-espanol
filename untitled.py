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
from typing import List, Dict, Optional

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
        """Mostrar tareas en consola."""
        tasks = self.get_tasks(status)
        
        if not tasks:
            print("📝 No hay tareas para mostrar.")
            return
        
        print(f"\n📋 Lista de Tareas ({len(tasks)} tareas)")
        print("=" * 50)
        
        for task in tasks:
            status_icon = "✅" if task["status"] == "completada" else "⏳"
            priority_icon = {
                "alta": "🔴",
                "media": "🟡", 
                "baja": "🟢"
            }.get(task["priority"], "⚪")
            
            print(f"{status_icon} [{task['id']}] {priority_icon} {task['title']}")
            if task['description']:
                print(f"   📄 {task['description']}")
            print(f"   📅 Creada: {task['created']}")
            if task['completed']:
                print(f"   ✅ Completada: {task['completed']}")
            print()

def main():
    """Función principal con menú interactivo."""
    task_manager = TaskManager()
    
    while True:
        print("\n" + "="*50)
        print("🎯 GESTOR DE TAREAS")
        print("="*50)
        print("1. 📝 Agregar tarea")
        print("2. 📋 Ver todas las tareas")
        print("3. ⏳ Ver tareas pendientes")
        print("4. ✅ Ver tareas completadas")
        print("5. ✅ Marcar tarea como completada")
        print("6. ✏️  Editar tarea")
        print("7. 🗑️  Eliminar tarea")
        print("8. 📊 Estadísticas")
        print("9. 🚪 Salir")
        print("="*50)
        
        choice = input("Selecciona una opción (1-9): ").strip()
        
        if choice == "1":
            title = input("📝 Título de la tarea: ").strip()
            description = input("📄 Descripción (opcional): ").strip()
            priority = input("🎯 Prioridad (alta/media/baja) [media]: ").strip().lower()
            if not priority:
                priority = "media"
            
            task_id = task_manager.add_task(title, description, priority)
            print(f"✅ Tarea agregada con ID: {task_id}")
        
        elif choice == "2":
            task_manager.display_tasks()
        
        elif choice == "3":
            task_manager.display_tasks("pendiente")
        
        elif choice == "4":
            task_manager.display_tasks("completada")
        
        elif choice == "5":
            task_manager.display_tasks("pendiente")
            try:
                task_id = int(input("ID de la tarea a completar: "))
                if task_manager.complete_task(task_id):
                    print("✅ Tarea marcada como completada")
                else:
                    print("❌ Tarea no encontrada")
            except ValueError:
                print("❌ ID inválido")
        
        elif choice == "6":
            task_manager.display_tasks()
            try:
                task_id = int(input("ID de la tarea a editar: "))
                task = task_manager.get_task_by_id(task_id)
                if task:
                    new_title = input(f"Nuevo título [{task['title']}]: ").strip()
                    new_desc = input(f"Nueva descripción [{task['description']}]: ").strip()
                    new_priority = input(f"Nueva prioridad [{task['priority']}]: ").strip().lower()
                    
                    updates = {}
                    if new_title:
                        updates['title'] = new_title
                    if new_desc:
                        updates['description'] = new_desc
                    if new_priority:
                        updates['priority'] = new_priority
                    
                    if updates:
                        task_manager.update_task(task_id, **updates)
                        print("✅ Tarea actualizada")
                    else:
                        print("ℹ️  No se realizaron cambios")
                else:
                    print("❌ Tarea no encontrada")
            except ValueError:
                print("❌ ID inválido")
        
        elif choice == "7":
            task_manager.display_tasks()
            try:
                task_id = int(input("ID de la tarea a eliminar: "))
                if task_manager.delete_task(task_id):
                    print("🗑️  Tarea eliminada")
                else:
                    print("❌ Tarea no encontrada")
            except ValueError:
                print("❌ ID inválido")
        
        elif choice == "8":
            stats = task_manager.get_stats()
            print(f"\n📊 ESTADÍSTICAS")
            print(f"Total de tareas: {stats['total']}")
            print(f"Completadas: {stats['completed']}")
            print(f"Pendientes: {stats['pending']}")
            print(f"Tasa de completado: {stats['completion_rate']:.1f}%")
        
        elif choice == "9":
            print("👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()
