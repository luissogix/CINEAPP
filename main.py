from datetime import datetime
from model import (Boletero, Cliente, CotizacionDolar, EdadInsuficienteError,
                   EncargadoDulceria, Funcion2D, Funcion3D, FuncionVIP,
                   ProductoImportado, ProductoNacional, Sala, SalaLlenaError,
                   ServicioCarteleraAPI, Venta, AsistenteDulceriaCine)


class SistemaCineCLI:
    """
    Sistema Interactivo de Selección e Ingreso al Cine.
    - Manejo de clientes Invitados vs Registrados (10% descuento en Funciones 2D para registrados).
    - 10 Salas clasificadas por formato (Salas 1-5: 2D, Salas 6-8: 3D, Salas 9-10: VIP).
    - Restricción de edad y opción de acompañante mayor de edad.
    """
    def __init__(self):
        self.clientes_registrados = {}
        # 1. Clasificación de las 10 Salas por Formato
        self.salas = {}
        for i in range(1, 6):
            self.salas[i] = Sala(numero_sala=i, formato="2D", capacidad=30)
        for i in range(6, 9):
            self.salas[i] = Sala(numero_sala=i, formato="3D", capacidad=30)
        for i in range(9, 11):
            self.salas[i] = Sala(numero_sala=i, formato="VIP", capacidad=30)
        
        # 2. Inicializar Servicio API y Cargar Películas de Cartelera
        self.servicio_api = ServicioCarteleraAPI()
        self.peliculas = self.servicio_api.obtener_peliculas_en_taquilla(limite=5)
        
        # 3. Empleados y Dulcería Base
        self.boletero = Boletero("E001", "Carlos Boletero", "12.345.678-9", "Caja Principal")
        self.dulcero = EncargadoDulceria("E002", "Marta Dulcería", "98.765.432-1", "Turno Tarde")
        
        cotizacion = CotizacionDolar(900)
        ProductoImportado.configurar_cotizacion(cotizacion)
        self.palomitas = ProductoNacional("D1", "Palomitas Grandes", 20, 3500)
        self.nachos = ProductoImportado("D2", "Nachos Importados (USD)", 10, 4.0)

    def iniciar(self):
        print("\n" + "=" * 68)
        print(" [***] BIENVENIDO AL SISTEMA DE GESTION Y SELECCION CINEAPP [***] ")
        print("=" * 68)

        while True:
            # PASO 1: TIPO DE ACCESO (INVITADO O REGISTRADO)
            print("\n[PASO 1] TIPO DE ACCESO DEL CLIENTE")
            print(" [1] Entrar como Invitado")
            print(" [2] Ingresar (Cliente ya registrado)")
            print(" [3] Registrarse como nuevo cliente (10% dcto en 2D)")
            
            es_registrado = False
            while True:
                tipo_acc = input("\nSeleccione opcion (1-3): ").strip()
                if tipo_acc == "1":
                    es_registrado = False
                    rut = "INVITADO"
                    nombre = "Invitado"
                    while True:
                        try:
                            edad = int(input("Ingrese Edad del Cliente: "))
                            cliente_titular = Cliente(rut, nombre, edad)
                            break
                        except ValueError as e:
                            print(f"[ERROR] {e}. Intente nuevamente.")
                    break
                elif tipo_acc == "2":
                    print("\n[INGRESO CLIENTE REGISTRADO]")
                    rut_ingreso = input("Ingrese su RUT registrado (puede ser sin puntos ni guion): ").strip().replace(".", "").replace("-", "")
                    if rut_ingreso in self.clientes_registrados:
                        cliente_titular = self.clientes_registrados[rut_ingreso]
                        es_registrado = True
                        print(f"[OK] Bienvenido de vuelta! Beneficio activo: 10% Descuento en entradas 2D.")
                        break
                    else:
                        print("[ATENCION] RUT no encontrado. Intente registrarse (opcion 3) o entrar como invitado.")
                elif tipo_acc == "3":
                    print("\n[REGISTRO DE NUEVO CLIENTE]")
                    rut_input = input("Ingrese su RUT (puede ser sin puntos ni guion): ").strip().replace(".", "").replace("-", "")
                    nombre = f"Cliente {rut_input}"
                    while True:
                        try:
                            edad = int(input("Ingrese Edad del Cliente: "))
                            cliente_titular = Cliente(rut_input, nombre, edad)
                            self.clientes_registrados[rut_input] = cliente_titular
                            es_registrado = True
                            print(f"[OK] Registro exitoso! Ha iniciado sesion automaticamente. Beneficio activo: 10% Descuento en entradas 2D.")
                            break
                        except ValueError as e:
                            print(f"[ERROR] {e}. Intente nuevamente.")
                    break
                else:
                    print("[ATENCION] Opcion invalida. Ingrese 1, 2 o 3.")

            # PASO 2: ELEGIR PELÍCULA DE CARTELERA
            print("\n[PASO 2] SELECCIONE UNA PELICULA DE TAQUILLA")
            for idx, p in enumerate(self.peliculas, 1):
                print(f" [{idx}] {p.titulo:<32} | {p.duracion_minutos} min | Clasificacion: {p.clasificacion} (Edad min: {p.edad_minima})")
            
            while True:
                try:
                    opcion_p = int(input("\nElija el numero de la pelicula que desea ver (1-5): "))
                    if 1 <= opcion_p <= len(self.peliculas):
                        pelicula_seleccionada = self.peliculas[opcion_p - 1]
                        break
                    print("[ATENCION] Opcion invalida. Seleccione un numero de la lista.")
                except ValueError:
                    print("[ATENCION] Debe ingresar un numero entero.")

            print(f"\n[OK] Pelicula seleccionada: '{pelicula_seleccionada.titulo}' (Edad Minima Exigida: {pelicula_seleccionada.edad_minima} anos)")

            # VALIDACIÓN DE EDAD Y ACOMPAÑANTE
            cliente_para_ticket = cliente_titular
            es_menor_con_acompanante = False

            if not pelicula_seleccionada.es_apta_para(cliente_titular.edad):
                print(f"\n[ATENCION] RESTRICCION DE EDAD: El cliente {cliente_titular.nombre} tiene {cliente_titular.edad} anos y la pelicula exige {pelicula_seleccionada.edad_minima} anos.")
                respuesta = input("Viene acompanado por un adulto mayor de edad? (S/N): ").strip().upper()
                
                if respuesta == "S":
                    print("\n[INFO] Por favor ingrese los datos del ACOMPANANTE MAYOR DE EDAD:")
                    rut_ac = input("RUT del Acompanante: ").strip()
                    nombre_ac = input("Nombre del Acompanante: ").strip()
                    while True:
                        try:
                            edad_ac = int(input("Edad del Acompanante: "))
                            if edad_ac < pelicula_seleccionada.edad_minima or edad_ac < 18:
                                print(f"[ERROR] El acompanante debe tener al menos 18 anos y cumplir la edad minima ({pelicula_seleccionada.edad_minima} anos).")
                                continue
                            acompanante = Cliente(rut_ac, nombre_ac if nombre_ac else "Acompanante Adulto", edad_ac)
                            break
                        except ValueError as e:
                            print(f"[ERROR] {e}. Intente nuevamente.")
                    
                    print(f"[OK] Acompanante validado: {acompanante.nombre} ({acompanante.edad} anos). Venta autorizada.")
                    cliente_para_ticket = acompanante
                    es_menor_con_acompanante = True
                else:
                    print("\n[ERROR] VENTA CANCELADA: No se permite el ingreso de menores sin un acompanante mayor de edad.")
                    if self._preguntar_nueva_compra():
                        continue
                    else:
                        break

            # PASO 3: TIPO DE FUNCIÓN
            print("\n[PASO 3] TIPO DE FUNCION")
            precio_2d_desc = "$4.500 (10% Dcto)" if es_registrado else "$5.000"
            print(f" [1] Funcion 2D ({precio_2d_desc})")
            print(" [2] Funcion 3D ($7.000 - Incluye lentes 3D)")
            print(" [3] Funcion VIP ($10.000 - Asientos Reclinables y Servicio Especial)")
            
            horario = datetime.now()
            precio_base = 5000
            
            while True:
                tipo_f = input("\nElija el tipo de funcion (1-3): ").strip()
                if tipo_f == "1":
                    descuento_2d = 0.10 if es_registrado else 0.0
                    funcion = Funcion2D("F2D", horario, pelicula_seleccionada, precio_base, capacidad_total=30, descuento=descuento_2d)
                    formato_elegido = "2D"
                    break
                elif tipo_f == "2":
                    funcion = Funcion3D("F3D", horario, pelicula_seleccionada, precio_base, capacidad_total=30, recargo_3d=2000)
                    formato_elegido = "3D"
                    break
                elif tipo_f == "3":
                    funcion = FuncionVIP("FVIP", horario, pelicula_seleccionada, precio_base, capacidad_total=30, recargo_vip=5000)
                    formato_elegido = "VIP"
                    break
                else:
                    print("[ATENCION] Opcion no valida. Ingrese 1, 2 o 3.")

            print(f"[OK] Formato seleccionado: {formato_elegido} (${funcion.calcular_precio():,.0f})")

            # PASO 4: FILTRAR Y SELECCIONAR SALAS CLASIFICADAS SEGÚN LA FUNCIÓN
            print(f"\n[PASO 4] SELECCION DE SALAS HABILITADAS PARA FORMATO {formato_elegido}")
            salas_filtradas = [sala for sala in self.salas.values() if sala.formato == formato_elegido]

            for s in salas_filtradas:
                disp = len(s.obtener_asientos_disponibles())
                print(f" - Sala {s.numero_sala:2d} (Formato: {s.formato}): [{disp}/30 Asientos libres]")

            while True:
                try:
                    num_sala = int(input(f"\nElija una sala configurada para {formato_elegido} ({[s.numero_sala for s in salas_filtradas]}): "))
                    if num_sala in [s.numero_sala for s in salas_filtradas]:
                        sala_elegida = self.salas[num_sala]
                        break
                    print(f"[ATENCION] La sala {num_sala} no esta disponible para formato {formato_elegido}.")
                except ValueError:
                    print("[ATENCION] Debe ingresar un numero de sala valido.")

            # PASO 5: CANTIDAD DE ENTRADAS Y DISPONIBILIDAD DE ASIENTOS
            print("\n[PASO 5] CANTIDAD DE ENTRADAS Y SELECCION DE ASIENTOS")
            min_entradas = 2 if es_menor_con_acompanante else 1
            if es_menor_con_acompanante:
                print(f"[INFO] Dado que asiste con un acompanante adulto, debe comprar al menos {min_entradas} entradas.")

            while True:
                try:
                    cantidad_entradas = int(input(f"Cuantas entradas desea comprar? (Minimo {min_entradas}): "))
                    if cantidad_entradas >= min_entradas:
                        break
                    print(f"[ATENCION] Debe comprar al menos {min_entradas} entrada(s).")
                except ValueError:
                    print("[ATENCION] Debe ingresar un numero valido.")

            asientos_reservados = []
            venta = Venta("V-101", cliente_para_ticket)
            venta_cancelada = False

            for n_ent in range(1, cantidad_entradas + 1):
                if es_menor_con_acompanante and n_ent == 1:
                    persona_label = f"Acompanante ({cliente_para_ticket.nombre})"
                elif es_menor_con_acompanante and n_ent == 2:
                    persona_label = f"Menor/Titular ({cliente_titular.nombre})"
                else:
                    persona_label = f"Entrada {n_ent}"

                print(f"\n[SELECCION DE ASIENTO {n_ent}/{cantidad_entradas}] PARA: {persona_label}")
                sala_elegida.mostrar_mapa_asientos()

                while True:
                    codigo_asiento = input(f"Ingrese codigo del asiento {n_ent} (ej: A1, C3): ").strip().upper()
                    if sala_elegida.esta_disponible(codigo_asiento):
                        try:
                            entrada = self.boletero.emitir_entrada(cliente_para_ticket, funcion, codigo_asiento)
                            sala_elegida.ocupar_asiento(codigo_asiento)
                            asientos_reservados.append(codigo_asiento)
                            venta.agregar_detalle(entrada, 1)
                            print(f"[OK] Asiento {codigo_asiento} reservado con exito.")
                            break
                        except (EdadInsuficienteError, SalaLlenaError) as err:
                            print(f"[ERROR DE NEGOCIO ATRAPADO] {err}")
                            print("[ATENCION] Venta interrumpida debido a la regla de negocio.")
                            venta_cancelada = True
                            break
                    else:
                        print(f"[ERROR] El asiento '{codigo_asiento}' no existe o ya esta ocupado. Intente con otro.")
                
                if venta_cancelada:
                    break
            
            if venta_cancelada:
                if self._preguntar_nueva_compra():
                    continue
                else:
                    break

            # DULCERÍA CON ASISTENTE VIRTUAL DE CINE
            print("\n[PASO 6] ATENCION VIRTUAL DE DULCERIA")
            print("Desea ingresar a la Dulceria del Cine para realizar un pedido? (S/N)")
            if input("Respuesta: ").strip().upper() == "S":
                asistente_dulceria = AsistenteDulceriaCine(self.dulcero)
                asistente_dulceria.atender_pedido(venta)

            # EMITIR COMPROBANTE FINAL
            print("\n" + "=" * 68)
            print(" [***] RESUMEN Y COMPROBANTE DE COMPRA [***] ")
            print("=" * 68)
            
            if es_registrado and formato_elegido == "2D":
                tipo_cliente_str = "Cliente Registrado (10% Dcto 2D Aplicado por entrada)"
            elif es_registrado:
                tipo_cliente_str = "Cliente Registrado (Descuento solo valido para funciones 2D)"
            else:
                tipo_cliente_str = "Cliente Invitado (Sin beneficios)"
                
            print(f"Tipo de Acceso: {tipo_cliente_str}")
            print(f"Titular de la Compra: {cliente_titular.nombre} (RUT: {cliente_titular.rut})")
            if es_menor_con_acompanante:
                print(f"Acompanante Responsable: {cliente_para_ticket.nombre} ({cliente_para_ticket.edad} anos)")
            print(f"Ubicacion: SALA {sala_elegida.numero_sala} ({sala_elegida.formato}) | Asientos: {', '.join(asientos_reservados)}")
            print(venta.emitir_comprobante())
            print("=" * 68)
            print(" [***] Disfrute su funcion en CINEAPP! [***] \n")

            if not self._preguntar_nueva_compra():
                break
        
        print("\n[INFO] Gracias por usar CINEAPP! Hasta pronto.")

    def _preguntar_nueva_compra(self):
        while True:
            resp = input("\n[?] Desea realizar otra compra / reiniciar el sistema? (S/N): ").strip().upper()
            if resp in ["S", "N"]:
                return resp == "S"
            print("[ATENCION] Ingrese S o N.")

if __name__ == "__main__":
    app = SistemaCineCLI()
    app.iniciar()
