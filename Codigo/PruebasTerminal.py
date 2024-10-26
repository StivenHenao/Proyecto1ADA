'''
Proyecto 1 - PruebasTerminal.py
Descripción: Este script contiene pruebas de tiempo de ejecución para las soluciones ingenua, dinámica y voraz del problema de la terminal inteligente.
Autores:
            Rodas Arango, Juan Manuel - 2259571
            García Castañeda, Alex - 2259517
            Gómez Agudelo, Juan Sebastián - 2259474
            Henao Aricapa, Stiven - 2259603
Docente:
            Delgado Saavedra, Carlos Andrés
Fecha: 2024-10-25
'''

import timeit
import time
import matplotlib.pyplot as plt
from TerminalInteligente import solucion_ingenua, solucion_dinamica, solucion_voraz, costos_global


# Función para medir el tiempo de ejecución
def medir_tiempo(funcion, *args):
    inicio = time.time()
    funcion(*args)
    fin = time.time()
    return fin - inicio

# Ejemplo de cadenas para probar
casos = [
    ("a", "b"),                    # Caso 1: Cadenas muy cortas
    ("algoritmo", "algoritmos"),    # Caso 2: Una letra más
    ("francesa", "ancestro"),       # Caso 3: Transformación moderada
    ("ingenioso", "ingeniero"),     # Caso 4: Transformación significativa
    ("comunicacion", "comunicacion"), # Caso 5: Cadenas iguales
    ("algorithm", "altruistic"),    # Caso 6: Ejemplo inicial
    ("aaaaaaaaa", "bbbbbbbbb"), # Caso 7: Cadenas muy largas con letras repetidas
    #("nos fuimos a paro", "orap a somiuf son") # Caso 8: Cadenas medianas invertidas
    #("establecimiento", "desestablecimiento"), # Caso 9: Transformación moderada
    ("abcdefghij", "jihgfedcba") # Caso 10: Cadenas muy largas invertidas
]


# Resultados para cada algoritmo
tiempos_ingenuo = []
tiempos_dinamico = []
tiempos_voraz = []

# Ejecuciones múltiples para promediar
n_ejecuciones = 50

for cadena_inicial, cadena_final in casos:
    # Medir tiempo para solución ingenua
    tiempo_total_ingenuo = sum(medir_tiempo(solucion_ingenua, cadena_inicial, cadena_final, 0, costos_global, []) for _ in range(n_ejecuciones))
    tiempos_ingenuo.append(tiempo_total_ingenuo / n_ejecuciones)

    # Medir tiempo para solución dinámica
    tiempo_total_dinamico = sum(medir_tiempo(solucion_dinamica, cadena_inicial, cadena_final, costos_global) for _ in range(n_ejecuciones))
    tiempos_dinamico.append(tiempo_total_dinamico / n_ejecuciones)

    # Medir tiempo para solución voraz
    tiempo_total_voraz = sum(medir_tiempo(solucion_voraz, cadena_inicial, cadena_final, costos_global) for _ in range(n_ejecuciones))
    tiempos_voraz.append(tiempo_total_voraz / n_ejecuciones)

# Mostrar resultados
print("Tiempos promedio (en segundos):")
for i, (cadena_inicial, cadena_final) in enumerate(casos):
    print(f"{cadena_inicial} -> {cadena_final}: Ingenuo: {tiempos_ingenuo[i]:.10f}, Dinámico: {tiempos_dinamico[i]:.10f}, Voraz: {tiempos_voraz[i]:.10f}")



# Graficar resultados
plt.figure(figsize=(10, 6))
plt.plot([str(c[0]) + " -> " + str(c[1]) for c in casos], tiempos_ingenuo, marker='o', label='Ingenuo')
plt.plot([str(c[0]) + " -> " + str(c[1]) for c in casos], tiempos_dinamico, marker='o', label='Dinámico')
plt.plot([str(c[0]) + " -> " + str(c[1]) for c in casos], tiempos_voraz, marker='o', label='Voraz')

plt.title('Comparación de Tiempos de Ejecución')
plt.xlabel('Casos de Prueba')
plt.ylabel('Tiempo Promedio (s)')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# Test con Timeit
# ------------------------------------------------------------


# Funciones para medir el tiempo de ejecución de cada solución
def medir_tiempo_ingenua():
    setup = "from TerminalInteligente import solucion_ingenua , costos_global"
    tiempo1 = timeit.timeit("solucion_ingenua('a', 'b', 0, costos_global, [])", setup=setup, number=50)
    tiempo2 = timeit.timeit("solucion_ingenua('algoritmo', 'algoritmos', 0, costos_global, [])", setup=setup, number=50)
    tiempo3 = timeit.timeit("solucion_ingenua('francesa', 'ancestro', 0, costos_global, [])", setup=setup, number=50)
    tiempo4 = timeit.timeit("solucion_ingenua('ingenioso', 'ingeniero', 0, costos_global, [])", setup=setup, number=50)
    tiempo5 = timeit.timeit("solucion_ingenua('comunicacion', 'comunicacion', 0, costos_global, [])", setup=setup, number=50)
    tiempo6 = timeit.timeit("solucion_ingenua('algorithm', 'altruistic', 0, costos_global, [])", setup=setup, number=50)
    tiempo7 = timeit.timeit("solucion_ingenua('aaaaaaa', 'bbbbbbb', 0, costos_global, [])", setup=setup, number=50)
    tiempo8 = timeit.timeit("solucion_ingenua('abcdefghij', 'jihgfedcba', 0, costos_global, [])", setup=setup, number=50)
    return tiempo1 + tiempo2 + tiempo3 + tiempo4 + tiempo5 + tiempo6 + tiempo7 + tiempo8 / 50

def medir_tiempo_dinamica():
    setup = "from TerminalInteligente import solucion_dinamica, costos_global"
    tiempo1 = timeit.timeit("solucion_dinamica('a', 'b', costos_global)", setup=setup, number=50)
    tiempo2 = timeit.timeit("solucion_dinamica('algoritmo', 'algoritmos',costos_global)", setup=setup, number=50)
    tiempo3 = timeit.timeit("solucion_dinamica('francesa', 'ancestro', costos_global)", setup=setup, number=50)
    tiempo4 = timeit.timeit("solucion_dinamica('ingenioso', 'ingeniero', costos_global)", setup=setup, number=50)
    tiempo5 = timeit.timeit("solucion_dinamica('comunicacion', 'comunicacion', costos_global)", setup=setup, number=50)
    tiempo6 = timeit.timeit("solucion_dinamica('algorithm', 'altruistic', costos_global)", setup=setup, number=50)
    tiempo7 = timeit.timeit("solucion_dinamica('aaaaaaa', 'bbbbbbb', costos_global)", setup=setup, number=50)
    tiempo8 = timeit.timeit("solucion_dinamica('abcdefghij', 'jihgfedcba', costos_global)", setup=setup, number=50)
    return tiempo1 + tiempo2 + tiempo3 + tiempo4 + tiempo5 + tiempo6 + tiempo7 + tiempo8 / 50

def medir_tiempo_voraz():
    setup = "from TerminalInteligente import solucion_voraz, costos_global"
    tiempo1 = timeit.timeit("solucion_voraz('a', 'b', costos_global)", setup=setup, number=50)
    tiempo2 = timeit.timeit("solucion_voraz('algoritmo', 'algoritmos', costos_global)", setup=setup, number=50)
    tiempo3 = timeit.timeit("solucion_voraz('francesa', 'ancestro', costos_global)", setup=setup, number=50)
    tiempo4 = timeit.timeit("solucion_voraz('ingenioso', 'ingeniero', costos_global)", setup=setup, number=50)
    tiempo5 = timeit.timeit("solucion_voraz('comunicacion', 'comunicacion', costos_global)", setup=setup, number=50)
    tiempo6 = timeit.timeit("solucion_voraz('algorithm', 'altruistic', costos_global)", setup=setup, number=50)
    tiempo7 = timeit.timeit("solucion_voraz('aaaaaaa', 'bbbbbbb', costos_global)", setup=setup, number=50)
    tiempo8 = timeit.timeit("solucion_voraz('abcdefghij', 'jihgfedcba', costos_global)", setup=setup, number=50)
    return tiempo1 + tiempo2 + tiempo3 + tiempo4 + tiempo5 + tiempo6 + tiempo7 + tiempo8 / 50

# Realizar mediciones
tiempos_ingenua = medir_tiempo_ingenua()
tiempos_dinamica = medir_tiempo_dinamica()
tiempos_voraz = medir_tiempo_voraz()

print(f"Tiempo promedio (ingenua): {tiempos_ingenua}")
print(f"Tiempo promedio (dinámica): {tiempos_dinamica}")
print(f"Tiempo promedio (voraz): {tiempos_voraz}")

# Gráfica de comparación de tiempos
metodos = ['Ingenua', 'Dinámica', 'Voraz']
tiempos = [tiempos_ingenua, tiempos_dinamica, tiempos_voraz]

plt.bar(metodos, tiempos, color=['blue', 'orange', 'green'])
plt.xlabel('Método')
plt.ylabel('Tiempo Promedio (segundos)')
plt.title('Comparación de Tiempos de Ejecución')
plt.show()
