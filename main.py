"""
PUNTO DE ENTRADA - Main
Conecta el controlador con la vista y ejecuta la aplicación
"""

import tkinter as tk
from vista import Vista
from controlador import Controlador


def main():
    """Punto de entrada de la aplicación."""
    
    # Crear la ventana principal
    root = tk.Tk()
    
    # Crear la vista
    vista = Vista(root)
    
    # Crear el controlador y pasarle la vista
    controlador = Controlador(vista)
    
    # Guardar referencia al controlador en la vista (para acceso directo)
    vista.controlador = controlador
    
    # Ejecutar la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()