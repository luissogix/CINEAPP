# 🎬 CineApp - Sistema de Gestión y Ventas Cine Estrella (POO en Python)

**INACAP** - Programación Orientada a Objetos Seguro (TI3V21)  
**Proyecto**: Cine Estrella (CineApp)  
**Desarrolladores**: Luis Lugo & Débora Sepúlveda  
**Docente**: Michael Arjel  

🖼️ **Diagrama de Clases UML (Actualizado)**: [`Diagrama actualizado.png`](Diagrama%20actualizado.png)  
🖼️ **Diagrama de Clases UML (Versión 1)**: [`Primer diagrama.png`](Primer%20diagrama.png)  

---

## 📋 Descripción del Proyecto
`CineApp` es un sistema completo y modular para la gestión de salas de cine, emisión de boletos y dulcería en **Python 3**, desarrollado aplicando rigurosamente los principios de la **Programación Orientada a Objetos (POO)** y arquitectura defensiva.

El sistema implementa el **Guion de Pruebas Oficial (P01 a P19)**:
- **Menú Principal Interactivo** y robusto ante opciones inexistentes (P01, P18, P19).
- **CRUD completo y Persistencia de Datos** en archivo JSON local (`datos_cine.json`) para películas y funciones (P02, P03, P04, P05, P06).
- **Validación matemática estricta de Cédula de Identidad (RUT chileno)** con algoritmo Módulo 11 (P07, P08).
- **Polimorfismo Real** en cálculo de tarifas de funciones 2D, 3D y Salas VIP con aforo exclusivo (P09, P10, P11).
- **Transacción Unificada (Composición)**: Venta simultánea de boletos y dulcería bajo un único folio y consulta de comprobantes detallados (P12, P13).
- **Reglas del Negocio con Excepciones de Dominio Propias**:
  - `EdadInsuficienteError` (Regla 1: Restricción legal para películas +14 y +18) (P15).
  - `SalaLlenaError` (Regla 2: Control estricto de aforo y butacas) (P14).
- **Integración con API Externa Oficial**: Cotización del dólar en vivo desde `https://mindicador.cl/api/dolar` para snacks importados, con modo de contingencia defensivo sin conexión a internet (P16, P17).

---

## 🏗️ Arquitectura del Repositorio
```text
CINEAPP/
├── main.py                     # Punto de entrada con Menú Principal navegable
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación oficial
├── datos_cine.json             # Almacenamiento persistente local (CRUD y Ventas)
├── Diagrama actualizado.png     # Diagrama de Clases UML Actualizado (Sumativa 2)
├── Primer diagrama.png         # Diagrama de Clases UML Inicial (Sumativa 1)
├── recursos/                   # Fuentes de diagramas (.drawio/.xml) y generadores
└── model/                      # Paquete con las clases del dominio
    ├── __init__.py             # Exposición de clases
    ├── cliente.py              # Cliente con validación de RUT (Módulo 11) y edad
    ├── pelicula.py             # Película con setters y autoclasificación
    ├── funcion.py              # Clase abstracta base Función
    ├── funcion_2d.py           # Subtipo Función 2D (con descuento clientes registrados)
    ├── funcion_3d.py           # Subtipo Función 3D (con recargo de lentes)
    ├── funcion_vip.py          # Subtipo Función VIP (con recargo de confort y aforo exclusivo)
    ├── sala.py                 # Salas clasificadas (mapas visuales y control de butacas)
    ├── empleado.py             # Clase base abstracta Empleado
    ├── boletero.py             # Boletero (emisión y aplicación de Reglas 1 y 2)
    ├── encargado_dulceria.py   # Encargado de confitería y ventas de dulcería
    ├── asistente_dulceria.py   # Asistente virtual para selección de snacks
    ├── item_vendible.py        # Interfaz abstracta para ítems transaccionales
    ├── entrada.py              # Subtipo Entrada para cine
    ├── producto_dulceria.py    # Clase base para confitería
    ├── producto_nacional.py    # Producto nacional cotizado en CLP
    ├── producto_importado.py   # Producto importado cotizado en USD con conversión dinámica
    ├── cotizacion_dolar.py     # Integración con mindicador.cl y fallback offline
    ├── venta.py                # Transacción unificada (Composición)
    ├── detalle_venta.py        # Detalle de venta (ítem, cantidad y subtotales)
    ├── persistencia.py         # Gestor de persistencia en disco (JSON)
    ├── edad_insuficiente_error.py # Excepción de dominio para Regla 1
    └── sala_llena_error.py     # Excepción de dominio para Regla 2
```

---

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/luissogix/CINEAPP.git
cd CINEAPP
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el sistema
```bash
python main.py
```

---

## 🧪 Guía Rápida de Verificación (Guion de Pruebas P01 - P19)

| N° | Prueba | Procedimiento en el Sistema | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **P01** | Ejecución | `python main.py` | Inicia y muestra el menú principal numerado (0-5). |
| **P02** | Crear película | Opción `[2]` -> `[2]`. Título: `Estreno`, Clasif: `+14`. | Confirma que se guardó con ID asignado. |
| **P03** | Listar película | Opción `[2]` -> `[1]`. | Aparece `Estreno (+14)` en la cartelera. |
| **P04** | Modificar película | Opción `[2]` -> `[3]`. Seleccionar `Estreno`, cambiar a `+18`. | El listado muestra el cambio de clasificación a `+18`. |
| **P05** | Persistencia | Salir (`[0]`), volver a ejecutar `python main.py` y listar (`[2]` -> `[1]`). | El registro `Estreno (+18)` sigue presente. |
| **P06** | Eliminar película | Opción `[2]` -> `[4]`. Seleccionar `Estreno`. | La película se elimina y ya no aparece en el listado. |
| **P07** | RUT correcto | Opción `[1]`. Ingresar RUT: `12.345.678-5`. | Lo acepta exitosamente. |
| **P08** | RUT incorrecto | Opción `[1]`. Ingresar RUT: `12.345.678-9`. | Lo rechaza por dígito verificador inválido y el programa sigue funcionando. |
| **P09** | Función 2D | Opción `[3]` -> `[1]` o `[3]`. | Calcula precio propio ($5.000 / $4.500 con descuento). |
| **P10** | Función 3D | Opción `[3]` -> `[1]` o `[3]`. | Calcula precio propio ($7.000, distinto a 2D). |
| **P11** | Función VIP | Opción `[3]` -> `[1]` o `[3]`. | Calcula precio propio ($10.000) y asientos limitados (4 cupos). |
| **P12** | Registrar venta | Opción `[1]`. Comprar 2 entradas y agregar productos en dulcería. | Queda guardado como un solo registro de venta con folio unificado. |
| **P13** | Detalle de venta | Opción `[4]`. Seleccionar el folio de la venta. | Se ven todas sus líneas de detalle, subtotales y total general. |
| **P14** | Función sin asientos | Opción `[1]`. En Sala VIP (4 asientos), comprar los 4 asientos e intentar 1 más. | La venta se impide (`SalaLlenaError`), avisa y sigue funcionando. |
| **P15** | Menor en película +18 | Opción `[1]`. Elegir película +18 con cliente de 15 años. | La venta se impide (`EdadInsuficienteError`), avisa y sigue funcionando. |
| **P16** | Dólar del día | Opción `[5]`. | Muestra el valor oficial de hoy desde `https://mindicador.cl/api/dolar`. |
| **P17** | Dólar sin internet | Desconectar wifi y entrar a Opción `[5]`. | Avisa que no pudo conectar, aplica valor de respaldo ($950) y no se cae. |
| **P18** | Opción inválida | En el Menú Principal, ingresar `99`. | Muestra mensaje de opción inválida y regresa al menú. |
| **P19** | Letras en número | En campo de edad o entradas, ingresar `abc`. | Muestra mensaje de error de formato y no se cae. |
