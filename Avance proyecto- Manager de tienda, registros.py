# Lista para almacenar las ventas del día
ventas_del_dia = [] 

# Bucle principal del programa
while True:
    print("\n--- Sistema de Registro de Ventas ---")
    print("1. Registrar nueva venta")
    print("2. Ver reporte de ventas del día")
    print("3. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == '1':
        # Código para registrar venta
        nueva_venta= input("¿Qué venta quisieras agregar?")
        precio_venta= input("¿Cuál es el precio de este artículo que se vendió?")
        cantidad_venta =input("¿Qué cantidad de este artículo se vendió?")
        tipo_cantidad = input("¿La cantidad es por unidades (u) o por peso (p)? ").lower()
        if tipo_cantidad == 'u':
            cantidad_final = int(cantidad_venta)
        elif tipo_cantidad == 'p':
            cantidad_final = float(cantidad_venta)
        else:
            print("Tipo de cantidad no reconocido. Se asumirá unidades.")
            cantidad_final = int(cantidad_venta)
        subtotal = float(precio_venta) * (cantidad_final)
        ventas_del_dia.append(subtotal)
    
    elif opcion == '2':
        # Código para ver el reporte
        total_del_dia = 0 
        for venta in ventas_del_dia:
            total_del_dia += venta
        print(f"\n--- Reporte de Ventas del Día ---")
        print(f"Total vendido: ${total_del_dia:.2f}") 
        
    elif opcion == '3':
        print("Saliendo del programa. ¡Hasta luego!")
        break

    else:
        print("Opción no válida. Por favor, intente de nuevo.")