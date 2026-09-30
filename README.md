# 🎬 CINEAPP - Sistema de Gestión de Cine

**INACAP** - Programación Orientada a Objetos (TI3V21) - Sumativa N°2  
**Desarrolladores**: Luis Lugo & Equipo  

---

## 📋 Descripción del Proyecto
CINEAPP es un sistema de gestión para un complejo de cines desarrollado en **Python** aplicando los principios de la **Programación Orientada a Objetos (POO)**. Permite administrar la venta de entradas, funciones (2D, 3D, VIP), productos de dulcería (nacionales e importados con cotización de moneda extranjera) y control de aforo y restricciones por edad.

---

## 🏗️ Arquitectura y Estructura del Código

El proyecto sigue una arquitectura modular donde cada clase se encuentra desacoplada en su propio archivo dentro del paquete `model/`:

```text
CINEAPP/
├── main.py                     # Script principal de demostración y pruebas
├── README.md                   # Documentación del proyecto
└── model/                      # Módulo con las clases del sistema
    ├── __init__.py             # Exposición centralizada de módulos
    ├── cliente.py              # Clase Cliente con validación de datos
    ├── empleado.py             # Clase base abstracta Empleado
    ├── boletero.py             # Subclase Boletero (emisión de entradas y validación de reglas)
    ├── encargado_dulceria.py   # Subclase EncargadoDulceria (gestión de ventas de dulcería)
    ├── pelicula.py             # Clase Película (clasificación y restricciones)
    ├── funcion.py              # Clase base Función (gestión de aforo y precios)
    ├── funcion_2d.py           # Subtipo Función 2D
    ├── funcion_3d.py           # Subtipo Función 3D (con recargo)
    ├── funcion_vip.py          # Subtipo Función VIP (con recargo)
    ├── item_vendible.py        # Interfaz/Base de ítems vendibles
    ├── entrada.py              # Subtipo Entrada para cine
    ├── producto_dulceria.py    # Clase base para productos comestibles/snacks
    ├── producto_nacional.py    # Producto en CLP
    ├── producto_importado.py   # Producto en USD conversible mediante tasa
    ├── cotizacion_dolar.py     # Clase de soporte para tasa de cambio en vivo/dinámica
    ├── venta.py                # Clase Venta (transacción y comprobante)
    ├── detalle_venta.py        # Detalle de ítem y cantidad
    ├── edad_insuficiente_error.py # Excepción personalizada (Regla de negocio: restricción edad)
    └── sala_llena_error.py     # Excepción personalizada (Regla de negocio: aforo lleno)
```

---

## ✨ Características y Principios POO Aplicados

1. **Polimorfismo**:
   - `calcular_precio()` en las funciones `Funcion2D`, `Funcion3D` y `FuncionVIP`.
2. **Encapsulamiento y Validaciones Defensivas**:
   - Validación de edad de cliente, capacidad de sala y stock de productos en los setters.
3. **Abstracción**:
   - Clase abstracta `Empleado` que obliga la implementación del método `get_rol()`.
4. **Reglas de Negocio con Excepciones Propias**:
   - `EdadInsuficienteError`: Bloquea la venta de funciones con clasificación inapropiada para menores.
   - `SalaLlenaError`: Evita sobreventas si la capacidad máxima de la sala fue alcanzada.
5. **Conversión Dinámica de Monedas**:
   - `CotizacionDolar` actualiza automáticamente el costo final en CLP de productos importados.

---

## 🚀 Cómo Ejecutar

Requiere **Python 3.8+** (sin librerías externas adicionales).

```bash
# Ejecutar la demostración de funcionalidades y reglas del negocio
python main.py
```

