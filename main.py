from datetime import datetime

from model import (
    AsistenteDulceriaCine,
    Boletero,
    Cliente,
    CotizacionDolar,
    EdadInsuficienteError,
    EncargadoDulceria,
    Funcion2D,
    Funcion3D,
    FuncionVIP,
    GestorPersistencia,
    Pelicula,
    ProductoImportado,
    ProductoNacional,
    Sala,
    SalaLlenaError,
    Venta,
)

class SistemaCineCLI:
    """
    Sistema Integral de Gestión y Ventas para Cine Estrella (CineApp).
    Cumple con el Guion de Pruebas (P01-P19) y principios avanzados de POO:
    - Menú Principal navegable con control de errores (P01, P18, P19).
    - CRUD completo de Películas y Funciones con Persistencia JSON (P02, P03, P04, P05, P06).
    - Validación matemática estricta de RUT con Módulo 11 (P07, P08).
    - Polimorfismo real en cálculo de tarifas 2D, 3D y VIP (P09, P10, P11).
    - Transacción unificada de venta (entradas + dulcería) y consulta de detalles (P12, P13).
    - Reglas de negocio protegidas con excepciones de dominio (P14: SalaLlenaError, P15: EdadInsuficienteError).
    - Integración dinámica con API oficial mindicador.cl y contingencia sin internet (P16, P17).
    """

    def __init__(self):
        # 1. Cargar persistencia de datos (Películas)
        self.peliculas = GestorPersistencia.cargar_peliculas()
        self.ventas_realizadas = []

        # 2. Inicializar Salas (1-5: 2D, 6-8: 3D, 9-10: VIP con aforo exclusivo)
        self.salas = {}
        for i in range(1, 6):
            self.salas[i] = Sala(numero_sala=i, formato="2D", capacidad=30)
        for i in range(6, 9):
            self.salas[i] = Sala(numero_sala=i, formato="3D", capacidad=30)
        for i in range(9, 11):
            self.salas[i] = Sala(numero_sala=i, formato="VIP", capacidad=4)  # VIP limitado para P11 y P14

        # 3. Inicializar Personal del Cine
        self.boletero = Boletero("E001", "Carlos Boletero", "12.345.678-5", "Caja Principal")
        self.dulcero = EncargadoDulceria("E002", "Marta Dulceria", "98.765.432-1", "Turno Tarde")

        # 4. Sincronizar Cotización del Dólar (mindicador.cl con fallback)
        self.cotizacion_dolar = CotizacionDolar.obtener_cotizacion_del_dia()
        ProductoImportado.configurar_cotizacion(self.cotizacion_dolar)

        # 5. Clientes registrados en memoria
        self.clientes_registrados = {
            "123456785": Cliente("12.345.678-5", "Cliente VIP Registrado", 28)
        }

        # 6. Funciones de cartelera iniciales
        self.funciones = self._inicializar_funciones_base()

    def _inicializar_funciones_base(self):
        funciones = {}
        if self.peliculas:
            p1 = self.peliculas[0]
            p2 = self.peliculas[1] if len(self.peliculas) > 1 else p1
            p3 = self.peliculas[2] if len(self.peliculas) > 2 else p1

            funciones["F2D-1"] = Funcion2D("F2D-1", datetime.now(), p1, precio_base=5000, capacidad_total=30)
            funciones["F3D-1"] = Funcion3D("F3D-1", datetime.now(), p2, precio_base=5000, capacidad_total=30, recargo_3d=2000)
            funciones["FVIP-1"] = FuncionVIP("FVIP-1", datetime.now(), p3, precio_base=5000, capacidad_total=4, recargo_vip=5000)
        return funciones

    def iniciar(self):
        """P01: Ejecución del programa y presentación del Menú Principal."""
        while True:
            print("\n" + "=" * 68)
            print(" [***] SISTEMA DE GESTION Y VENTAS CINE ESTRELLA (CINEAPP) [***] ")
            print("=" * 68)
            print(" [1] Iniciar Venta de Entradas y Dulceria")
            print(" [2] Administracion de Peliculas (Crear, Listar, Modificar, Eliminar)")
            print(" [3] Administracion de Funciones (2D, 3D, VIP - Tarifas Polimorficas)")
            print(" [4] Consultar Ventas Realizadas y Detalle de Comprobante")
            print(" [5] Consultar Cotizacion Oficial del Dolar (mindicador.cl)")
            print(" [0] Salir del Sistema")
            print("=" * 68)

            opcion = input("Seleccione una opcion (0-5): ").strip()

            if opcion == "1":
                self._flujo_venta_entradas()
            elif opcion == "2":
                self._menu_administracion_peliculas()
            elif opcion == "3":
                self._menu_administracion_funciones()
            elif opcion == "4":
                self._consultar_ventas()
            elif opcion == "5":
                self._consultar_dolar()
            elif opcion == "0":
                print("\n[INFO] Gracias por utilizar CineApp. Guardando estado y saliendo...")
                break
            else:
                # P18: Opción de menú que no existe (ej: 99)
                print(f"\n[ATENCION] La opcion '{opcion}' no es valida. Ingrese una opcion entre 0 y 5.")

    # -------------------------------------------------------------------------
    # P02, P03, P04, P05, P06: CRUD Y PERSISTENCIA DE PELÍCULAS
    # -------------------------------------------------------------------------
    def _menu_administracion_peliculas(self):
        while True:
            print("\n" + "-" * 55)
            print("  --- GESTION DE PELICULAS EN CARTELERA (CRUD) ---")
            print("-" * 55)
            print("  [1] Listar peliculas en cartelera (P03)")
            print("  [2] Crear nueva pelicula (P02)")
            print("  [3] Modificar clasificacion de pelicula (P04)")
            print("  [4] Eliminar pelicula de cartelera (P06)")
            print("  [0] Volver al Menu Principal")
            print("-" * 55)

            sub_op = input("Seleccione una opcion (0-4): ").strip()

            if sub_op == "1":
                self._listar_peliculas()
            elif sub_op == "2":
                self._crear_pelicula()
            elif sub_op == "3":
                self._modificar_pelicula()
            elif sub_op == "4":
                self._eliminar_pelicula()
            elif sub_op == "0":
                break
            else:
                print(f"[ATENCION] Opcion '{sub_op}' invalida.")

    def _listar_peliculas(self):
        """P03: Listar películas."""
        print("\n" + "=" * 70)
        print("                CARTELERA DE PELICULAS REGISTRADAS")
        print("=" * 70)
        if not self.peliculas:
            print(" [!] No hay peliculas registradas en la cartelera.")
            return

        print(f" {'N°':<4} | {'ID':<8} | {'TITULO':<25} | {'DURACION':<10} | {'CLASIF':<7} | {'EDAD MIN':<8}")
        print("-" * 70)
        for idx, p in enumerate(self.peliculas, 1):
            print(f" [{idx:<2}] | {p.id_pelicula:<8} | {p.titulo:<25} | {p.duracion_minutos} min    | {p.clasificacion:<7} | +{p.edad_minima} anos")
        print("=" * 70)

    def _crear_pelicula(self):
        """P02: Crear película y confirmar guardado."""
        print("\n[CREAR NUEVA PELICULA]")
        titulo = input("Ingrese Titulo de la pelicula (ej: Estreno): ").strip()
        if not titulo:
            print("[ERROR] El titulo no puede estar vacio.")
            return

        clasif = input("Ingrese Clasificacion (ej: TE, +14, +18): ").strip().upper()
        if not clasif:
            clasif = "+14"

        while True:
            dur_input = input("Ingrese Duracion en minutos [120]: ").strip()
            if not dur_input:
                duracion = 120
                break
            try:
                duracion = int(dur_input)
                if duracion > 0:
                    break
                print("[ERROR] La duracion debe ser mayor a 0.")
            except ValueError:
                print("[ERROR] Debe ingresar un numero entero valido.")

        nuevo_id = f"P-{len(self.peliculas) + 101}"
        nueva_peli = Pelicula(nuevo_id, titulo, duracion, clasif)

        self.peliculas.append(nueva_peli)
        GestorPersistencia.guardar_peliculas(self.peliculas)
        print(f"\n[OK] El programa confirma que se guardo la pelicula '{nueva_peli.titulo}' ({nueva_peli.clasificacion}) con ID {nueva_peli.id_pelicula}.")

    def _modificar_pelicula(self):
        """P04: Modificar película: cambiar clasificación y listar."""
        if not self.peliculas:
            print("[ATENCION] No hay peliculas para modificar.")
            return

        self._listar_peliculas()
        while True:
            sel = input("\nIngrese el N° de la pelicula que desea modificar (o 'C' para cancelar): ").strip()
            if sel.upper() == "C":
                return
            try:
                num = int(sel)
                if 1 <= num <= len(self.peliculas):
                    pelicula = self.peliculas[num - 1]
                    break
                print("[ATENCION] Numero fuera de rango.")
            except ValueError:
                print("[ERROR] Ingrese un numero valido.")

        print(f"\nModificando pelicula '{pelicula.titulo}' (Clasificacion actual: {pelicula.clasificacion})")
        nueva_clasif = input("Ingrese nueva clasificacion (ej: +14, +18, TE): ").strip().upper()
        if not nueva_clasif:
            print("[ATENCION] No se ingresaron cambios.")
            return

        pelicula.clasificacion = nueva_clasif
        GestorPersistencia.guardar_peliculas(self.peliculas)
        print(f"[OK] Modificacion guardada con exito. Nueva clasificacion: {pelicula.clasificacion}")
        print("\nListado actualizado con el cambio:")
        self._listar_peliculas()

    def _eliminar_pelicula(self):
        """P06: Eliminar película de prueba y listar."""
        if not self.peliculas:
            print("[ATENCION] No hay peliculas para eliminar.")
            return

        self._listar_peliculas()
        while True:
            sel = input("\nIngrese el N° de la pelicula a eliminar (o 'C' para cancelar): ").strip()
            if sel.upper() == "C":
                return
            try:
                num = int(sel)
                if 1 <= num <= len(self.peliculas):
                    pelicula_borrada = self.peliculas.pop(num - 1)
                    break
                print("[ATENCION] Numero fuera de rango.")
            except ValueError:
                print("[ERROR] Ingrese un numero valido.")

        GestorPersistencia.guardar_peliculas(self.peliculas)
        print(f"[OK] Pelicula '{pelicula_borrada.titulo}' eliminada con exito.")
        print("\nListado actualizado:")
        self._listar_peliculas()

    # -------------------------------------------------------------------------
    # P09, P10, P11: ADMINISTRACIÓN DE FUNCIONES Y TARIFAS POLIMÓRFICAS
    # -------------------------------------------------------------------------
    def _menu_administracion_funciones(self):
        while True:
            print("\n" + "-" * 55)
            print("  --- GESTION DE FUNCIONES Y TARIFAS POLIMORFICAS ---")
            print("-" * 55)
            print("  [1] Listar funciones y precios calculados (P09, P10, P11)")
            print("  [2] Crear nueva funcion 2D, 3D o VIP")
            print("  [3] Demostracion Polimorfica: calcular_precio() en tiempo real")
            print("  [0] Volver al Menu Principal")
            print("-" * 55)

            sub = input("Seleccione opcion (0-3): ").strip()
            if sub == "1":
                self._listar_funciones()
            elif sub == "2":
                self._crear_funcion_manual()
            elif sub == "3":
                self._demostracion_polimorfica()
            elif sub == "0":
                break
            else:
                print(f"[ATENCION] Opcion '{sub}' invalida.")

    def _listar_funciones(self):
        print("\n" + "=" * 75)
        print("                 LISTADO DE FUNCIONES PROGRAMADAS")
        print("=" * 75)
        print(f" {'ID':<8} | {'TIPO':<6} | {'PELICULA':<22} | {'PRECIO FINAL':<14} | {'ASIENTOS':<12}")
        print("-" * 75)
        for fid, fn in self.funciones.items():
            tipo = fn.__class__.__name__.replace("Funcion", "")
            precio_str = f"${fn.calcular_precio():,.0f} CLP"
            asientos_str = f"{fn.asientos_vendidos}/{fn.capacidad_total} vendidos"
            print(f" {fid:<8} | {tipo:<6} | {fn.pelicula.titulo:<22} | {precio_str:<14} | {asientos_str:<12}")
        print("=" * 75)

    def _crear_funcion_manual(self):
        if not self.peliculas:
            print("[ERROR] Debe existir al menos una pelicula para crear una funcion.")
            return

        print("\n[CREAR NUEVA FUNCION]")
        print("Formatos disponibles: [1] Funcion 2D | [2] Funcion 3D | [3] Funcion VIP")
        fmt = input("Elija formato (1-3): ").strip()

        self._listar_peliculas()
        while True:
            try:
                p_idx = int(input("Seleccione el N° de la pelicula asociada: "))
                if 1 <= p_idx <= len(self.peliculas):
                    p_sel = self.peliculas[p_idx - 1]
                    break
                print("[ATENCION] Seleccione un numero de la lista.")
            except ValueError:
                print("[ERROR] Debe ingresar un numero.")

        fid = f"F-USR-{len(self.funciones) + 1}"
        horario = datetime.now()
        precio_base = 5000

        if fmt == "1":
            fn = Funcion2D(fid, horario, p_sel, precio_base=precio_base, capacidad_total=30)
            print(f"[OK] Creada Funcion 2D con precio propio: ${fn.calcular_precio():,.0f} CLP (P09).")
        elif fmt == "2":
            fn = Funcion3D(fid, horario, p_sel, precio_base=precio_base, capacidad_total=30, recargo_3d=2000)
            print(f"[OK] Creada Funcion 3D con precio propio distinto a 2D: ${fn.calcular_precio():,.0f} CLP (P10).")
        elif fmt == "3":
            fn = FuncionVIP(fid, horario, p_sel, precio_base=precio_base, capacidad_total=4, recargo_vip=5000)
            print(f"[OK] Creada Funcion VIP con precio propio: ${fn.calcular_precio():,.0f} CLP y asientos limitados: {fn.capacidad_total} (P11).")
        else:
            print("[ERROR] Formato no valido.")
            return

        self.funciones[fid] = fn

    def _demostracion_polimorfica(self):
        """Demuestra polimorfismo invocando fn.calcular_precio() sin consultar el tipo."""
        print("\n--- DEMOSTRACION POLIMORFICA SIN IF/ISINSTANCE ---")
        peli_demo = self.peliculas[0] if self.peliculas else Pelicula("P0", "Demo Film", 100, "TE")

        f2d = Funcion2D("DEMO-2D", datetime.now(), peli_demo, precio_base=5000, capacidad_total=30)
        f3d = Funcion3D("DEMO-3D", datetime.now(), peli_demo, precio_base=5000, capacidad_total=30, recargo_3d=2000)
        fvip = FuncionVIP("DEMO-VIP", datetime.now(), peli_demo, precio_base=5000, capacidad_total=4, recargo_vip=5000)

        lista_polimorfica = [f2d, f3d, fvip]
        for f in lista_polimorfica:
            print(f" -> Objeto tipo {f.__class__.__name__:<11} | Tarifa calculada: ${f.calcular_precio():,.0f} CLP")

    # -------------------------------------------------------------------------
    # P16, P17: CONSULTAR COTIZACIÓN DÓLAR OFICIAL
    # -------------------------------------------------------------------------
    def _consultar_dolar(self):
        print("\n" + "=" * 65)
        print("   CONSULTA DE INDICADOR EXTERNO: DOLAR OBSERVADO")
        print("=" * 65)
        print("Conectando con https://mindicador.cl/api/dolar ...")
        self.cotizacion_dolar = CotizacionDolar.obtener_cotizacion_del_dia()
        ProductoImportado.configurar_cotizacion(self.cotizacion_dolar)

        valor_usd = self.cotizacion_dolar.get_valor_dolar()
        print(f"\nValor del Dolar Aplicado: ${valor_usd:,.2f} CLP")
        print(f"Origen del Dato: {self.cotizacion_dolar.origen}")
        print(f"Fecha de Cotizacion: {self.cotizacion_dolar.fecha_actualizacion}")

        # Ejemplo de cálculo con snack importado
        nachos = ProductoImportado("D-IMP", "Nachos Importados (USD)", stock=10, precio_usd=4.0)
        precio_clp = nachos.get_precio_unitario()
        print(f"\nEjemplo en Dulceria: 1x {nachos.descripcion} (${nachos.precio_usd:.2f} USD)")
        print(f" -> Precio en pesos chilenos: ${precio_clp:,.0f} CLP")
        print("=" * 65)

    # -------------------------------------------------------------------------
    # P07, P08, P12, P13, P14, P15: FLUJO DE VENTA, REGLAS Y COMPROBANTE
    # -------------------------------------------------------------------------
    def _flujo_venta_entradas(self):
        print("\n" + "=" * 68)
        print(" [***] INICIO DEL PROCESO DE VENTA DE ENTRADAS Y DULCERIA [***] ")
        print("=" * 68)

        # PASO 1: CLIENTE Y VALIDACIÓN DE RUT (P07, P08, P19)
        cliente_titular = self._solicitar_cliente()
        if cliente_titular is None:
            return

        # PASO 2: SELECCIÓN DE PELÍCULA
        if not self.peliculas:
            print("[ERROR] No hay peliculas disponibles en cartelera.")
            return

        self._listar_peliculas()
        while True:
            try:
                # P19: control de letras
                p_op = int(input(f"\nSeleccione el N° de la pelicula a ver (1-{len(self.peliculas)}): "))
                if 1 <= p_op <= len(self.peliculas):
                    pelicula_sel = self.peliculas[p_op - 1]
                    break
                print("[ATENCION] Opcion fuera de rango.")
            except ValueError:
                print("[ERROR] Debe ingresar un numero entero valido (no letras).")

        print(f"[OK] Pelicula seleccionada: '{pelicula_sel.titulo}' (Clasificacion: {pelicula_sel.clasificacion} | Minimo: {pelicula_sel.edad_minima} anos)")

        # PASO 3: FORMATO DE SALA Y FUNCIÓN
        print("\n[PASO 3] TIPO DE FUNCION")
        print(" [1] Funcion 2D ($5.000 / $4.500 con 10% Dcto si es registrado)")
        print(" [2] Funcion 3D ($7.000 - Incluye lentes 3D)")
        print(" [3] Funcion VIP ($10.000 - Aforo exclusivo y asientos reclinables)")

        while True:
            fmt_op = input("\nElija el tipo de funcion (1-3): ").strip()
            if fmt_op in ["1", "2", "3"]:
                break
            print("[ATENCION] Opcion no valida. Ingrese 1, 2 o 3.")

        es_registrado = cliente_titular.rut.replace(".", "").replace("-", "") in self.clientes_registrados
        horario = datetime.now()
        precio_base = 5000

        if fmt_op == "1":
            descuento = 0.10 if es_registrado else 0.0
            formato = "2D"
            funcion = Funcion2D("F2D", horario, pelicula_sel, precio_base, capacidad_total=30, descuento=descuento)
        elif fmt_op == "2":
            formato = "3D"
            funcion = Funcion3D("F3D", horario, pelicula_sel, precio_base, capacidad_total=30, recargo_3d=2000)
        else:
            formato = "VIP"
            funcion = FuncionVIP("FVIP", horario, pelicula_sel, precio_base, capacidad_total=4, recargo_vip=5000)

        # Seleccionar sala
        salas_formato = [s for s in self.salas.values() if s.formato == formato]
        sala_elegida = salas_formato[0]
        funcion.capacidad_total = sala_elegida.capacidad

        # PASO 4: CANTIDAD DE ENTRADAS (P19)
        while True:
            try:
                cant_entradas = int(input("\nCuantas entradas desea comprar? (Minimo 1): "))
                if cant_entradas >= 1:
                    break
                print("[ATENCION] Debe comprar al menos 1 entrada.")
            except ValueError:
                print("[ERROR] Debe ingresar un numero entero valido (no letras).")

        # Emisión de venta
        id_venta = f"V-{len(self.ventas_realizadas) + 101}"
        venta = Venta(id_venta, cliente_titular)
        asientos_reservados = []
        venta_cancelada = False

        for n_ent in range(1, cant_entradas + 1):
            print(f"\n[SELECCION DE ASIENTO {n_ent}/{cant_entradas}]")
            sala_elegida.mostrar_mapa_asientos()

            while True:
                cod_asiento = input(f"Ingrese codigo de asiento para la entrada {n_ent} (ej: V1 o A1): ").strip().upper()
                if not sala_elegida.esta_disponible(cod_asiento):
                    print(f"[ERROR] El asiento '{cod_asiento}' no existe o ya esta ocupado. Intente con otro.")
                    continue

                # INTENTO DE EMISIÓN DE ENTRADA CON EL MODELO (Boletero)
                # Regla 1 (P15): EdadInsuficienteError
                # Regla 2 (P14): SalaLlenaError
                try:
                    entrada = self.boletero.emitir_entrada(cliente_titular, funcion, cod_asiento)
                    sala_elegida.ocupar_asiento(cod_asiento)
                    asientos_reservados.append(cod_asiento)
                    venta.agregar_detalle(entrada, 1)
                    print(f"[OK] Asiento {cod_asiento} reservado con exito.")
                    break

                except EdadInsuficienteError as err:
                    # P15: Regla 1 capturada
                    print(f"\n[EXCEPCION DE DOMINIO ATRAPADA: EdadInsuficienteError]")
                    print(f">> {err}")
                    print("[VENTA IMPEDIDA] Regla de negocio 1 activada por el modelo (Boletero.validar_venta).")
                    print("El cliente no cumple con la clasificacion requerida. El sistema impide la venta y sigue funcionando.")
                    venta_cancelada = True
                    break

                except SalaLlenaError as err:
                    # P14: Regla 2 capturada
                    print(f"\n[EXCEPCION DE DOMINIO ATRAPADA: SalaLlenaError]")
                    print(f">> {err}")
                    print("[VENTA IMPEDIDA] Regla de negocio 2 activada por el modelo (Funcion.ocupar_asiento).")
                    print("La funcion no cuenta con asientos disponibles. El sistema impide la venta y sigue funcionando.")
                    venta_cancelada = True
                    break

            if venta_cancelada:
                break

        if venta_cancelada:
            print("\n[INFO] La transaccion fue cancelada debido a la regla del negocio. Regresando al menu principal...")
            return

        # PASO 5: DULCERÍA Y SNACKS (P12: 2 entradas + dulcería en la misma venta)
        print("\n[PASO 5] DULCERIA DEL CINE")
        resp_dulceria = input("Desea agregar productos de dulceria a esta misma venta? (S/N): ").strip().upper()
        if resp_dulceria == "S":
            asistente = AsistenteDulceriaCine(self.dulcero)
            asistente.atender_pedido(venta)

        # EMITIR COMPROBANTE UNIFICADO (P12, P13)
        comprobante = venta.emitir_comprobante()
        print("\n" + "=" * 68)
        print(" [***] RESUMEN DE VENTA EMITIDO EXITOSAMENTE [***] ")
        print("=" * 68)
        print(f"Ubicacion: SALA {sala_elegida.numero_sala} ({sala_elegida.formato}) | Asientos: {', '.join(asientos_reservados)}")
        print(comprobante)
        print("=" * 68)

        # Guardar en registro histórico
        registro_venta = {
            "id_venta": venta.id_venta,
            "fecha": str(venta.fecha),
            "cliente": {
                "rut": cliente_titular.rut,
                "nombre": cliente_titular.nombre,
                "edad": cliente_titular.edad
            },
            "total": venta.calcular_total(),
            "comprobante": comprobante
        }
        self.ventas_realizadas.append(registro_venta)
        GestorPersistencia.guardar_venta_registro(registro_venta)
        print(f"[OK] Venta registrada con folio {venta.id_venta} en almacenamiento persistente.")

    def _solicitar_cliente(self):
        """Solicita cliente y valida RUT con Módulo 11 (P07, P08, P19)."""
        print("\n[DATOS DEL COMPRADOR]")
        while True:
            rut_in = input("Ingrese RUT del comprador con puntos y guion (ej: 12.345.678-5) o 'INVITADO': ").strip()
            if not rut_in:
                print("[ERROR] El RUT no puede estar vacio.")
                continue

            try:
                # Validar RUT antes de instanciar
                if rut_in.upper() != "INVITADO" and not Cliente.validar_rut(rut_in):
                    raise ValueError(f"RUT invalido: '{rut_in}'. El digito verificador no coincide con el cuerpo del RUT.")
                break
            except ValueError as e:
                # P08: Muestra mensaje y el programa sigue funcionando
                print(f"[ERROR] {e} Intente nuevamente.")

        nombre = input("Ingrese Nombre del comprador: ").strip()
        if not nombre:
            nombre = "Cliente General"

        while True:
            # P19: control de letras en campo edad
            try:
                edad = int(input("Ingrese Edad del comprador: "))
                cliente = Cliente(rut_in, nombre, edad)
                print(f"[OK] Cliente validado con exito: {cliente.nombre} (RUT: {cliente.rut}, Edad: {cliente.edad})")
                return cliente
            except ValueError as e:
                print(f"[ERROR] {e} Intente nuevamente.")

    # -------------------------------------------------------------------------
    # P13: CONSULTAR DETALLE DE VENTA
    # -------------------------------------------------------------------------
    def _consultar_ventas(self):
        ventas_totales = GestorPersistencia.cargar_ventas()
        print("\n" + "=" * 65)
        print("             HISTORIAL Y DETALLE DE VENTAS")
        print("=" * 65)
        if not ventas_totales:
            print(" [!] No hay ventas registradas en el sistema.")
            return

        for idx, v in enumerate(ventas_totales, 1):
            print(f" [{idx}] Folio: {v['id_venta']} | Fecha: {v['fecha'][:19]} | Cliente: {v['cliente']['nombre']} (RUT: {v['cliente']['rut']}) | Total: ${v['total']:,.0f} CLP")

        while True:
            sel = input("\nIngrese el N° de la venta que desea ver en detalle (o '0' para salir): ").strip()
            if sel == "0":
                break
            try:
                num = int(sel)
                if 1 <= num <= len(ventas_totales):
                    v_sel = ventas_totales[num - 1]
                    print("\n" + "-" * 60)
                    print(f"DETALLE COMPLETO DE VENTA {v_sel['id_venta']}:")
                    print("-" * 60)
                    print(v_sel.get("comprobante", "Sin comprobante de texto guardado."))
                    print("-" * 60)
                    break
                print("[ATENCION] Numero no valido.")
            except ValueError:
                print("[ERROR] Debe ingresar un numero entero.")


if __name__ == "__main__":
    app = SistemaCineCLI()
    app.iniciar()
