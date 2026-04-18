"""
Created on Fri Nov 22 17:07:49 2024

@author: ANGELO
"""

from datetime import datetime

# Clase para los clientes
class Cliente:
    def __init__(self, id_cliente, nombre, contrasena, saldo):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.contrasena = contrasena
        self.saldo = saldo
        self.movimientos = []  # Lista de movimientos

    def __str__(self):
        return f"{self.id_cliente}: {self.nombre} - Saldo: {self.saldo}"


# Clase para los cajeros automáticos
class Cajero:
    def __init__(self, id_cajero, ubicacion):
        self.id_cajero = id_cajero
        self.ubicacion = ubicacion
        self.billetes = {200: 0, 100: 0, 50: 0, 20: 0}  # Denominaciones
        self.movimientos = []  # Movimientos asociados al cajero

    def actualizar_billetes(self, denominacion, cantidad):
        if denominacion in self.billetes:
            self.billetes[denominacion] += cantidad
            self.movimientos.append(
                f"{datetime.now()} - Abastecido con {cantidad} billetes de {denominacion}."
            )
        else:
            print("Denominación inválida")

    def saldo_total(self):
        return sum(denom * cant for denom, cant in self.billetes.items())

    def __str__(self):
        return f"{self.id_cajero} - {self.ubicacion}"


# Funciones auxiliares
def desglose_billetes(monto, billetes_disponibles):
    """Realiza el desglose de billetes para un monto solicitado."""
    desglose = {}
    for denominacion in sorted(billetes_disponibles.keys(), reverse=True):
        if monto == 0:
            break
        cantidad_disponible = billetes_disponibles[denominacion]
        cantidad_necesaria = monto // denominacion
        if cantidad_necesaria > 0:
            cantidad_a_usar = min(cantidad_necesaria, cantidad_disponible)
            desglose[denominacion] = cantidad_a_usar
            monto -= cantidad_a_usar * denominacion
    if monto > 0:
        return None  # No se puede realizar el desglose
    return desglose

# Función para ordenar usando QuickSort
def quicksort(lista, key):
    """Ordena la lista de objetos (clientes o cajeros) por una clave proporcionada."""
    if len(lista) <= 1:
        return lista
    pivot = lista[0]
    less = [x for x in lista[1:] if key(x) < key(pivot)]
    greater = [x for x in lista[1:] if key(x) >= key(pivot)]
    return quicksort(less, key) + [pivot] + quicksort(greater, key)

# Función de búsqueda binaria
def busqueda_binaria(lista, key, target):
    """Realiza una búsqueda binaria en una lista ordenada."""
    low, high = 0, len(lista) - 1
    while low <= high:
        mid = (low + high) // 2
        if key(lista[mid]) == target:
            return lista[mid]
        elif key(lista[mid]) < target:
            low = mid + 1
        else:
            high = mid - 1
    return None  # No se encontró el elemento

def listar_clientes_ordenados(clientes):
    clientes_list = list(clientes.values())
    clientes_list = quicksort(clientes_list, key=lambda cliente: cliente.id_cliente)
    print("\n--- Lista de Clientes (Ordenados) ---")
    for cliente in clientes_list:
        print(cliente)

def listar_cajeros_ordenados(cajeros):
    cajeros_list = list(cajeros.values())
    cajeros_list = quicksort(cajeros_list, key=lambda cajero: cajero.id_cajero)
    print("\n--- Lista de Cajeros (Ordenados) ---")
    for cajero in cajeros_list:
        print(cajero)

def dar_baja_cliente(clientes, id_cliente):
    cliente = busqueda_binaria(list(clientes.values()), key=lambda c: c.id_cliente, target=id_cliente)
    
    if cliente:
        confirmacion = input(f"¿Está seguro de que desea dar de baja al cliente {cliente.nombre}? (s/n): ")
        if confirmacion.lower() == 's':
            del clientes[id_cliente]
            print("Cliente dado de baja correctamente.")
        else:
            print("Operación cancelada.")
    else:
        print("Cliente no encontrado.")

def dar_baja_cajero(cajeros, id_cajero):
    cajero = busqueda_binaria(list(cajeros.values()), key=lambda c: c.id_cajero, target=id_cajero)
    
    if cajero:
        confirmacion = input(f"¿Está seguro de que desea dar de baja al cajero de {cajero.ubicacion}? (s/n): ")
        if confirmacion.lower() == 's':
            del cajeros[id_cajero]
            print("Cajero dado de baja correctamente.")
        else:
            print("Operación cancelada.")
    else:
        print("Cajero no encontrado.")


# Función principal del sistema
def menu_principal():
    clientes = {}  # Diccionario para almacenar clientes
    cajeros = {}  # Diccionario para almacenar cajeros

    while True:
        print("\n--- Sistema de Cajero Automático ---")
        print("1. Registrar cliente")
        print("2. Registrar cajero")
        print("3. Realizar operación")
        print("4. Actualizar cajero")
        print("5. Listar clientes")
        print("6. Listar cajeros")
        print("7. Dar de baja cliente/cajero")
        print("8. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":  # Registrar cliente
            id_cliente = input("ID del cliente: ")
            if id_cliente in clientes:
                print("Error: El ID ya está registrado. Intente con otro ID.")
                continue
            nombre = input("Nombre del cliente: ")
            contrasena = input("Contraseña: ")
            saldo = float(input("Saldo inicial: "))
            clientes[id_cliente] = Cliente(id_cliente, nombre, contrasena, saldo)
            print("Cliente registrado con éxito.")

        elif opcion == "2":  # Registrar cajero
            id_cajero = input("ID del cajero: ")
            if id_cajero in cajeros:
                print("Error: El ID ya está registrado. Intente con otro ID.")
                continue
            ubicacion = input("Ubicación del cajero: ")
            cajeros[id_cajero] = Cajero(id_cajero, ubicacion)
            print("Cajero registrado con éxito.")

        elif opcion == "3":  # Realizar operación
            if not clientes or not cajeros:
                print("Debe haber al menos un cliente y un cajero registrados.")
                continue

            id_cliente = input("Ingrese su ID de cliente: ")
            contrasena = input("Ingrese su contraseña: ")

            if id_cliente not in clientes or clientes[id_cliente].contrasena != contrasena:
                print("ID de cliente o contraseña incorrecta.")
                continue

            cliente = clientes[id_cliente]
            print("\n--- Operaciones ---")
            print("1. Retiro")
            print("2. Depósito")
            print("3. Transferencia")
            print("4. Pago de servicios")
            print("5. Consultar saldo")
            print("6. Consultar movimientos")
            operacion = input("Seleccione una operación: ")

            if operacion == "1":  # Retiro
                id_cajero = input("ID del cajero: ")
                if id_cajero not in cajeros:
                    print("Cajero no encontrado.")
                    continue

                cajero = cajeros[id_cajero]
                monto = int(input("Ingrese el monto a retirar: "))

                if monto > cliente.saldo:
                    print("Saldo insuficiente en su cuenta.")
                    continue

                desglose = desglose_billetes(monto, cajero.billetes)
                if desglose:
                    # Actualizar el cajero y el cliente
                    for denom, cant in desglose.items():
                        cajero.billetes[denom] -= cant
                    cliente.saldo -= monto
                    cliente.movimientos.append(
                        f"{datetime.now()} - Retiro de {monto} exitoso. Desglose: {desglose}"
                    )
                    print("Retiro exitoso. Desglose de billetes:")
                    for denom, cant in desglose.items():
                        print(f"Billetes de {denom}: {cant}")
                else:
                    print("No se puede realizar el retiro. El cajero no tiene suficientes billetes para cubrir el monto.")


            elif operacion == "2":  # Depósito
                id_cajero = input("ID del cajero: ")
                if id_cajero not in cajeros:
                    print("Cajero no encontrado.")
                    continue
                cajero = cajeros[id_cajero]
                billetes_depositados = {}
                for denom in cajero.billetes.keys():
                    cantidad = int(input(f"Cantidad de billetes de {denom}: "))
                    billetes_depositados[denom] = cantidad
                    cajero.billetes[denom] += cantidad
                monto = sum(denom * cant for denom, cant in billetes_depositados.items())
                cliente.saldo += monto
                cliente.movimientos.append(
                    f"{datetime.now()} - Depósito de {monto} exitoso"
                )
                print("Depósito exitoso.")

            elif operacion == "3":  # Transferencia
                while True:
                    id_destinatario = input("Ingrese el ID del cliente destinatario (o '0' para retroceder): ")
                    if id_destinatario == "0":
                        print("Regresando al menú anterior...")
                        break
                    if id_destinatario not in clientes:
                        print("El cliente destinatario no existe. Intente nuevamente.")
                        continue

                    monto = float(input("Ingrese el monto a transferir: "))
                    if monto <= 0:
                        print("El monto debe ser mayor a cero.")
                    elif monto > cliente.saldo:
                        print("Saldo insuficiente para realizar la transferencia.")
                    else:
                        # Transferencia válida
                        cliente_destinatario = clientes[id_destinatario]
                        cliente.saldo -= monto
                        cliente_destinatario.saldo += monto

                        # Registrar movimientos en ambas cuentas
                        cliente.movimientos.append(
                            f"{datetime.now()} - Transferencia enviada de {monto} a {cliente_destinatario.nombre} (ID: {id_destinatario})"
                        )
                        cliente_destinatario.movimientos.append(
                            f"{datetime.now()} - Transferencia recibida de {monto} de {cliente.nombre} (ID: {cliente.id_cliente})"
                        )

                        print(f"Transferencia exitosa. Se transfirieron {monto} a {cliente_destinatario.nombre}.")
                        break

            elif operacion == "4":  # Pago de servicios
                while True:
                    nombre_entidad = input("Ingrese el nombre de la entidad a la que desea pagar (o '0' para retroceder): ")
                    if nombre_entidad == "0":
                        print("Regresando al menú anterior...")
                        break

                    monto = float(input(f"Ingrese el monto a pagar a {nombre_entidad}: "))
                    if monto <= 0:
                        print("El monto debe ser mayor a cero. Intente nuevamente.")
                    elif monto > cliente.saldo:
                        print("Saldo insuficiente para realizar el pago.")
                    else:
                        cliente.saldo -= monto
                        cliente.movimientos.append(
                            f"{datetime.now()} - Pago de servicio: {nombre_entidad} por un monto de {monto:.2f}"
                        )
                        print(f"Pago exitoso. Se ha pagado {monto:.2f} a {nombre_entidad}.")
                        break
            elif operacion == "5":  # Consultar saldo
                print(f"\nSaldo actual: {cliente.saldo:.2f}")

            elif operacion == "6":  # Consultar movimientos
                print("\n--- Movimientos recientes ---")
                if cliente.movimientos:
                    for movimiento in cliente.movimientos[-5:]:  # Últimos 5 movimientos
                        print(f"  - {movimiento}")
                else:
                    print("No hay movimientos registrados.")


        elif opcion == "4":  # Actualizar cajero
            print("\n--- Submenú de Actualización de Cajeros ---")
            print("1. Abastecer cajero")
            print("2. Consultar saldo del cajero")
            print("3. Consultar movimientos del cajero")
            subopcion = input("Seleccione una opción: ")

            id_cajero = input("ID del cajero: ")
            if id_cajero not in cajeros:
                print("Cajero no encontrado.")
                continue

            cajero = cajeros[id_cajero]

            if subopcion == "1":  # Abastecer cajero
                print(f"\n--- Abasteciendo cajero {id_cajero} ---")
                for denom in cajero.billetes.keys():
                    cantidad = int(input(f"Ingrese la cantidad de billetes de {denom}: "))
                    cajero.actualizar_billetes(denom, cantidad)
                print("Cajero abastecido con éxito.")

            elif subopcion == "2":  # Consultar saldo del cajero
                print(f"\nSaldo total en cajero {id_cajero}: {cajero.saldo_total()}")

            elif subopcion == "3":  # Consultar movimientos del cajero
                print(f"\n--- Movimientos del cajero {id_cajero} ---")
                if cajero.movimientos:
                    for movimiento in cajero.movimientos[-5:]:
                        print(f"  - {movimiento}")
                else:
                    print("No hay movimientos registrados para este cajero.")

            else:
                print("Opción no válida en el submenú.")

        elif opcion == "5":  # Listar clientes
            if clientes:
                listar_clientes_ordenados(clientes)
            else:
                print("No hay clientes registrados.")

        elif opcion == "6":  # Listar cajeros
            if cajeros:
                listar_cajeros_ordenados(cajeros)
            else:
                print("No hay cajeros registrados.")


        elif opcion == "7":  # Dar de Baja Cliente/Cajero
            print("\n--- Dar de Baja ---")
            print("1. Dar de Baja Cliente")
            print("2. Dar de Baja Cajero")
            subopcion = input("Seleccione una opción: ")

            if subopcion == "1":  # Dar de Baja Cliente
                id_cliente = input("Ingrese el ID del cliente a dar de baja: ")
                dar_baja_cliente(clientes, id_cliente)  # Llamada a la función para dar de baja al cliente

            elif subopcion == "2":  # Dar de Baja Cajero
                id_cajero = input("Ingrese el ID del cajero a dar de baja: ")
                dar_baja_cajero(cajeros, id_cajero)  # Llamada a la función para dar de baja al cajero

            else:
                print("Opción no válida en el submenú.")

        elif opcion == "8":  # Salir
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


# Ejecución del sistema
menu_principal()
