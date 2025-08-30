# Lista para almacenar los subtotales de las ventas del día
# Cada elemento de la lista será un número flotante (float)
ventas_del_dia = [] 

# Bucle principal del programa: se ejecutará continuamente hasta que el usuario decida salir
while True:
    # Mostrar el menú de opciones al usuario
    print("\n--- Sistema de Registro de Ventas ---")
    print("1. Registrar nueva venta")
    print("2. Ver reporte de ventas del día")
    print("3. Salir")
    
    # Solicitar al usuario que ingrese una opción
    opcion = input("Seleccione una opción: ")
    
    # --- Lógica para la opción 1: Registrar nueva venta ---
    if opcion == '1':
        print("\n--- Registrar Nueva Venta ---")
        # Solicitar el nombre del producto
        nombre_producto = input("Ingrese el nombre del producto: ")
        
        # Solicitar el precio y convertirlo a float para manejar decimales
        # Se asume que el usuario ingresará un número válido
        precio_venta_str = input(f"¿Cuál es el precio de '{nombre_producto}'? ")
        precio_venta = float(precio_venta_str) # Convertir la cadena a número flotante
        
        # Solicitar la cantidad
        cantidad_venta_str = input(f"¿Qué cantidad de '{nombre_producto}' se vendió? ")
        
        # Preguntar si la cantidad es por unidades o por peso para la conversión de tipo
        tipo_cantidad = input("¿La cantidad es por unidades (u) o por peso (p)? ").lower()
        
        # Convertir la cantidad al tipo adecuado (int o float)
        cantidad_final = 0 # Inicializar para asegurar que tiene un valor
        if tipo_cantidad == 'u':
            cantidad_final = int(cantidad_venta_str) # Cantidad entera (ej. 2 unidades)
        elif tipo_cantidad == 'p':
            cantidad_final = float(cantidad_venta_str) # Cantidad decimal (ej. 1.5 kg)
        else:
            # Si la entrada no es 'u' ni 'p', se asume unidades y se notifica al usuario
            print("Tipo de cantidad no reconocido. Se asumirá unidades.")
            cantidad_final = int(cantidad_venta_str) 
            
        # Calcular el subtotal de la venta
        subtotal = precio_venta * cantidad_final
        
        # Guardar el subtotal en la lista de ventas del día
        ventas_del_dia.append(subtotal)
        print(f"Venta de '{nombre_producto}' registrada con un subtotal de ${subtotal:.2f}.")
    
    # --- Lógica para la opción 2: Ver reporte de ventas del día ---
    elif opcion == '2':
        print("\n--- Reporte de Ventas del Día ---")
        if not ventas_del_dia: # Comprobar si la lista de ventas está vacía
            print("No hay ventas registradas para el día.")
        else:
            total_del_dia = 0 # Inicializar el total antes de sumarlo
            # Iterar sobre cada subtotal en la lista y sumarlo al total
            for venta in ventas_del_dia:
                total_del_dia += venta 
            
            # Imprimir el total de ventas del día, formateado a dos decimales
            print(f"Total vendido en el día: ${total_del_dia:.2f}")
    
    # --- Lógica para la opción 3: Salir del programa ---
    elif opcion == '3':
        print("Saliendo del Sistema de Registro de Ventas. ¡Hasta luego!")
        break # Rompe el bucle 'while True' para terminar el programa
        
    # --- Lógica para opciones no válidas ---
    else:
        print("Opción no válida. Por favor, ingrese 1, 2 o 3.")

