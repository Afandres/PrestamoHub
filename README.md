# 📦 GESPRÉ - Sistema de Gestión de Préstamo de Elementos

**Versión:** 3.0.0  
**Fecha:** 2024  
**Estado:** ✅ En producción

---

## 📋 Descripción

**GESPRÉ** (Gestión de Préstamo de Elementos) es un sistema de escritorio desarrollado en Python que permite administrar el préstamo y devolución de elementos organizados por categorías. El sistema está diseñado para pequeñas y medianas organizaciones que necesitan controlar el inventario de sus recursos.

### 🎯 Características Principales

- 📊 **Gestión de Inventario**: Registro, edición y eliminación de elementos
- 📂 **Organización por Categorías**: Deportes, Informática, Audiovisuales, Herramientas
- 🔄 **Préstamos y Devoluciones**: Control completo de movimientos
- 👥 **Gestión de Usuarios**: Registro y administración de usuarios
- 📈 **Estadísticas en Tiempo Real**: Visualización de disponibilidad
- 📋 **Historial de Préstamos**: Seguimiento completo de cada elemento
- 💾 **Persistencia Automática**: Guardado automático en JSON
- 🖥️ **Interfaz Intuitiva**: Diseño amigable con Tkinter

---

## 🏗️ Arquitectura del Sistema

El sistema sigue una arquitectura **MVC** (Modelo-Vista-Controlador) simplificada:



### 📐 Capas del Sistema

| Capa | Archivo | Responsabilidad |
|------|---------|-----------------|
| **Modelo** | `modelo.py` | Lógica de negocio, gestión de datos, validaciones |
| **Controlador** | `controlador.py` | Conecta modelo con vista, maneja eventos del usuario |
| **Vista** | `vista.py` | Interfaz gráfica, captura de eventos, visualización |
| **Persistencia** | `datos.json` | Almacenamiento de datos en formato JSON |

---

## 🚀 Instalación y Ejecución

### Requisitos Previos

- Python 3.8 o superior
- Tkinter (incluido en Python por defecto)

### Instalación

1. **Clonar o descargar el repositorio**

```bash
git clone https://github.com/tu-usuario/sistema-prestamos.git
cd sistema-prestamos

# Ejecutar el sistema
python main.py