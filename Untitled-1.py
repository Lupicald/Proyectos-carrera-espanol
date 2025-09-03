# Primero, se crea la tabla de Pitágoras y se guarda en una lista de listas.
tabla = []
for i in range(1, 11):
    fila = []
    for j in range(1, 11):
        fila.append(i * j)
    tabla.append(fila)

# Después, se define la función que va a mostrar la tabla en pantalla sin corchetes ni comas.
def mostrar_tabla(matriz):
    print("--- Tabla de Pitágoras ---")
    for fila in matriz:
        for numero in fila:
            print(f"{numero:4}", end=" ")
        print()
    print("------------------------")

# Luego, se define la función que realiza la multiplicación
# buscando el resultado en la tabla.
def multiplicar(tabla, num1, num2):
    resultado = tabla[num1 - 1][num2 - 1]
    return resultado

# A partir de aquí, el programa empieza a ejecutar las acciones.

# 1. Se llama a la función para mostrar la tabla completa.
mostrar_tabla(tabla)

# 2. Se solicitan los dos números al usuario.
num1 = int(input("Ingresa el primer número (1-10): "))
num2 = int(input("Ingresa el segundo número (1-10): "))

# 3. Se llama a la función de multiplicación y se guarda el resultado.
resultado_multiplicacion = multiplicar(tabla, num1, num2)

# 4. Se muestra el resultado final en pantalla.
print (f"El resultado de la multiplicación es:{resultado_multiplicacion} ")
