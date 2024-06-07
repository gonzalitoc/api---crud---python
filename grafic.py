import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:5000"

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        
        tk.Label(root, text="Usuario").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(root, text="Contraseña").grid(row=1, column=0, padx=10, pady=10)
        
        self.usuario_entry = tk.Entry(root)
        self.passw_entry = tk.Entry(root, show="*")
        
        self.usuario_entry.grid(row=0, column=1, padx=10, pady=10)
        self.passw_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Button(root, text="Iniciar Sesión", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        usuario = self.usuario_entry.get()
        passw = self.passw_entry.get()
        
        response = requests.post(f"{API_URL}/login", json={"usuario": usuario, "passw": passw})
        
        if response.status_code == 200:
            messagebox.showinfo("Éxito", f"Inicio de sesión exitoso, bienvenido {usuario}")
            self.root.destroy()
            main_app()
        else:
            messagebox.showerror("Error", "Usuario o contraseña invalida")

class ListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Registros")

        self.create_widgets()
        self.get_records()  # Obtener registros al inicio

    def create_widgets(self):
        # Crear un Treeview para listar los registros
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Descripción"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        
        self.tree.grid(row=0, column=0, padx=50, pady=20, sticky="nsew")

        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=150)
        self.tree.column("Descripción", width=600)

        self.root.columnconfigure(0, weight=2)
        self.root.rowconfigure(0, weight=2)

        # Botones CRUD
        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ns")

        tk.Button(btn_frame, text="Agregar", command=self.add_record).pack(pady=10)
        tk.Button(btn_frame, text="Editar", command=self.edit_record).pack(pady=10)
        tk.Button(btn_frame, text="Eliminar", command=self.delete_record).pack(pady=10)
        tk.Button(btn_frame, text="Cerrar Sesión", command=self.logout).pack(pady=10)

    def get_records(self):
        response = requests.get(f"{API_URL}/ping")
        if response.status_code == 200:
            records = response.json()["Datos"]
            self.tree.delete(*self.tree.get_children())
            for record in records:
                self.tree.insert("", "end", values=(record["id_producto"], record["nombre"], record["descripcion"]))
        else:
            messagebox.showerror("Error", "Error al obtener los registros")

    def add_record(self):
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Agregar Registro")
        
        tk.Label(self.edit_window, text="Nombre").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.edit_window, text="Descripción").grid(row=1, column=0, padx=10, pady=10)
        
        self.nombre_entry = tk.Entry(self.edit_window)
        self.desc_entry = tk.Entry(self.edit_window)
        
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=10)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Button(self.edit_window, text="Guardar", command=self.save_new_record).grid(row=2, column=0, columnspan=2, pady=10)

    def save_new_record(self):
        nombre = self.nombre_entry.get()
        descripcion = self.desc_entry.get()
        
        response = requests.post(f"{API_URL}/ping", json={"nombre": nombre, "descripcion": descripcion})
        if response.status_code == 200:
            messagebox.showinfo("Éxito", "Registro agregado correctamente")
            self.edit_window.destroy()
            self.get_records()
        else:
            messagebox.showerror("Error", "Error al agregar el registro")
    
    def edit_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            record_id = item['values'][0]
            nombre = item['values'][1]
            descripcion = item['values'][2]

            self.edit_window = tk.Toplevel(self.root)
            self.edit_window.title("Editar Registro")
            
            tk.Label(self.edit_window, text="Nombre").grid(row=0, column=0, padx=10, pady=10)
            tk.Label(self.edit_window, text="Descripción").grid(row=1, column=0, padx=10, pady=10)
            
            self.nombre_entry = tk.Entry(self.edit_window)
            self.desc_entry = tk.Entry(self.edit_window)
            
            self.nombre_entry.grid(row=0, column=1, padx=10, pady=10)
            self.desc_entry.grid(row=1, column=1, padx=10, pady=10)
            
            self.nombre_entry.insert(0, nombre)
            self.desc_entry.insert(0, descripcion)
            
            tk.Button(self.edit_window, text="Guardar", command=lambda: self.update_record(record_id)).grid(row=2, column=0, columnspan=2, pady=10)
        else:
            messagebox.showerror("Error", "Seleccione un registro para editar")
    
    def update_record(self, record_id):
        nombre = self.nombre_entry.get()
        descripcion = self.desc_entry.get()
        
        response = requests.put(f"{API_URL}/ping/{record_id}", json={"nombre": nombre, "descripcion": descripcion})
        if response.status_code == 200:
            messagebox.showinfo("Éxito", "Registro actualizado correctamente")
            self.edit_window.destroy()
            self.get_records()
        else:
            messagebox.showerror("Error", "Error al actualizar el registro")

    def delete_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            record_id = item['values'][0]
            
            response = requests.delete(f"{API_URL}/ping/{record_id}")
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.get_records()
            else:
                messagebox.showerror("Error", "Error al eliminar el registro")
        else:
            messagebox.showerror("Error", "Seleccione un registro para eliminar")

    def logout(self):
        self.root.destroy()
        main()

def main_app():
    root = tk.Tk()
    app = ListApp(root)
    root.mainloop()

def main():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
