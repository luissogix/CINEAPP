# 🎬 CineApp - Sistema de Gestión y Ventas Cine Estrella (POO Seguro)

---

## 1. Integrantes y Negocio

- **Integrantes del Equipo**:
  - **Luis Lugo**
  - **Débora Sepúlveda**
- **Negocio Asignado**: **Cine Estrella (CineApp)**  
  Sistema integral de gestión de cartelera cinematográfica, clasificación por edades, control de aforos por sala (2D, 3D, VIP), venta transaccional unificada de boletos y snacks de confitería, y cotización de productos importados.
- **Asignatura**: Programación Orientada a Objeto Seguro (TI3V21)  
- **Institución**: INACAP Sede Puente Alto  
- **Docente**: Michael Arjel  
- **Evaluación**: Evaluación Sumativa N°3 (Ponderación 35%)  

---

## 2. Cómo Instalar y Ejecutar el Programa (Paso a Paso)

El sistema está diseñado para ejecutarse de forma inmediata en cualquier computador que solo disponga de Python 3.8 o superior, sin configuraciones complejas de base de datos externas.

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/luissogix/CINEAPP.git
cd CINEAPP
```

### Paso 2: Instalar dependencias oficiales
El proyecto utiliza la librería oficial `requests` para el consumo seguro de servicios web:
```bash
pip install -r requirements.txt
```

### Paso 3: Ejecutar la aplicación
```bash
python main.py
```

> [!NOTE]
> Al iniciar la aplicación por primera vez, el sistema crea automáticamente el archivo de base de datos SQLite local (`cineapp.db`) y todas sus tablas con integridad referencial (`PRAGMA foreign_keys = ON;`), poblando el catálogo base de películas para su uso inmediato.

---

## 3. Decisiones de Seguridad

### 3.1 Prevención de Inyección SQL (SQL Injection - CWE-89)
- **Arquitectura DAO desacoplada**: La capa de acceso a datos está completamente separada del modelo en el paquete [`dao/`](dao/), impidiendo que exista lógica SQL embebida en las clases de entidad (`model/`).
- **Consultas 100% Parametrizadas**: Ninguna sentencia SQL se construye mediante concatenación de texto, operadores `+` o `f-strings`. Todas las operaciones CRUD (`PeliculaDAO`, `ClienteDAO`, `VentaDAO`) utilizan marcadores de posición nativos (`?`) donde el motor de SQLite se encarga del escape seguro de caracteres:
  ```python
  # Ejemplo en dao/pelicula_dao.py:
  cursor.execute("SELECT * FROM peliculas WHERE id_pelicula = ?;", (id_pelicula,))
  ```
- **Transacciones Atómicas Seguras**: La venta y sus líneas de detalle se registran bajo un bloque transaccional atómico (`with conn:` en `VentaDAO`), garantizando que si una línea de detalle falla, se aplique un `ROLLBACK` automático para mantener la consistencia de los datos.

### 3.2 Validación de Entradas de Usuario
- **Validación Matemática de Cédula de Identidad (RUT chileno)**: Implementación estricta del algoritmo **Módulo 11** en [`model/cliente.py`](model/cliente.py). Se valida el formato, cuerpo y dígito verificador. Cualquier RUT con dígito erróneo es rechazado defensivamente.
- **Encapsulamiento y Validaciones en `@setter`**:
  - `Cliente.edad`: Valida tipo entero y rango legal de 0 a 120 años mediante `@edad.setter`.
  - `Pelicula.clasificacion`: Valida la nomenclatura estándar (`TE`, `+14`, `+18`) y autocalcula la edad mínima requerida.
- **Excepciones Propias del Dominio**:
  - `EdadInsuficienteError`: Bloquea la venta si un menor de edad intenta adquirir entradas para películas no aptas (+14 o +18) sin acompañante adulto.
  - `SalaLlenaError`: Bloquea la venta cuando se sobrepasa la capacidad física de la sala (aforo exclusivo de 4 asientos en Salas VIP).
- **Control de Formato y Robustez en Menú CLI**: Validación previa de tipo en todos los prompts numéricos, previniendo caídas ante entradas no numéricas (`abc`) u opciones fuera de rango (`99`).

---

## 4. Uso de Inteligencia Artificial

Durante el desarrollo del sistema se utilizaron asistentes de IA como apoyo técnico, evaluando críticamente cada recomendación:

### 4.1 Código Adoptado (con justificación técnica)
- **Algoritmo Módulo 11 para RUT chileno**: Se adoptó la función de ponderación matemática (multiplicadores 2 al 7 con residuo 11) para validar la Cédula de Identidad en `Cliente.validar_rut()`.
  - *Razón técnica*: Es un algoritmo determinista estándar de la legislación chilena. Implementarlo con lógica nativa de Python evita dependencias externas innecesarias y asegura alta velocidad de ejecución.

### 4.2 Código Modificado (con justificación técnica)
- **Cliente HTTP para Consumo de API en `CotizacionDolar`**: La IA inicialmente sugirió usar llamadas inline directas sin control de tiempo de respuesta. Se modificó encapsulando el consumo en una clase dedicada con la librería oficial `requests`, agregando:
  - Cabecera `User-Agent` para evitar bloqueos HTTP 403.
  - `timeout=5` segundos para evitar que la aplicación quede congelada ante latencias de red.
  - Manejo granular de excepciones (`requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`).
  - Modo de contingencia defensivo con valor de respaldo ($950 CLP) que asegura la continuidad operativa del cine sin internet.

### 4.3 Código Descartado (con justificación técnica)
- **Construcción de Consultas SQL mediante `f-strings`**: Se descartaron sugerencias de generación rápida de queries que formateaban texto directamente en la instrucción SQL (`f"SELECT * FROM peliculas WHERE titulo = '{titulo}'"`).
  - *Razón técnica*: Esta práctica introduce una vulnerabilidad crítica de **Inyección SQL (CWE-89)**. Se descartó categóricamente y se impuso el uso exclusivo de tuplas de parámetros con el marcador `?` en todos los métodos del paquete `dao/`.

---

## 5. Arquitectura del Repositorio y Diagramas UML

```text
CINEAPP/
├── dao/                        # Capa de Acceso a Datos (Persistencia SQLite)
│   ├── __init__.py             # Exposición de DAOs
│   ├── conexion.py             # Conexión centralizada y creación automática de tablas
│   ├── pelicula_dao.py         # CRUD completo parametrizado para Películas
│   ├── cliente_dao.py          # Registro y lectura parametrizada de Clientes
│   └── venta_dao.py            # Transacción atómica de Venta y DetalleVenta
├── model/                      # Clases del Dominio POO
│   ├── __init__.py             # Exposición del modelo
│   ├── cliente.py              # Validación de RUT (Módulo 11) y @edad.setter
│   ├── pelicula.py             # Película con setters y autoclasificación
│   ├── funcion.py              # Clase abstracta base Función
│   ├── funcion_2d.py           # Subtipo Función 2D
│   ├── funcion_3d.py           # Subtipo Función 3D (recargo lentes)
│   ├── funcion_vip.py          # Subtipo Función VIP (confort y aforo exclusivo)
│   ├── sala.py                 # Salas con control de butacas y mapa visual
│   ├── empleado.py             # Clase abstracta Empleado
│   ├── boletero.py             # Emisión y aplicación de Reglas 1 y 2
│   ├── encargado_dulceria.py   # Gestión de ventas de confitería
│   ├── asistente_dulceria.py   # Asistente virtual para selección de snacks
│   ├── item_vendible.py        # Interfaz para ítems transaccionales
│   ├── entrada.py              # Ítem vendible tipo Entrada
│   ├── producto_dulceria.py    # Clase base para confitería
│   ├── producto_nacional.py    # Producto nacional en CLP
│   ├── producto_importado.py   # Producto importado en USD convertido a CLP
│   ├── cotizacion_dolar.py     # Integración API mindicador.cl con requests y fallback
│   ├── venta.py                # Transacción unificada (Composición)
│   ├── detalle_venta.py        # Detalle de venta (subtotales y cantidades)
│   ├── persistencia.py         # Respaldo de persistencia JSON local
│   ├── edad_insuficiente_error.py # Excepción de dominio para Regla 1
│   └── sala_llena_error.py     # Excepción de dominio para Regla 2
├── main.py                     # Menú principal y punto de entrada interactivo
├── requirements.txt            # Dependencias oficiales (requests)
├── Diagrama actualizado.png     # Diagrama de Clases UML del sistema completo
├── Primer diagrama.png         # Diagrama de Clases UML Inicial (Sumativa 1)
└── recursos/                   # Scripts generadores y fuentes .drawio / .xml
```

### Diagramas de Clases UML:
- 🖼️ **Diagrama de Clases UML (Actualizado con DAO y SQLite)**: [`Diagrama actualizado.png`](Diagrama%20actualizado.png)
- 🖼️ **Diagrama de Clases UML (Versión 1 - Inicial)**: [`Primer diagrama.png`](Primer%20diagrama.png)

---

## 6. Guía Rápida de Verificación (P01 a P19)

| N° | Prueba | Procedimiento en el Sistema | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **P01** | Ejecución | `python main.py` | Inicia y muestra el menú principal numerado (0-5). |
| **P02** | Crear película | Opción `[2]` -> `[2]`. Título: `Estreno`, Clasif: `+14`. | Confirma que se guardó en SQLite con ID asignado. |
| **P03** | Listar película | Opción `[2]` -> `[1]`. | Aparece `Estreno (+14)` en la cartelera. |
| **P04** | Modificar película | Opción `[2]` -> `[3]`. Seleccionar `Estreno`, cambiar a `+18`. | Modificación guardada en SQLite; listado muestra clasificación `+18`. |
| **P05** | Persistencia | Salir (`[0]`), volver a ejecutar `python main.py` y listar (`[2]` -> `[1]`). | El registro `Estreno (+18)` persiste en la base de datos `cineapp.db`. |
| **P06** | Eliminar película | Opción `[2]` -> `[4]`. Seleccionar `Estreno`. | La película se elimina de SQLite y ya no aparece en el listado. |
| **P07** | RUT correcto | Opción `[1]`. Ingresar RUT: `12.345.678-5`. | Lo valida y acepta exitosamente. |
| **P08** | RUT incorrecto | Opción `[1]`. Ingresar RUT: `12.345.678-9`. | Lo rechaza por dígito verificador inválido y el sistema sigue operando. |
| **P09** | Función 2D | Opción `[3]` -> `[1]` o `[3]`. | Tarifa calculada con método polimórfico propio ($5.000 / $4.500). |
| **P10** | Función 3D | Opción `[3]` -> `[1]` o `[3]`. | Tarifa calculada con recargo propio ($7.000). |
| **P11** | Función VIP | Opción `[3]` -> `[1]` o `[3]`. | Tarifa propia ($10.000) y aforo limitado (4 asientos). |
| **P12** | Registrar venta | Opción `[1]`. Comprar entradas y agregar snacks. | Transacción unificada atómica guardada en SQLite (`ventas` y `detalles_venta`). |
| **P13** | Detalle de venta | Opción `[4]`. Seleccionar el folio de la venta. | Muestra cabecera y todas las líneas de detalle desde la base de datos. |
| **P14** | Función sin asientos | Opción `[1]`. En Sala VIP (4 cupos), ocupar los 4 cupos e intentar 1 más. | La venta se bloquea (`SalaLlenaError`), avisa y continúa operando. |
| **P15** | Menor en película +18 | Opción `[1]`. Seleccionar película +18 con cliente de 15 años. | La venta se bloquea (`EdadInsuficienteError`), avisa y continúa operando. |
| **P16** | Dólar del día | Opción `[5]`. | Consulta oficial a `mindicador.cl` con `requests` y muestra el valor en vivo. |
| **P17** | Dólar sin internet / timeout | Desconectar wifi o simular demora. | Avisa error de red/timeout, activa contingencia ($950 CLP) y no se cae. |
| **P18** | Opción inválida | En el Menú Principal, ingresar `99`. | Muestra advertencia de opción no válida y vuelve al menú. |
| **P19** | Letras en número | En campo de edad o entradas, ingresar `abc`. | Muestra error de formato numérico y solicita reintentar sin caerse. |
