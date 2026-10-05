# 🎬 cineAPP - Sistema de Gestión de Cine Avanzado (POO + API REST)

**INACAP** - Programación Orientada a Objetos (TI3V21) - Evaluación Sumativa N°2  
**Desarrolladores**: Luis Lugo & Debora Sepulveda  

---

## 📋 Descripción del Proyecto
`cineAPP` es un sistema completo e interactivo de gestión para complejos de cine desarrollado en **Python 3** aplicando rigurosamente los principios de la **Programación Orientada a Objetos (POO)**.

El sistema permite gestionar todo el flujo de ingreso de clientes, consulta de cartelera en vivo mediante **API REST pública (TMDB)**, compra de entradas por sala/asiento (matriz 5x6), validación de restricciones de edad con acompaño adulto, beneficios de clientes registrados y atención virtual en dulcería.

---

## 🏗️ Arquitectura y Estructura del Código

El código está organizado siguiendo el estándar modular de una clase por archivo en el paquete `model/`:

```text
CINEAPPMAKETA/
├── main.py                     # Sistema Interactivo CLI principal
├── README.md                   # Documentación oficial del proyecto
└── model/                      # Paquete con las clases del sistema
    ├── __init__.py             # Exposición centralizada del módulo POO
    ├── cliente.py              # Clase Cliente con encapsulamiento defensivo
    ├── empleado.py             # Clase base abstracta Empleado (abc.ABC)
    ├── boletero.py             # Subclase Boletero (emisión de entradas y reglas de negocio)
    ├── encargado_dulceria.py   # Subclase EncargadoDulceria (atención y ventas de dulcería)
    ├── asistente_dulceria.py   # 🤖 Asistente Virtual Interactivo de Dulcería
    ├── pelicula.py             # Clase Película (clasificación y restricciones de edad)
    ├── servicio_cartelera_api.py # 🌐 Servicio API REST para películas en taquilla
    ├── sala.py                 # 🏛️ Clase Sala con mapa visual de 30 asientos (5x6) y formato
    ├── funcion.py              # Clase base abstracta Función
    ├── funcion_2d.py           # Subtipo Función 2D (con descuento para clientes registrados)
    ├── funcion_3d.py           # Subtipo Función 3D (con recargo de lentes)
    ├── funcion_vip.py          # Subtipo Función VIP (con recargo de confort)
    ├── item_vendible.py        # Interfaz base para ítems vendibles
    ├── entrada.py              # Subtipo Entrada para cine
    ├── producto_dulceria.py    # Clase base para productos comestibles/snacks
    ├── producto_nacional.py    # Producto nacional en CLP
    ├── producto_importado.py   # Producto importado en USD con conversión dinámica
    ├── cotizacion_dolar.py     # Clase de soporte para indicador de tasa de cambio
    ├── venta.py                # Clase Venta (transacción principal)
    ├── detalle_venta.py        # Detalle de ítem y cantidad (Composición)
    ├── edad_insuficiente_error.py # 🚫 Excepción del dominio (Regla de edad)
    └── sala_llena_error.py     # 🚫 Excepción del dominio (Regla de aforo)
```

---

## ✨ Principios POO y Características Implementadas

1. **Polimorfismo Real**:
   - `calcular_precio()` implementado de forma específica en `Funcion2D`, `Funcion3D` y `FuncionVIP`. Se invoca dinámicamente sin `if/isinstance`.

2. **Encapsulamiento y Validaciones Defensivas**:
   - Atributos privados (`_atributo`) expuestos con `@property` y `@setter`. Validaciones con `raise ValueError` para edades, precios y stock.

3. **Abstracción & Interfaces**:
   - Clases abstractas `Empleado`, `Funcion`, `ItemVendible` y `ProductoDulceria` con métodos abstractos obligatorios.

4. **Reglas de Negocio con Excepciones Propias**:
   - `EdadInsuficienteError`: Bloquea venta a menores si no cumplen la edad mínima requerida.
   - `SalaLlenaError`: Bloquea venta si la capacidad máxima de la sala fue alcanzada.

5. **Relaciones POO**:
   - **Composición**: `Venta` crea sus objetos `DetalleVenta` en su propio flujo.
   - **Agregación**: `Funcion` recibe por parámetro una `Pelicula` creada externamente.

6. **Integración API REST**:
   - `ServicioCarteleraAPI` consulta la API de TMDB en tiempo real para obtener estrenos actuales y transformarlos dinámicamente en objetos `Pelicula`.

7. **Funcionalidades de Experiencia de Usuario**:
   - **Ingreso**: Tipo de acceso Invitado o Cliente Registrado (10% Dcto en entradas 2D).
   - **Restricción de Edad**: Solicitud de acompañante adulto mayor de edad (+18) con compra automática de 2 entradas.
   - **Cine de 10 Salas**: Salas clasificadas por formato (1-5 2D, 6-8 3D, 9-10 VIP) con mapa gráfico de asientos `[A1]` a `[E6]`.
   - **Asistente Virtual de Dulcería**: Menú de palomitas (formatos y sabores), bebidas, extras y sugerencia de ventas cruzadas.

---

## 🚀 Cómo Ejecutar

Requiere **Python 3.8+** (utiliza bibliotecas nativas `urllib` y `json`).
*Nota: Se requiere conexión a Internet activa al iniciar para cargar la cartelera desde la API de TMDB.*

```bash
# Ejecutar el sistema completo en la terminal
python main.py
```
