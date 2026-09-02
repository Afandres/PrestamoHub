"""
CONTROLADOR - Conecta el modelo con la vista
Maneja las acciones del usuario y actualiza la vista
"""

from modelo import Sistema, Elemento


class Controlador:
    """Controlador que maneja la lógica de la aplicación."""
    
    def __init__(self, vista):
        self.vista = vista
        self.sistema = Sistema()
        
        # Conectar señales de la vista
        self.vista.on_actualizar = self.actualizar
        self.vista.on_prestar = self.prestar
        self.vista.on_devolver = self.devolver
        self.vista.on_agregar = self.agregar
        self.vista.on_eliminar = self.eliminar
        self.vista.on_buscar = self.buscar
        self.vista.on_editar = self.editar
        self.vista.on_reporte = self.reporte
        self.vista.on_estadisticas = self.estadisticas
        self.vista.on_agregar_usuario = self.agregar_usuario
        self.vista.on_eliminar_usuario = self.eliminar_usuario
    
    def actualizar(self):
        """Obtiene los datos actualizados del modelo."""
        return {
            'elementos': self.sistema.elementos,
            'estadisticas': self.sistema.estadisticas(),
            'usuarios': self.sistema.usuarios,
            'categorias': list(self.sistema.categorias.keys()),
            'nombres_usuarios': self.sistema.obtener_nombres_usuarios()
        }
    
    def prestar(self, codigo, nombre_usuario):
        """Realiza un préstamo usando el nombre del usuario."""
        return self.sistema.prestar(codigo, nombre_usuario)
    
    def devolver(self, codigo):
        """Realiza una devolución."""
        return self.sistema.devolver(codigo)
    
    def agregar(self, datos):
        """Agrega un nuevo elemento."""
        e = Elemento(
            datos['codigo'],
            datos['nombre'],
            datos['categoria'],
            datos.get('descripcion', ''),
            datos.get('ubicacion', '')
        )
        return self.sistema.agregar_elemento(e)
    
    def eliminar(self, codigo):
        """Elimina un elemento."""
        return self.sistema.eliminar_elemento(codigo)
    
    def buscar(self, texto):
        """Busca elementos por nombre."""
        return self.sistema.buscar_por_nombre(texto)
    
    def editar(self, codigo, datos):
        """Edita un elemento existente."""
        e = self.sistema.buscar_elemento(codigo)
        if not e:
            return False, "Elemento no encontrado"
        
        cat_anterior = e.categoria
        
        e.nombre = datos.get('nombre', e.nombre)
        e.categoria = datos.get('categoria', e.categoria)
        e.descripcion = datos.get('descripcion', e.descripcion)
        e.ubicacion = datos.get('ubicacion', e.ubicacion)
        
        if cat_anterior != e.categoria:
            if cat_anterior in self.sistema.categorias:
                self.sistema.categorias[cat_anterior] = [
                    x for x in self.sistema.categorias[cat_anterior] 
                    if x.codigo != codigo
                ]
            if e.categoria not in self.sistema.categorias:
                self.sistema.categorias[e.categoria] = []
            self.sistema.categorias[e.categoria].append(e)
        
        self.sistema.guardar_datos()
        return True, "Elemento actualizado"
    
    def reporte(self):
        """Genera un reporte."""
        return self.sistema.reporte()
    
    def estadisticas(self):
        """Obtiene estadísticas."""
        return self.sistema.estadisticas()
    
    def agregar_usuario(self, nombre, email, telefono):
        """Agrega un nuevo usuario."""
        return self.sistema.agregar_usuario(nombre, email, telefono)
    
    def eliminar_usuario(self, nombre):
        """Elimina un usuario."""
        return self.sistema.eliminar_usuario(nombre)