precio_menor = 30
precio_mayor = 45
precio_menor3 = 0

descuentos = {
    "Adulto Mayor": 12,
    "Profesor": 10,
    "Estudiante": 10
}
print("Bienvenidos al Museo de Antropología e Historia\n")
numero_visitantes = int(input("¿Cuántos visitantes pagarán boleto? "))
total_a_pagar = 0
for i in range(numero_visitantes):
    print(f"\nVisitante #{i + 1}")

    menor3 = input("¿Es menor de 3 años? (S/N): ").strip().upper()
    if menor3 == "S":
        precio = precio_menor3
        print(f"No paga boleto. Precio: ${precio}")
        total_a_pagar += precio
        continue

    menor18 = input("¿Es menor de 18 años? (S/N): ").strip().upper()
    if menor18 == "S":
        precio = precio_menor
    else:
        precio = precio_mayor

    tipo_visitante = input("¿Es Adulto Mayor, Profesor, Estudiante o Ninguno? ").strip().title()

    if tipo_visitante == "Salir":
        print("Venta cancelada.")
        break

    descuento = descuentos.get(tipo_visitante, 0)
    precio_final = precio * (1 - descuento / 100)
    print(f"Precio a pagar con descuento: ${precio_final:.2f}")

    total_a_pagar += precio_final

print(f"\nTotal a pagar por todos los visitantes: ${total_a_pagar:.2f}")