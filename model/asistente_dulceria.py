from model.producto_nacional import ProductoNacional

class AsistenteDulceriaCine:
    """
    Asistente Virtual de la Dulcería del Cine.
    Atiende al cliente ofreciendo menú completo: Palomitas, Bebidas y Extras,
    confirmando tamaños/sabores y ofreciendo ventas cruzadas (upselling).
    """
    def __init__(self, encargado_dulceria):
        self.encargado = encargado_dulceria
        self._contador_item = 100

    def _generar_id(self, prefijo="DUL"):
        self._contador_item += 1
        return f"{prefijo}-{self._contador_item}"

    def atender_pedido(self, venta):
        print("\n" + "=" * 60)
        print(" 🍿 ¡HOLA! SOY TU ASISTENTE VIRTUAL DE LA DULCERÍA DE CINEAPP 🥤")
        print(" ¿En qué puedo ayudarte hoy? ¡Tenemos las mejores golosinas!")
        print("=" * 60)

        items_pedidos = []

        # 1. PALOMITAS
        print("\n🍿 ¿Deseas llevar PALOMITAS? (S/N)")
        if input("Respuesta: ").strip().upper() == "S":
            print("\n  Formatos disponibles: [1] Mediano ($3.000) | [2] Grande ($4.000) | [3] Balde ($5.500)")
            t_sel = input("  Elija tamaño (1-3): ").strip()
            tamano_map = {"1": ("Mediano", 3000), "2": ("Grande", 4000), "3": ("Balde", 5500)}
            tam_nombre, tam_precio = tamano_map.get(t_sel, ("Grande", 4000))

            print("\n  Sabores disponibles: [1] Saladas | [2] Caramelo | [3] Mixtas")
            s_sel = input("  Elija sabor (1-3): ").strip()
            sabor_map = {"1": "Saladas", "2": "Caramelo", "3": "Mixtas"}
            sabor_nombre = sabor_map.get(s_sel, "Saladas")

            desc = f"Palomitas ({tam_nombre} - {sabor_nombre})"
            item_id = self._generar_id("PAL")
            prod = ProductoNacional(item_id, desc, stock=50, precio_pesos=tam_precio)
            self.encargado.registrar_venta_dulceria(venta, prod, 1)
            items_pedidos.append(f"• 1x {desc} -> ${tam_precio:,.0f}")
            print(f"  ✅ Agregado: {desc}")

        # 2. BEBIDAS
        print("\n🥤 ¿Deseas agregar BEBIDAS? (S/N)")
        if input("Respuesta: ").strip().upper() == "S":
            print("\n  Opciones: [1] Coca-Cola | [2] Sprite | [3] Fanta | [4] Agua")
            b_sel = input("  Elija variedad (1-4): ").strip()
            bebida_map = {"1": "Coca-Cola", "2": "Sprite", "3": "Fanta", "4": "Agua"}
            bebida_nombre = bebida_map.get(b_sel, "Coca-Cola")

            print("\n  Tamaños: [1] Mediano ($2.000) | [2] Grande ($2.800)")
            tb_sel = input("  Elija tamaño (1-2): ").strip()
            tb_map = {"1": ("Mediano", 2000), "2": ("Grande", 2800)}
            tb_nombre, tb_precio = tb_map.get(tb_sel, ("Grande", 2800))

            desc = f"Bebida {bebida_nombre} ({tb_nombre})"
            item_id = self._generar_id("BEB")
            prod = ProductoNacional(item_id, desc, stock=50, precio_pesos=tb_precio)
            self.encargado.registrar_venta_dulceria(venta, prod, 1)
            items_pedidos.append(f"• 1x {desc} -> ${tb_precio:,.0f}")
            print(f"  ✅ Agregado: {desc}")

        # 3. OFRECER UN EXTRA RÁPIDO (UP-SELLING)
        print("\n🍫 ¿Deseas agregar un EXTRA rápido para acompañar tu película?")
        print("  [1] Nachos con Queso ($3.500)")
        print("  [2] Hot Dogs ($3.000)")
        print("  [3] Gomitas ($1.800)")
        print("  [4] M&M's ($2.200)")
        print("  [5] No gracias, cerrar pedido")
        
        ex_sel = input("  Selección (1-5): ").strip()
        extra_map = {
            "1": ("Nachos con Queso", 3500),
            "2": ("Hot Dogs", 3000),
            "3": ("Gomitas", 1800),
            "4": ("M&M's", 2200)
        }
        if ex_sel in extra_map:
            ex_nombre, ex_precio = extra_map[ex_sel]
            desc = f"Extra: {ex_nombre}"
            item_id = self._generar_id("EXT")
            prod = ProductoNacional(item_id, desc, stock=50, precio_pesos=ex_precio)
            self.encargado.registrar_venta_dulceria(venta, prod, 1)
            items_pedidos.append(f"• 1x {desc} -> ${ex_precio:,.0f}")
            print(f"  ✅ Agregado: {desc}")

        # RESUMEN FINAL DE ATENCIÓN DE DULCERÍA
        print("\n" + "=" * 60)
        print(" 📋 RESUMEN DE TU PEDIDO EN DULCERÍA")
        print("=" * 60)
        if items_pedidos:
            for item in items_pedidos:
                print(f" {item}")
            print(" ¡Pedido procesado exitosamente por el Asistente Virtual!")
        else:
            print(" No se agregaron productos de dulcería a esta compra.")
        print("=" * 60 + "\n")
