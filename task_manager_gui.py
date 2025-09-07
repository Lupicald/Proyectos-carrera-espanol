#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Gestión de Tareas - Versión GUI
==========================================
Una aplicación con interfaz gráfica para gestionar tareas diarias y proyectos.

Autor: Usuario
Fecha: 2025
"""

import json
import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Dict, Optional

class TaskManagerGUI:
    """Gestor de tareas con interfaz gráfica usando Tkinter."""
    
    def __init__(self):
        self.data_file = "tareas.json"
        self.tasks = self.load_tasks()
        self.root = tk.Tk()
        self.setup_gui()
        self.refresh_task_list()
    
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
    
    def setup_gui(self):
        """Configurar la interfaz gráfica."""
        self.root.title("🎯 Gestor de Tareas Profesional")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🎯 Gestor de Tareas Profesional", 
                              font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.N), padx=(0, 10))
        
        # Botones
        ttk.Button(button_frame, text="📝 Agregar Tarea", 
                  command=self.add_task_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="✏️ Editar Tarea", 
                  command=self.edit_task_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="✅ Completar", 
                  command=self.complete_task).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="🗑️ Eliminar", 
                  command=self.delete_task).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="📊 Estadísticas", 
                  command=self.show_stats).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="🔄 Actualizar", 
                  command=self.refresh_task_list).pack(fill=tk.X, pady=2)
        
        # Frame de la lista de tareas
        list_frame = ttk.LabelFrame(main_frame, text="📋 Lista de Tareas", padding="5")
        list_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview para mostrar tareas
        columns = ('ID', 'Título', 'Descripción', 'Prioridad', 'Estado', 'Creada')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.task_tree.heading('ID', text='ID')
        self.task_tree.heading('Título', text='Título')
        self.task_tree.heading('Descripción', text='Descripción')
        self.task_tree.heading('Prioridad', text='Prioridad')
        self.task_tree.heading('Estado', text='Estado')
        self.task_tree.heading('Creada', text='Creada')
        
        # Configurar ancho de columnas
        self.task_tree.column('ID', width=50)
        self.task_tree.column('Título', width=150)
        self.task_tree.column('Descripción', width=200)
        self.task_tree.column('Prioridad', width=80)
        self.task_tree.column('Estado', width=100)
        self.task_tree.column('Creada', width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid para treeview y scrollbar
        self.task_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Frame de filtros
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(filter_frame, text="Filtrar por estado:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="Todas")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["Todas", "Pendiente", "Completada"], 
                                   state="readonly", width=15)
        filter_combo.pack(side=tk.LEFT, padx=(0, 10))
        filter_combo.bind('<<ComboboxSelected>>', self.filter_tasks)
        
        # Estadísticas rápidas
        self.stats_label = ttk.Label(filter_frame, text="", font=('Arial', 10))
        self.stats_label.pack(side=tk.RIGHT)
        
        self.update_stats()
    
    def refresh_task_list(self):
        """Actualizar la lista de tareas en el Treeview."""
        # Limpiar lista actual
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Agregar tareas
        for task in self.tasks:
            status_icon = "✅" if task["status"] == "completada" else "⏳"
            priority_icon = {
                "alta": "🔴",
                "media": "🟡", 
                "baja": "🟢"
            }.get(task["priority"], "⚪")
            
            self.task_tree.insert('', tk.END, values=(
                task['id'],
                task['title'],
                task['description'][:50] + "..." if len(task['description']) > 50 else task['description'],
                f"{priority_icon} {task['priority'].title()}",
                f"{status_icon} {task['status'].title()}",
                task['created']
            ))
    
    def filter_tasks(self, event=None):
        """Filtrar tareas por estado."""
        filter_value = self.filter_var.get()
        
        # Limpiar lista actual
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Filtrar y agregar tareas
        filtered_tasks = self.tasks
        if filter_value != "Todas":
            filtered_tasks = [task for task in self.tasks if task["status"] == filter_value.lower()]
        
        for task in filtered_tasks:
            status_icon = "✅" if task["status"] == "completada" else "⏳"
            priority_icon = {
                "alta": "🔴",
                "media": "🟡", 
                "baja": "🟢"
            }.get(task["priority"], "⚪")
            
            self.task_tree.insert('', tk.END, values=(
                task['id'],
                task['title'],
                task['description'][:50] + "..." if len(task['description']) > 50 else task['description'],
                f"{priority_icon} {task['priority'].title()}",
                f"{status_icon} {task['status'].title()}",
                task['created']
            ))
    
    def update_stats(self):
        """Actualizar estadísticas rápidas."""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["status"] == "completada"])
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        stats_text = f"📊 Total: {total} | ✅ Completadas: {completed} | ⏳ Pendientes: {pending} | 📈 Progreso: {completion_rate:.1f}%"
        self.stats_label.config(text=stats_text)
    
    def add_task_dialog(self):
        """Mostrar diálogo para agregar nueva tarea."""
        dialog = TaskDialog(self.root, "Agregar Nueva Tarea")
        if dialog.result:
            task_id = len(self.tasks) + 1
            new_task = {
                "id": task_id,
                "title": dialog.result["title"],
                "description": dialog.result["description"],
                "priority": dialog.result["priority"],
                "status": "pendiente",
                "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "completed": None
            }
            self.tasks.append(new_task)
            self.save_tasks()
            self.refresh_task_list()
            self.update_stats()
            messagebox.showinfo("Éxito", f"✅ Tarea agregada exitosamente con ID: {task_id}")
    
    def edit_task_dialog(self):
        """Mostrar diálogo para editar tarea."""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor selecciona una tarea para editar.")
            return
        
        item = self.task_tree.item(selected[0])
        task_id = int(item['values'][0])
        
        # Encontrar la tarea
        task = None
        for t in self.tasks:
            if t['id'] == task_id:
                task = t
                break
        
        if task:
            dialog = TaskDialog(self.root, "Editar Tarea", task)
            if dialog.result:
                task.update(dialog.result)
                self.save_tasks()
                self.refresh_task_list()
                self.update_stats()
                messagebox.showinfo("Éxito", "✅ Tarea actualizada exitosamente")
    
    def complete_task(self):
        """Marcar tarea como completada."""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor selecciona una tarea para completar.")
            return
        
        item = self.task_tree.item(selected[0])
        task_id = int(item['values'][0])
        
        for task in self.tasks:
            if task["id"] == task_id:
                if task["status"] == "completada":
                    messagebox.showinfo("Info", "Esta tarea ya está completada.")
                    return
                task["status"] = "completada"
                task["completed"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_tasks()
                self.refresh_task_list()
                self.update_stats()
                messagebox.showinfo("Éxito", "✅ Tarea marcada como completada")
                return
        
        messagebox.showerror("Error", "❌ Tarea no encontrada")
    
    def delete_task(self):
        """Eliminar tarea."""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor selecciona una tarea para eliminar.")
            return
        
        item = self.task_tree.item(selected[0])
        task_id = int(item['values'][0])
        task_title = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar la tarea '{task_title}'?"):
            for i, task in enumerate(self.tasks):
                if task["id"] == task_id:
                    del self.tasks[i]
                    self.save_tasks()
                    self.refresh_task_list()
                    self.update_stats()
                    messagebox.showinfo("Éxito", "🗑️ Tarea eliminada exitosamente")
                    return
            
            messagebox.showerror("Error", "❌ Tarea no encontrada")
    
    def show_stats(self):
        """Mostrar estadísticas detalladas."""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["status"] == "completada"])
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        stats_text = f"""📊 ESTADÍSTICAS DETALLADAS

📈 Total de tareas: {total}
✅ Completadas: {completed}
⏳ Pendientes: {pending}
📊 Tasa de completado: {completion_rate:.1f}%

Progreso visual:
{'█' * int(completion_rate / 5)}{'░' * (20 - int(completion_rate / 5))} {completion_rate:.1f}%"""
        
        messagebox.showinfo("Estadísticas", stats_text)
    
    def run(self):
        """Ejecutar la aplicación."""
        self.root.mainloop()


class TaskDialog:
    """Diálogo para agregar/editar tareas."""
    
    def __init__(self, parent, title, task=None):
        self.result = None
        
        # Crear ventana de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos del formulario
        ttk.Label(main_frame, text="📝 Título:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.title_var = tk.StringVar()
        if task:
            self.title_var.set(task['title'])
        title_entry = ttk.Entry(main_frame, textvariable=self.title_var, width=50)
        title_entry.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(main_frame, text="📄 Descripción:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.desc_var = tk.StringVar()
        if task:
            self.desc_var.set(task['description'])
        desc_entry = ttk.Entry(main_frame, textvariable=self.desc_var, width=50)
        desc_entry.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(main_frame, text="🎯 Prioridad:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.priority_var = tk.StringVar()
        if task:
            self.priority_var.set(task['priority'])
        else:
            self.priority_var.set("media")
        
        priority_frame = ttk.Frame(main_frame)
        priority_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Radiobutton(priority_frame, text="🔴 Alta", variable=self.priority_var, value="alta").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(priority_frame, text="🟡 Media", variable=self.priority_var, value="media").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(priority_frame, text="🟢 Baja", variable=self.priority_var, value="baja").pack(side=tk.LEFT)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="✅ Guardar", command=self.save).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="❌ Cancelar", command=self.cancel).pack(side=tk.RIGHT)
        
        # Enfocar el primer campo
        title_entry.focus()
        
        # Esperar a que se cierre el diálogo
        self.dialog.wait_window()
    
    def save(self):
        """Guardar los datos del formulario."""
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("Error", "El título es obligatorio.")
            return
        
        self.result = {
            "title": title,
            "description": self.desc_var.get().strip(),
            "priority": self.priority_var.get()
        }
        self.dialog.destroy()
    
    def cancel(self):
        """Cancelar el diálogo."""
        self.dialog.destroy()


def main():
    """Función principal."""
    app = TaskManagerGUI()
    app.run()


if __name__ == "__main__":
    main()

