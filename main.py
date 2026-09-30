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
        print(" 🎬 BIENVENIDO AL SISTEMA DE GESTIÓN Y SELECCIÓN CINEAPP 🎬")
        print("=" * 68)

        # PASO 1: TIPO DE ACCESO (INVITADO O REGISTRADO)
        print("\n📝 [PASO 1] TIPO DE ACCESO DEL CLIENTE")
        print(" [1] Entrar como Invitado")
        print(" [2] Cliente Registrado (Obtén 10% dcto en funciones 2D)")
        
        es_registrado = False
        while True:
            tipo_acc = input("\nSeleccione opción (1-2): ").strip()
            if tipo_acc == "1":
                es_registrado = False
                rut = "INVITADO"
                nombre = "Invitado"
                break
            elif tipo_acc == "2":
                es_registrado = True
                print("\n🔐 INGRESO CLIENTE REGISTRADO:")
                rut = input("Ingrese su RUT registrado (ej: 19.876.543-2): ").strip()
                nombre = input("Ingrese su Nombre Completo: ").strip()
                break
            else:
                print("⚠️ Opción inválida. Ingrese 1 o 2.")

        while True:
            try:
                edad = int(input("Ingrese Edad del Cliente: "))
                cliente_titular = Cliente(rut, nombre if nombre else "Cliente General", edad)
                break
            except ValueError as e:
                print(f"❌ Error: {e}. Intente nuevamente.")

        if es_registrado:
            print(f"✅ ¡Bienvenido(a) {cliente_titular.nombre}! Beneficio activo: 10% Descuento en entradas 2D.")

        # PASO 2: ELEGIR PELÍCULA DE CARTELERA
        print("\n🍿 [PASO 2] SELECCIONE UNA PELÍCULA DE TAQUILLA")
        for idx, p in enumerate(self.peliculas, 1):
            print(f" [{idx}] {p.titulo:<32} | {p.duracion_minutos} min | Clasificación: {p.clasificacion} (Edad mín: {p.edad_minima})")
        
        while True:
            try:
                opcion_p = int(input("\nElija el número de la película que desea ver (1-5): "))
                if 1 <= opcion_p <= len(self.peliculas):
                    pelicula_seleccionada = self.peliculas[opcion_p - 1]
                    break
                print("⚠️ Opción inválida. Seleccione un número de la lista.")
            except ValueError:
                print("⚠️ Debe ingresar un número entero.")

        print(f"\n✅ Película seleccionada: '{pelicula_seleccionada.titulo}' (Edad Mínima Exigida: {pelicula_seleccionada.edad_minima} años)")

        # VALIDACIÓN DE EDAD Y ACOMPAÑANTE
        cliente_para_ticket = cliente_titular
        es_menor_con_acompanante = False

        if not pelicula_seleccionada.es_apta_para(cliente_titular.edad):
            print(f"\n⚠️ RESTRICCIÓN DE EDAD: El cliente {cliente_titular.nombre} tiene {cliente_titular.edad} años y la película exige {pelicula_seleccionada.edad_minima} años.")
            respuesta = input("¿Viene acompañado por un adulto mayor de edad? (S/N): ").strip().upper()
            
            if respuesta == "S":
                print("\n👤 Por favor ingrese los datos del ACOMPAÑANTE MAYOR DE EDAD:")
                rut_ac = input("RUT del Acompañante: ").strip()
                nombre_ac = input("Nombre del Acompañante: ").strip()
                while True:
                    try:
                        edad_ac = int(input("Edad del Acompañante: "))
                        if edad_ac < pelicula_seleccionada.edad_minima or edad_ac < 18:
                            print(f"❌ El acompañante debe tener al menos 18 años y cumplir la edad mínima ({pelicula_seleccionada.edad_minima} años).")
                            continue
                        acompanante = Cliente(rut_ac, nombre_ac if nombre_ac else "Acompañante Adulto", edad_ac)
                        break
                    except ValueError as e:
                        print(f"❌ Error: {e}. Intente nuevamente.")
                
                print(f"✅ Acompañante validado: {acompanante.nombre} ({acompanante.edad} años). Venta autorizada.")
                cliente_para_ticket = acompanante
                es_menor_con_acompanante = True
            else:
                print("\n❌ VENTA CANCELADA: No se permite el ingreso de menores sin un acompañante mayor de edad.")
                return

        # PASO 3: TIPO DE FUNCIÓN
        print("\n🎥 [PASO 3] TIPO DE FUNCIÓN")
        precio_2d_desc = "$4.500 (10% Dcto)" if es_registrado else "$5.000"
        print(f" [1] Función 2D ({precio_2d_desc})")
        print(" [2] Función 3D ($7.000 - Incluye lentes 3D)")
        print(" [3] Función VIP ($10.000 - Asientos Reclinables y Servicio Especial)")
        
        horario = datetime.now()
        precio_base = 5000
        
        while True:
            tipo_f = input("\nElija el tipo de función (1-3): ").strip()
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
                print("⚠️ Opción no válida. Ingrese 1, 2 o 3.")

        print(f"✅ Formato seleccionado: {formato_elegido} (${funcion.calcular_precio():,.0f})")

        # PASO 4: FILTRAR Y SELECCIONAR SALAS CLASIFICADAS SEGÚN LA FUNCIÓN
        print(f"\n🏛️ [PASO 4] SELECCIÓN DE SALAS HABILITADAS PARA FORMATO {formato_elegido}")
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
                print(f"⚠️ La sala {num_sala} no está disponible para formato {formato_elegido}.")
            except ValueError:
                print("⚠️ Debe ingresar un número de sala válido.")

        # PASO 5: DISPONIBILIDAD Y SELECCIÓN DE ASIENTO(S)
        cantidad_entradas = 2 if es_menor_con_acompanante else 1
        
        if es_menor_con_acompanante:
            print(f"\n💡 Dado que asiste con un acompañante adulto, se seleccionarán 2 entradas consecutivas/disponibles.")

        asientos_reservados = []
        venta = Venta("V-101", cliente_para_ticket)

        for n_ent in range(1, cantidad_entradas + 1):
            persona_label = f"Acompañante ({cliente_para_ticket.nombre})" if (es_menor_con_acompanante and n_ent == 1) else f"Menor/Titular ({cliente_titular.nombre})"
            print(f"\n💺 [PASO 5.{n_ent}] SELECCIÓN DE ASIENTO PARA: {persona_label}")
            sala_elegida.mostrar_mapa_asientos()

            while True:
                codigo_asiento = input(f"Ingrese código del asiento {n_ent} (ej: A1, C3, E6): ").strip().upper()
                if sala_elegida.esta_disponible(codigo_asiento):
                    try:
                        entrada = self.boletero.emitir_entrada(cliente_para_ticket, funcion, codigo_asiento)
                        sala_elegida.ocupar_asiento(codigo_asiento)
                        asientos_reservados.append(codigo_asiento)
                        venta.agregar_detalle(entrada, 1)
                        print(f"✅ Asiento {codigo_asiento} reservado con éxito.")
                        break
                    except (EdadInsuficienteError, SalaLlenaError) as err:
                        print(f"❌ Error: {err}")
                        return
                else:
                    print(f"❌ El asiento '{codigo_asiento}' no existe o ya está ocupado. Intente con otro.")

        # DULCERÍA CON ASISTENTE VIRTUAL DE CINE
        print("\n🍿 [PASO 6] ATENCIÓN VIRTUAL DE DULCERÍA")
        print("¿Desea ingresar a la Dulcería del Cine para realizar un pedido? (S/N)")
        if input("Respuesta: ").strip().upper() == "S":
            asistente_dulceria = AsistenteDulceriaCine(self.dulcero)
            asistente_dulceria.atender_pedido(venta)


        # EMITIR COMPROBANTE FINAL
        print("\n" + "=" * 68)
        print(" 🧾 RESUMEN Y COMPROBANTE DE COMPRA")
        print("=" * 68)
        tipo_cliente_str = "Cliente Registrado (10% Dcto 2D Aplicado)" if es_registrado else "Cliente Invitado"
        print(f"Tipo de Acceso: {tipo_cliente_str}")
        print(f"Titular de la Compra: {cliente_titular.nombre} (RUT: {cliente_titular.rut})")
        if es_menor_con_acompanante:
            print(f"Acompañante Responsable: {cliente_para_ticket.nombre} ({cliente_para_ticket.edad} años)")
        print(f"Ubicación: SALA {sala_elegida.numero_sala} ({sala_elegida.formato}) | Asientos: {', '.join(asientos_reservados)}")
        print(venta.emitir_comprobante())
        print("=" * 68)
        print("✨ ¡Disfrute su función en CINEAPP! ✨\n")

if __name__ == "__main__":
    app = SistemaCineCLI()
    app.iniciar()
