# Actividad 4

# --- SECCIÓN DE FUNCIONES ---
# todas las funciones creadas
# para que el menú principal pueda llamarlas desde cualquier lugar.

def contar_palabras(mensaje_a_contar):
    """Recibe un string y retorna la cantidad de palabras que contiene."""
    lista_palabras = mensaje_a_contar.split()
    cantidad_palabras = len(lista_palabras)
    return cantidad_palabras

def sumar_tupla_numeros(tupla_a_sumar):
    """Recibe una tupla de números y retorna la suma de sus elementos."""
    try:
        resultado_suma = sum(tupla_a_sumar)
        return resultado_suma
    except TypeError:
        return "Error: No se pueden sumar elementos de texto. Este es el error esperado."
        
def buscar_contacto(contactos, nombre):
    """Recibe un diccionario y un nombre y retorna el número de teléfono."""
    try:
        return contactos[nombre]
    except KeyError:
        return "Contacto no encontrado."


# --- MENÚ PRINCIPAL DEL PROGRAMA ---
# Este bucle permite que el usuario interactúe con el programa hasta que decida salir.
while True:
    print("\n--- Menú Principal ---")
    print("1. Manipular Tuplas")
    print("2. Usar Diccionarios")
    print("3. Manejar Excepciones")
    print("4. Manipular Strings")
    print("5. Salir")
    
    opcion = input("Seleccione una opción (1-5): ")
    
    # --- Bloque 1: Manipular Tuplas ---
    if opcion == '1':
        print("\n--- Sección de Tuplas ---")
        
        # 1. Uso de tuplas
        frutas = ("naranja", "manzana", "sandia", "platano", "uva")
        print(f"La tupla original es: {frutas}")
        print(f"El tercer elemento de la tupla es: {frutas[2]}")
        
        frutas_lista = list(frutas)
        print("Tupla convertida a lista:", frutas_lista)
        
        fruta_nueva_1 = input("Ingresa la primera fruta adicional: ")
        fruta_nueva_2 = input("Ingresa la segunda fruta adicional: ")
        frutas_lista.append(fruta_nueva_1)
        frutas_lista.append(fruta_nueva_2)
        fru_tupla_nueva = tuple(frutas_lista)
        print("Nueva tupla con frutas añadidas:", fru_tupla_nueva)
        
        # 2. Convierte la tupla a lista y ordena
        frutas_ordenadas = list(fru_tupla_nueva)
        frutas_ordenadas.sort()
        print("Lista de frutas ordenada alfabéticamente:", frutas_ordenadas)
        
        # 3. Aplica la función de suma a la tupla de frutas (causará un TypeError intencional)
        print("\nAhora aplicaremos la función 'sumar_tupla_numeros' a la tupla de frutas.")
        suma_tupla = sumar_tupla_numeros(fru_tupla_nueva)
        print(suma_tupla)

    # --- Bloque 2: Usar Diccionarios ---
    elif opcion == '2':
        print("\n--- Sección de Diccionarios ---")
        
        # 1. Crea y agrega un contacto
        contactos = {
            "derek": 1234567890,
            "juan": 1234567891,
            "jose": 1234567892,
        }
        print("Diccionario de contactos inicial:", contactos)
        # Pide al usuario el nombre y el número del nuevo contacto
        print("\nAhora puedes agregar un nuevo contacto:")
        nombre_nuevo = input("Ingresa el nombre del nuevo contacto: ")
        numero_nuevo = int(input("Ingresa el número de teléfono: "))

        # Agrega el nuevo contacto al diccionario
        contactos[nombre_nuevo] = numero_nuevo
        print("Nuevo contacto añadido:", contactos)

        # 2. Itera sobre las claves e imprime
        print("\nClaves (nombres) de los contactos:")
        for contac in contactos:
            print(contac)

        # 3. Aplica la función de búsqueda
        print("\nAhora buscaremos un contacto.")
        nombre_a_buscar = input("¿A quién quisieras buscar?: ")
        busqueda_contactos = buscar_contacto(contactos, nombre_a_buscar)
        print(f"El número de {nombre_a_buscar} es {busqueda_contactos}")

    # --- Bloque 3: Manejar Excepciones ---
    elif opcion == '3':
        print("\n--- Sección de Excepciones ---")
        
        # 1: Suma de números enteros
        try:
            print("\n- Prueba de suma de números -")
            numero_entero1 = int(input("Por favor ingresa un número entero: "))
            numero_entero2 = int(input("Por favor ingresa otro número entero: "))
            suma_numeros_enteros = numero_entero1 + numero_entero2
            print(f"La suma es: {suma_numeros_enteros}")
        except ValueError:
            print("¡Error! Por favor, asegúrate de que el número sea un número entero.")

        # 2: División de números enteros
        try:
            print("\n- Prueba de división de números -")
            numero_entero3 = int(input("Por favor ingresa un número entero para dividir: "))
            numero_entero4 = int(input("Por favor ingresa otro número entero para dividir: "))
            divison_numeros_enteros = numero_entero3 / numero_entero4
            print(f"La división es: {divison_numeros_enteros}")
        except ValueError:
            print("¡Error! Por favor, asegúrate de que el número sea un número entero.")
        except ZeroDivisionError:
            print("¡Error! El número no se puede dividir entre 0.")

    # --- Bloque 4: Manipular Strings ---
    elif opcion == '4':
        print("\n--- Sección de Strings ---")
        
        # 1. Crea y manipula el string
        mensaje = "Expedition 33 se merece el GOTY"
        print(f"Mensaje original: '{mensaje}'")
        print(f"La longitud del mensaje es: {len(mensaje)}")
        
        mensaje_mayus = mensaje.upper()
        print(f"Mensaje en mayúsculas: '{mensaje_mayus}'")
        
        mensaje_reemplazar = mensaje_mayus.replace("GOTY", "Juego del año")
        print(f"Mensaje con palabra reemplazada: '{mensaje_reemplazar}'")

        # 2. Aplica la función para contar palabras
        palabras_en_mensaje = contar_palabras(mensaje)
        print(f"La cantidad de palabras en el mensaje es: {palabras_en_mensaje}")

    # --- Bloque 5: Salir ---
    elif opcion == '5':
        print("\nSaliendo del programa. ¡Hasta luego!")
        break

    # --- Opción no válida ---
    else:
        print("\nOpción no válida. Por favor, ingrese un número del 1 al 5.")
