# Archivo: actividad3.py
#Derek Joan Ramos del Angel
# Descripción:
# Este programa genera y muestra la tabla de Pitágoras (del 1 al 10),
# y luego solicita dos factores al usuario para encontrar el resultado
# de su multiplicación dentro de la tabla, sin usar el operador *.

# --- Generación de la tabla de Pitágoras ---
# La tabla se almacena en una lista de listas (matriz).
tabla = []
for i in range(1, 11):
    fila = []
    for j in range(1, 11):
        fila.append(i * j)
    tabla.append(fila)

# --- Funciones del programa ---

# Función que muestra la tabla de Pitágoras en pantalla.
# No regresa un valor, solo imprime el contenido con formato.
def mostrar_tabla(matriz):
    print("--- Tabla de Pitágoras ---")
    for fila in matriz:
        for numero in fila:
            # Se usa f-string y ':4' para alinear los números con un ancho de 4 caracteres.
            print(f"{numero:4}", end=" ")
        print()  # Salto de línea para la siguiente fila
    print("------------------------")

# Función que realiza la multiplicación de dos números
# buscando el resultado en la tabla.
# Regresa el valor del resultado.
def multiplicar(tabla, num1, num2):
    # Se accede al elemento de la tabla usando los números como índices.
    # Se resta 1 porque los índices de las listas inician en 0.
    resultado = tabla[num1 - 1][num2 - 1]
    return resultado

# --- Lógica principal del programa ---

# 1. Se llama a la función para mostrar la tabla completa.
mostrar_tabla(tabla)

# 2. Se solicitan los dos números al usuario.
# Se convierten los inputs a enteros con int().
num1 = int(input("Ingresa el primer número (1-10): "))
num2 = int(input("Ingresa el segundo número (1-10): "))

# 3. VERIFICACIÓN: Se comprueba que los números estén en el rango válido.
# Si el usuario ingresa un número mayor a 10 o menor a 1, se muestra un mensaje de error.
if num1 > 10 or num2 > 10 or num1 < 1 or num2 < 1:
    print("Error: Los números deben estar entre 1 y 10.")
else:
    # 4. Si los números son válidos, se llama a la función de multiplicación y se guarda el resultado.
    resultado_multiplicacion = multiplicar(tabla, num1, num2)

    # 5. Se muestra el resultado final en pantalla.
    print(f"El resultado de la multiplicación de {num1} y {num2} es: {resultado_multiplicacion}")
