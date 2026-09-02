"""
MODELO - Lógica de negocio y datos del sistema
Contiene las clases Elemento, Categoria, Usuario y Sistema
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class Elemento:
    """Representa un elemento que puede ser prestado."""
    
    def __init__(self, codigo, nombre, categoria, descripcion="", ubicacion=""):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.ubicacion = ubicacion
        self.disponible = True
        self.usuario_actual = None
        self.fecha_prestamo = None
        self.historial = []
    
    def prestar(self, usuario):
        """Realiza el préstamo del elemento."""
        if not self.disponible:
            return False, f"'{self.nombre}' ya está prestado"
        
        self.disponible = False
        self.usuario_actual = usuario
        self.fecha_prestamo = datetime.now()
        
        self.historial.append({
            'fecha': self.fecha_prestamo.strftime("%d/%m/%Y %H:%M"),
            'accion': 'PRESTAMO',
            'usuario': usuario
        })
        
        return True, "Préstamo exitoso"
    
    def devolver(self):
        """Registra la devolución del elemento."""
        if self.disponible:
            return False, f"'{self.nombre}' ya está disponible"
        
        self.disponible = True
        self.historial.append({
            'fecha': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'accion': 'DEVOLUCION',
            'usuario': self.usuario_actual
        })
        
        self.usuario_actual = None
        self.fecha_prestamo = None
        
        return True, "Devolución exitosa"
    
    def esta_disponible(self):
        return self.disponible
    
    def a_dict(self):
        """Convierte a diccionario para guardar."""
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'descripcion': self.descripcion,
            'ubicacion': self.ubicacion,
            'disponible': self.disponible,
            'usuario_actual': self.usuario_actual,
            'fecha_prestamo': self.fecha_prestamo.isoformat() if self.fecha_prestamo else None,
            'historial': self.historial
        }
    
    @classmethod
    def desde_dict(cls, datos):
        """Crea un elemento desde un diccionario."""
        e = cls(
            datos['codigo'],
            datos['nombre'],
            datos['categoria'],
            datos.get('descripcion', ''),
            datos.get('ubicacion', '')
        )
        e.disponible = datos.get('disponible', True)
        e.usuario_actual = datos.get('usuario_actual')
        e.historial = datos.get('historial', [])
        return e
    
    def info(self):
        """Información para mostrar."""
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'estado': 'Disponible' if self.disponible else 'Prestado',
            'usuario': self.usuario_actual or '-',
            'ubicacion': self.ubicacion,
            'total_prestamos': len(self.historial)
        }


class Sistema:
    """Sistema principal que maneja todo."""
    
    ARCHIVO = "datos.json"
    
    def __init__(self):
        self.elementos = []
        self.usuarios = []
        self.categorias = {}
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga los datos desde el archivo JSON."""
        if os.path.exists(self.ARCHIVO):
            try:
                with open(self.ARCHIVO, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    
                # Cargar elementos
                for info in datos.get('elementos', []):
                    e = Elemento.desde_dict(info)
                    self.elementos.append(e)
                    
                    # Agregar a categoría
                    if e.categoria not in self.categorias:
                        self.categorias[e.categoria] = []
                    self.categorias[e.categoria].append(e)
                
                # Cargar usuarios
                self.usuarios = datos.get('usuarios', [])
                return
            except:
                pass
        
        # Datos de ejemplo si no hay archivo
        self._cargar_ejemplos()
    
    def guardar_datos(self):
        """Guarda los datos en el archivo JSON."""
        datos = {
            'elementos': [e.a_dict() for e in self.elementos],
            'usuarios': self.usuarios
        }
        try:
            with open(self.ARCHIVO, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def _cargar_ejemplos(self):
        """Carga elementos y usuarios de ejemplo."""
        # Categorías
        categorias = ["Deportes", "Informática", "Audiovisuales", "Herramientas"]
        for cat in categorias:
            self.categorias[cat] = []
        
        # Elementos
        ejemplos = [
            ("EL-001", "Balón de fútbol", "Deportes", "Talla 5", "Bodega"),
            ("EL-002", "Balón de baloncesto", "Deportes", "Talla 7", "Bodega"),
            ("EL-003", "Computador portátil", "Informática", "16GB RAM", "Oficina"),
            ("EL-004", "Mouse inalámbrico", "Informática", "Logitech", "Oficina"),
            ("EL-005", "Teclado mecánico", "Informática", "RGB", "Oficina"),
            ("EL-006", "Videobeam", "Audiovisuales", "Epson EB-2000", "Sala A"),
            ("EL-007", "Cámara réflex", "Audiovisuales", "Canon EOS", "Estudio"),
            ("EL-008", "Trípode", "Audiovisuales", "Profesional", "Estudio"),
            ("EL-009", "Taladro", "Herramientas", "Bosch percutor", "Taller"),
            ("EL-010", "Multímetro", "Herramientas", "Fluke 117", "Taller")
        ]
        
        for cod, nom, cat, desc, ub in ejemplos:
            e = Elemento(cod, nom, cat, desc, ub)
            self.elementos.append(e)
            self.categorias[cat].append(e)
        
        # Usuarios
        self.usuarios = [
            {"nombre": "Juan Pérez", "email": "juan@mail.com", "telefono": "555-0101"},
            {"nombre": "María García", "email": "maria@mail.com", "telefono": "555-0102"},
            {"nombre": "Carlos López", "email": "carlos@mail.com", "telefono": "555-0103"}
        ]
        
        self.guardar_datos()
    
    # ===== OPERACIONES CON USUARIOS =====
    
    def agregar_usuario(self, nombre, email="", telefono=""):
        """Agrega un nuevo usuario."""
        for u in self.usuarios:
            if u['nombre'].lower() == nombre.lower():
                return False, "Ya existe un usuario con ese nombre"
        
        self.usuarios.append({
            'nombre': nombre,
            'email': email,
            'telefono': telefono
        })
        self.guardar_datos()
        return True, "Usuario agregado"
    
    def eliminar_usuario(self, nombre):
        """Elimina un usuario por su nombre."""
        for i, u in enumerate(self.usuarios):
            if u['nombre'].lower() == nombre.lower():
                # Verificar que no tenga préstamos activos
                for e in self.elementos:
                    if e.usuario_actual == u['nombre'] and not e.disponible:
                        return False, "El usuario tiene préstamos activos"
                
                self.usuarios.pop(i)
                self.guardar_datos()
                return True, "Usuario eliminado"
        
        return False, "Usuario no encontrado"
    
    def buscar_usuario(self, nombre):
        """Busca un usuario por nombre."""
        for u in self.usuarios:
            if u['nombre'].lower() == nombre.lower():
                return u
        return None
    
    def obtener_nombres_usuarios(self):
        """Obtiene solo los nombres de los usuarios."""
        return [u['nombre'] for u in self.usuarios]
    
    # ===== OPERACIONES CON ELEMENTOS =====
    
    def buscar_elemento(self, codigo):
        for e in self.elementos:
            if e.codigo == codigo:
                return e
        return None
    
    def buscar_por_nombre(self, texto):
        texto = texto.lower()
        return [e for e in self.elementos if texto in e.nombre.lower()]
    
    def agregar_elemento(self, elemento):
        if self.buscar_elemento(elemento.codigo):
            return False
        
        self.elementos.append(elemento)
        if elemento.categoria not in self.categorias:
            self.categorias[elemento.categoria] = []
        self.categorias[elemento.categoria].append(elemento)
        self.guardar_datos()
        return True
    
    def eliminar_elemento(self, codigo):
        e = self.buscar_elemento(codigo)
        if not e or not e.disponible:
            return False
        
        self.elementos = [x for x in self.elementos if x.codigo != codigo]
        if e.categoria in self.categorias:
            self.categorias[e.categoria] = [x for x in self.categorias[e.categoria] 
                                            if x.codigo != codigo]
        self.guardar_datos()
        return True
    
    def prestar(self, codigo, nombre_usuario):
        """Realiza un préstamo usando el nombre del usuario."""
        e = self.buscar_elemento(codigo)
        if not e:
            return False, "Elemento no encontrado"
        
        usuario = self.buscar_usuario(nombre_usuario)
        if not usuario:
            return False, f"Usuario '{nombre_usuario}' no encontrado"
        
        nombre = usuario['nombre']
        resultado, mensaje = e.prestar(nombre)
        
        if resultado:
            self.guardar_datos()
        
        return resultado, mensaje
    
    def devolver(self, codigo):
        e = self.buscar_elemento(codigo)
        if not e:
            return False, "Elemento no encontrado"
        
        resultado, mensaje = e.devolver()
        if resultado:
            self.guardar_datos()
        
        return resultado, mensaje
    
    def disponibles(self):
        return [e for e in self.elementos if e.disponible]
    
    def prestados(self):
        return [e for e in self.elementos if not e.disponible]
    
    def estadisticas(self):
        total = len(self.elementos)
        disp = len(self.disponibles())
        prest = len(self.prestados())
        
        stats_cat = {}
        for cat, elems in self.categorias.items():
            stats_cat[cat] = {
                'total': len(elems),
                'disponibles': len([e for e in elems if e.disponible]),
                'prestados': len([e for e in elems if not e.disponible])
            }
        
        return {
            'total': total,
            'disponibles': disp,
            'prestados': prest,
            'categorias': len(self.categorias),
            'usuarios': len(self.usuarios),
            'por_categoria': stats_cat
        }
    
    def reporte(self):
        """Genera un reporte en texto."""
        stats = self.estadisticas()
        texto = "="*50 + "\n"
        texto += " SISTEMA DE PRÉSTAMOS\n"
        texto += "="*50 + "\n\n"
        texto += f"Total elementos: {stats['total']}\n"
        texto += f"Disponibles: {stats['disponibles']}\n"
        texto += f"Prestados: {stats['prestados']}\n"
        texto += f"Categorías: {stats['categorias']}\n"
        texto += f"Usuarios: {stats['usuarios']}\n\n"
        
        texto += "USUARIOS REGISTRADOS:\n"
        texto += "-"*30 + "\n"
        for u in self.usuarios:
            texto += f"  • {u['nombre']} - {u.get('email', '')} - {u.get('telefono', '')}\n"
        
        texto += "\n" + "="*50 + "\n"
        return texto