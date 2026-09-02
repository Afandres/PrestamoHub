"""
VISTA - Interfaz gráfica de usuario (Tkinter)
Muestra los datos y captura las acciones del usuario
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext


class Vista:
    """Ventana principal de la aplicación."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PrestamoHub - Préstamo de Elementos")
        self.root.geometry("1100x650")
        self.root.resizable(True, True)
        
        # Callbacks
        self.on_actualizar = None
        self.on_prestar = None
        self.on_devolver = None
        self.on_agregar = None
        self.on_eliminar = None
        self.on_buscar = None
        self.on_editar = None
        self.on_reporte = None
        self.on_estadisticas = None
        self.on_agregar_usuario = None
        self.on_eliminar_usuario = None
        
        # Variables
        self.filtro_estado = tk.StringVar(value="Todos")
        self.busqueda_texto = tk.StringVar()
        
        # Construir interfaz
        self._crear_menu()
        self._crear_panel_principal()
        self._crear_barra_estado()
        
        # Cargar datos iniciales
        self.root.after(100, self.actualizar)
    
    def _crear_menu(self):
        """Barra de menú."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nuevo Elemento", command=self._nuevo_elemento)
        menu_archivo.add_command(label="Nuevo Usuario", command=self._nuevo_usuario)
        menu_archivo.add_command(label="Ver Usuarios", command=self._ver_usuarios)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        
        # Reportes
        menu_reportes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reportes", menu=menu_reportes)
        menu_reportes.add_command(label="Ver Reporte", command=self._ver_reporte)
        menu_reportes.add_command(label="Estadísticas", command=self._ver_estadisticas)
    
    def _crear_panel_principal(self):
        """Panel principal con tabla y estadísticas."""
        
        # Título
        frame_titulo = tk.Frame(self.root, bg='#2c3e50', height=55)
        frame_titulo.pack(fill=tk.X)
        tk.Label(
            frame_titulo,
            text="🏦 PrestamoHub - Gestión de Préstamo de Elementos",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        ).pack(pady=10)
        
        # Panel principal
        panel = tk.Frame(self.root)
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ----- IZQUIERDA: Tabla -----
        frame_tabla = tk.Frame(panel)
        frame_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Barra de herramientas
        toolbar = tk.Frame(frame_tabla)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        botones = [
            ("➕ Nuevo", self._nuevo_elemento, '#27ae60'),
            ("✏️ Editar", self._editar_elemento, '#3498db'),
            ("🗑️ Eliminar", self._eliminar_elemento, '#e74c3c'),
            ("🔍 Buscar", self._buscar, '#f39c12')
        ]
        
        for texto, cmd, color in botones:
            tk.Button(
                toolbar,
                text=texto,
                command=cmd,
                bg=color,
                fg='white',
                font=('Arial', 9, 'bold')
            ).pack(side=tk.LEFT, padx=2)
        
        # Filtros
        tk.Label(toolbar, text="Filtrar:").pack(side=tk.LEFT, padx=(15, 5))
        
        self.combo_filtro = ttk.Combobox(
            toolbar,
            textvariable=self.filtro_estado,
            values=["Todos", "Disponibles", "Prestados"],
            width=12,
            state='readonly'
        )
        self.combo_filtro.pack(side=tk.LEFT)
        self.combo_filtro.set("Todos")
        self.combo_filtro.bind('<<ComboboxSelected>>', lambda e: self.actualizar())
        
        # Campo de búsqueda
        tk.Label(toolbar, text="Buscar:").pack(side=tk.LEFT, padx=(15, 5))
        entry_busqueda = tk.Entry(toolbar, textvariable=self.busqueda_texto, width=20)
        entry_busqueda.pack(side=tk.LEFT)
        entry_busqueda.bind('<KeyRelease>', lambda e: self.actualizar())
        
        # Tabla
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=('codigo', 'nombre', 'categoria', 'estado', 'usuario', 'ubicacion'),
            show='headings',
            height=18
        )
        
        self.tree.heading('codigo', text='Código')
        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('categoria', text='Categoría')
        self.tree.heading('estado', text='Estado')
        self.tree.heading('usuario', text='Usuario')
        self.tree.heading('ubicacion', text='Ubicación')
        
        self.tree.column('codigo', width=80)
        self.tree.column('nombre', width=180)
        self.tree.column('categoria', width=120)
        self.tree.column('estado', width=110)
        self.tree.column('usuario', width=130)
        self.tree.column('ubicacion', width=120)
        
        scroll = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Doble click para ver detalles
        self.tree.bind('<Double-Button-1>', self._ver_detalles)
        
        # ----- DERECHA: Estadísticas -----
        frame_derecho = tk.Frame(panel, width=280)
        frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        frame_derecho.pack_propagate(False)
        
        # Panel de estadísticas
        self.frame_stats = tk.LabelFrame(frame_derecho, text="📊 Estadísticas", font=('Arial', 11, 'bold'))
        self.frame_stats.pack(fill=tk.BOTH, expand=True)
        
        self.label_stats = tk.Label(
            self.frame_stats,
            text="Cargando...",
            font=('Arial', 10),
            justify=tk.LEFT,
            anchor='nw'
        )
        self.label_stats.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Botones de acciones rápidas
        frame_acciones = tk.LabelFrame(frame_derecho, text="⚡ Acciones", font=('Arial', 11, 'bold'))
        frame_acciones.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(
            frame_acciones,
            text="📤 Prestar",
            command=self._prestar,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            height=2
        ).pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(
            frame_acciones,
            text="📥 Devolver",
            command=self._devolver,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            height=2
        ).pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(
            frame_acciones,
            text="📋 Reporte",
            command=self._ver_reporte,
            bg='#f39c12',
            fg='white',
            font=('Arial', 10, 'bold'),
            height=2
        ).pack(fill=tk.X, padx=10, pady=5)
    
    def _crear_barra_estado(self):
        """Barra de estado en la parte inferior."""
        self.status = tk.Label(
            self.root,
            text="Listo",
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=('Arial', 9)
        )
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
    
    # ========== MÉTODOS PÚBLICOS ==========
    
    def actualizar(self):
        """Actualiza la tabla y estadísticas desde el controlador."""
        if not self.on_actualizar:
            return
        
        datos = self.on_actualizar()
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener elementos según filtro
        elementos = datos['elementos']
        filtro = self.filtro_estado.get()
        busqueda = self.busqueda_texto.get().lower()
        
        if filtro == "Disponibles":
            elementos = [e for e in elementos if e.disponible]
        elif filtro == "Prestados":
            elementos = [e for e in elementos if not e.disponible]
        
        if busqueda:
            elementos = [e for e in elementos if busqueda in e.nombre.lower()]
        
        # Insertar en tabla
        for e in elementos:
            estado = "✅ Disponible" if e.disponible else "🔒 Prestado"
            usuario = e.usuario_actual or "-"
            
            self.tree.insert('', 'end', values=(
                e.codigo,
                e.nombre,
                e.categoria,
                estado,
                usuario,
                e.ubicacion
            ))
        
        self.status.config(text=f"Total: {len(elementos)} elementos")
        
        # Actualizar estadísticas
        stats = datos['estadisticas']
        texto = f"""
📦 Total: {stats['total']}
✅ Disponibles: {stats['disponibles']}
🔒 Prestados: {stats['prestados']}
👤 Usuarios: {stats['usuarios']}
📁 Categorías: {stats['categorias']}

📂 Por categoría:
"""
        for cat, d in stats['por_categoria'].items():
            texto += f"\n  {cat}: {d['disponibles']} disp / {d['prestados']} prest"
        
        self.label_stats.config(text=texto)
    
    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        """Muestra un mensaje al usuario."""
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)
    
    def obtener_seleccion(self):
        """Obtiene el código del elemento seleccionado en la tabla."""
        seleccion = self.tree.selection()
        if not seleccion:
            return None
        return self.tree.item(seleccion[0])['values'][0]
    
    # ========== USUARIOS ==========
    
    def _ver_usuarios(self):
        """Muestra la lista de usuarios."""
        if not self.on_actualizar:
            return
        
        datos = self.on_actualizar()
        usuarios = datos['usuarios']
        
        if not usuarios:
            messagebox.showinfo("Usuarios", "No hay usuarios registrados")
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Lista de Usuarios")
        ventana.geometry("500x400")
        ventana.transient(self.root)
        
        tree = ttk.Treeview(
            ventana,
            columns=('nombre', 'email', 'telefono'),
            show='headings',
            height=15
        )
        
        tree.heading('nombre', text='Nombre')
        tree.heading('email', text='Email')
        tree.heading('telefono', text='Teléfono')
        
        tree.column('nombre', width=180)
        tree.column('email', width=180)
        tree.column('telefono', width=120)
        
        scroll = ttk.Scrollbar(ventana, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        for u in usuarios:
            tree.insert('', 'end', values=(
                u['nombre'],
                u.get('email', ''),
                u.get('telefono', '')
            ))
        
        # Botón para eliminar usuario
        def eliminar_usuario():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un usuario")
                return
            
            nombre = tree.item(seleccion[0])['values'][0]
            
            if messagebox.askyesno("Confirmar", f"¿Eliminar al usuario '{nombre}'?"):
                if self.on_eliminar_usuario:
                    exito, msg = self.on_eliminar_usuario(nombre)
                    if exito:
                        messagebox.showinfo("Éxito", msg)
                        ventana.destroy()
                        self.actualizar()
                    else:
                        messagebox.showerror("Error", msg)
        
        tk.Button(
            ventana,
            text="🗑️ Eliminar Usuario",
            command=eliminar_usuario,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=20
        ).pack(pady=10)
        
        tk.Button(
            ventana,
            text="Cerrar",
            command=ventana.destroy,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(pady=5)
    
    def _nuevo_usuario(self):
        """Agrega un nuevo usuario (sin ID)."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Usuario")
        dialog.geometry("400x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        campos = [
            ("Nombre:", "nombre"),
            ("Email:", "email"),
            ("Teléfono:", "telefono")
        ]
        
        entries = {}
        
        for i, (label, key) in enumerate(campos):
            tk.Label(dialog, text=label, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, padx=10, pady=8, sticky='w'
            )
            entry = tk.Entry(dialog, width=35)
            entry.grid(row=i, column=1, padx=10, pady=8)
            entries[key] = entry
        
        def guardar():
            nombre = entries['nombre'].get().strip()
            email = entries['email'].get().strip()
            telefono = entries['telefono'].get().strip()
            
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            if self.on_agregar_usuario:
                exito, msg = self.on_agregar_usuario(nombre, email, telefono)
                if exito:
                    messagebox.showinfo("Éxito", msg)
                    dialog.destroy()
                    self.actualizar()
                else:
                    messagebox.showerror("Error", msg)
        
        frame_btns = tk.Frame(dialog)
        frame_btns.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        tk.Button(
            frame_btns,
            text="Guardar",
            command=guardar,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_btns,
            text="Cancelar",
            command=dialog.destroy,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    # ========== ELEMENTOS ==========
    
    def _nuevo_elemento(self):
        """Abre diálogo para nuevo elemento."""
        if not self.on_agregar:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Elemento")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        campos = [
            ("Código:", "codigo"),
            ("Nombre:", "nombre"),
            ("Categoría:", "categoria"),
            ("Descripción:", "descripcion"),
            ("Ubicación:", "ubicacion")
        ]
        
        entries = {}
        
        for i, (label, key) in enumerate(campos):
            tk.Label(dialog, text=label, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, padx=10, pady=5, sticky='w'
            )
            
            if key == "categoria":
                datos = self.on_actualizar()
                entry = ttk.Combobox(dialog, values=datos['categorias'], width=35)
            elif key == "descripcion":
                entry = tk.Text(dialog, width=35, height=3)
            else:
                entry = tk.Entry(dialog, width=35)
            
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[key] = entry
        
        def guardar():
            try:
                datos = {
                    'codigo': entries['codigo'].get().strip(),
                    'nombre': entries['nombre'].get().strip(),
                    'categoria': entries['categoria'].get().strip(),
                    'descripcion': entries['descripcion'].get("1.0", tk.END).strip(),
                    'ubicacion': entries['ubicacion'].get().strip()
                }
                
                if not datos['codigo'] or not datos['nombre'] or not datos['categoria']:
                    messagebox.showerror("Error", "Código, Nombre y Categoría son obligatorios")
                    return
                
                exito, msg = self.on_agregar(datos)
                if exito:
                    messagebox.showinfo("Éxito", "Elemento agregado")
                    dialog.destroy()
                    self.actualizar()
                else:
                    messagebox.showerror("Error", msg)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        frame_btns = tk.Frame(dialog)
        frame_btns.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        tk.Button(
            frame_btns,
            text="Guardar",
            command=guardar,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_btns,
            text="Cancelar",
            command=dialog.destroy,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    def _editar_elemento(self):
        """Edita el elemento seleccionado."""
        codigo = self.obtener_seleccion()
        if not codigo:
            messagebox.showwarning("Advertencia", "Seleccione un elemento")
            return
        
        if not self.on_actualizar:
            return
        
        datos = self.on_actualizar()
        elemento = None
        for e in datos['elementos']:
            if e.codigo == codigo:
                elemento = e
                break
        
        if not elemento:
            messagebox.showerror("Error", "Elemento no encontrado")
            return
        
        if not elemento.disponible:
            messagebox.showwarning("Advertencia", "No se puede editar un elemento prestado")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Elemento")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        campos = [
            ("Código:", "codigo", elemento.codigo),
            ("Nombre:", "nombre", elemento.nombre),
            ("Categoría:", "categoria", elemento.categoria),
            ("Descripción:", "descripcion", elemento.descripcion),
            ("Ubicación:", "ubicacion", elemento.ubicacion)
        ]
        
        entries = {}
        
        for i, (label, key, valor) in enumerate(campos):
            tk.Label(dialog, text=label, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, padx=10, pady=5, sticky='w'
            )
            
            if key == "categoria":
                entry = ttk.Combobox(dialog, values=datos['categorias'], width=35)
                entry.set(valor)
            elif key == "codigo":
                entry = tk.Entry(dialog, width=35)
                entry.insert(0, valor)
                entry.config(state='readonly')
            elif key == "descripcion":
                entry = tk.Text(dialog, width=35, height=3)
                entry.insert("1.0", valor)
            else:
                entry = tk.Entry(dialog, width=35)
                entry.insert(0, valor)
            
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[key] = entry
        
        def guardar():
            try:
                datos_nuevos = {
                    'nombre': entries['nombre'].get().strip(),
                    'categoria': entries['categoria'].get().strip(),
                    'descripcion': entries['descripcion'].get("1.0", tk.END).strip(),
                    'ubicacion': entries['ubicacion'].get().strip()
                }
                
                if not datos_nuevos['nombre'] or not datos_nuevos['categoria']:
                    messagebox.showerror("Error", "Nombre y Categoría son obligatorios")
                    return
                
                if self.on_editar:
                    exito, msg = self.on_editar(codigo, datos_nuevos)
                    if exito:
                        messagebox.showinfo("Éxito", "Elemento actualizado")
                        dialog.destroy()
                        self.actualizar()
                    else:
                        messagebox.showerror("Error", msg)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        frame_btns = tk.Frame(dialog)
        frame_btns.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        tk.Button(
            frame_btns,
            text="Guardar",
            command=guardar,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_btns,
            text="Cancelar",
            command=dialog.destroy,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    def _eliminar_elemento(self):
        """Elimina el elemento seleccionado."""
        codigo = self.obtener_seleccion()
        if not codigo:
            messagebox.showwarning("Advertencia", "Seleccione un elemento")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar este elemento?"):
            if self.on_eliminar:
                exito = self.on_eliminar(codigo)
                if exito:
                    messagebox.showinfo("Éxito", "Elemento eliminado")
                    self.actualizar()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar (¿está prestado?)")
    
    def _buscar(self):
        """Busca un elemento por código."""
        codigo = simpledialog.askstring("Buscar", "Ingrese el código:")
        if codigo:
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == codigo:
                    self.tree.selection_set(item)
                    self.tree.see(item)
                    return
            messagebox.showinfo("No encontrado", f"No se encontró el elemento {codigo}")
    
    # ========== PRÉSTAMOS Y DEVOLUCIONES ==========
    
    def _prestar(self):
        """Realiza un préstamo (usa nombre de usuario)."""
        if not self.on_prestar or not self.on_actualizar:
            return
        
        codigo = self.obtener_seleccion()
        if not codigo:
            messagebox.showwarning("Advertencia", "Seleccione un elemento")
            return
        
        datos = self.on_actualizar()
        elemento = None
        for e in datos['elementos']:
            if e.codigo == codigo:
                elemento = e
                break
        
        if not elemento or not elemento.disponible:
            messagebox.showwarning("Advertencia", "El elemento no está disponible")
            return
        
        if not datos['usuarios']:
            messagebox.showwarning("Advertencia", "No hay usuarios registrados")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Realizar Préstamo")
        dialog.geometry("400x180")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Elemento: {elemento.nombre}", font=('Arial', 11, 'bold')).pack(pady=10)
        tk.Label(dialog, text="Seleccione el usuario:").pack()
        
        nombres_usuarios = [u['nombre'] for u in datos['usuarios']]
        
        combo = ttk.Combobox(
            dialog,
            values=nombres_usuarios,
            width=40,
            state='readonly'
        )
        combo.pack(pady=5)
        
        def realizar():
            nombre_usuario = combo.get()
            if not nombre_usuario:
                messagebox.showerror("Error", "Seleccione un usuario")
                return
            
            exito, msg = self.on_prestar(codigo, nombre_usuario)
            
            if exito:
                messagebox.showinfo("Éxito", f"Préstamo realizado a {nombre_usuario}")
                dialog.destroy()
                self.actualizar()
            else:
                messagebox.showerror("Error", msg)
        
        tk.Button(
            dialog,
            text="Prestar",
            command=realizar,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(pady=10)
    
    def _devolver(self):
        """Realiza una devolución."""
        if not self.on_devolver:
            return
        
        codigo = self.obtener_seleccion()
        if not codigo:
            messagebox.showwarning("Advertencia", "Seleccione un elemento")
            return
        
        datos = self.on_actualizar()
        elemento = None
        for e in datos['elementos']:
            if e.codigo == codigo:
                elemento = e
                break
        
        if not elemento or elemento.disponible:
            messagebox.showwarning("Advertencia", "El elemento no está prestado")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Devolver '{elemento.nombre}'?"):
            exito, msg = self.on_devolver(codigo)
            if exito:
                messagebox.showinfo("Éxito", "Devolución realizada")
                self.actualizar()
            else:
                messagebox.showerror("Error", msg)
    
    # ========== DETALLES ==========
    
    def _ver_detalles(self, event):
        """Muestra detalles del elemento al hacer doble clic."""
        codigo = self.obtener_seleccion()
        if not codigo:
            return
        
        if not self.on_actualizar:
            return
        
        datos = self.on_actualizar()
        elemento = None
        for e in datos['elementos']:
            if e.codigo == codigo:
                elemento = e
                break
        
        if not elemento:
            return
        
        info = elemento.info()
        
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Detalles - {elemento.nombre}")
        ventana.geometry("500x400")
        ventana.transient(self.root)
        
        texto = f"""
📋 DETALLES DEL ELEMENTO
{'='*40}

Código: {info['codigo']}
Nombre: {info['nombre']}
Categoría: {info['categoria']}
Estado: {info['estado']}
Usuario: {info['usuario']}
Ubicación: {info['ubicacion']}
Total préstamos: {info['total_prestamos']}

📜 HISTORIAL
{'='*40}
"""
        
        if elemento.historial:
            for i, reg in enumerate(elemento.historial[-5:], 1):
                texto += f"\n{i}. {reg['fecha']} - {reg['accion']} - {reg['usuario']}"
        else:
            texto += "\nSin historial"
        
        text_widget = tk.Text(ventana, wrap=tk.WORD, font=('Courier', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text_widget.insert('1.0', texto)
        text_widget.config(state=tk.DISABLED)
        
        tk.Button(
            ventana,
            text="Cerrar",
            command=ventana.destroy,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(pady=10)
    
    # ========== REPORTES ==========
    
    def _ver_reporte(self):
        """Muestra el reporte del sistema."""
        if not self.on_reporte:
            return
        
        reporte = self.on_reporte()
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Reporte del Sistema")
        ventana.geometry("600x500")
        ventana.transient(self.root)
        
        text_widget = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, font=('Courier', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert('1.0', reporte)
        text_widget.config(state=tk.DISABLED)
        
        tk.Button(
            ventana,
            text="Cerrar",
            command=ventana.destroy,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(pady=10)
    
    def _ver_estadisticas(self):
        """Muestra estadísticas detalladas."""
        if not self.on_estadisticas:
            return
        
        stats = self.on_estadisticas()
        
        texto = f"""
📊 ESTADÍSTICAS DEL SISTEMA
{'='*50}

📦 TOTALES
  Total elementos: {stats['total']}
  ✅ Disponibles: {stats['disponibles']}
  🔒 Prestados: {stats['prestados']}
  👤 Usuarios: {stats['usuarios']}
  📁 Categorías: {stats['categorias']}

📂 POR CATEGORÍA
{'='*50}
"""
        
        for cat, d in stats['por_categoria'].items():
            texto += f"\n{cat}:"
            texto += f"\n  Total: {d['total']}"
            texto += f"\n  ✅ Disponibles: {d['disponibles']}"
            texto += f"\n  🔒 Prestados: {d['prestados']}"
            if d['total'] > 0:
                pct = (d['disponibles'] / d['total']) * 100
                texto += f"\n  📈 Disponibilidad: {pct:.1f}%"
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Estadísticas del Sistema")
        ventana.geometry("500x500")
        ventana.transient(self.root)
        
        text_widget = tk.Text(ventana, wrap=tk.WORD, font=('Arial', 11))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text_widget.insert('1.0', texto)
        text_widget.config(state=tk.DISABLED)
        
        tk.Button(
            ventana,
            text="Cerrar",
            command=ventana.destroy,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(pady=10)