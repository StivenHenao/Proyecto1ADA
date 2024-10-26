'''
Proyecto 1 - TPruebasSubasta.py
Descripción: Este script contiene pruebas de tiempo de ejecución para las soluciones ingenua, dinámica y voraz del problema de la subasta pública.
Autores:
            Rodas Arango, Juan Manuel - 2259571
            García Castañeda, Alex - 2259517
            Gómez Agudelo, Juan Sebastián - 2259474
            Henao Aricapa, Stiven - 2259603
Docente:
            Delgado Saavedra, Carlos Andrés
Fecha: 2024-10-25
'''

import time
import timeit
import matplotlib.pyplot as plt
from SubastaPublica import fuerza_bruta, programacion_dinamica, voraz

# Función para medir el tiempo de ejecución
def medir_tiempo(funcion, *args):
    inicio = time.time()
    funcion(*args)
    fin = time.time()
    return fin - inicio

# Ejemplo de subastas con más propuestas para probar
casos = [
    (300, [(250, 100, 150), (180, 50, 200)], 200), # Caso 1: Una oferta mayor y otra menor al precio del gobierno
    (400, [(150, 50, 200), (200, 100, 250)], 500), # Caso 2: Ambas ofertas menores al precio del gobierno
    (500, [(300, 50, 200), (400, 100, 300), (350, 50, 150)], 100),  # Caso 3: Precio del gobierno menor al de todas las ofertas
    (500, [(200, 50, 200), (300, 100, 250), (400, 150, 300)], 250),  # Caso 4: Solo una oferta mayor al precio del gobierno
    (600, [(200, 100, 250), (300, 100, 350), (120, 50, 200)], 150)  # Caso 5: Algunas ofertas son mayores y otras menores al precio del gobierno
]


# Resultados para cada algoritmo
tiempos_fuerza_bruta = []
tiempos_dinamico = []
tiempos_voraz = []

# Ejecuciones múltiples para promediar
n_ejecuciones = 50

for A, ofertas, precio_gobierno in casos:
    # Medir tiempo para solución fuerza bruta
    tiempo_total_fuerza_bruta = sum(medir_tiempo(fuerza_bruta, A, ofertas, precio_gobierno) for _ in range(n_ejecuciones))
    tiempos_fuerza_bruta.append(tiempo_total_fuerza_bruta / n_ejecuciones)

    # Medir tiempo para solución dinámica
    tiempo_total_dinamico = sum(medir_tiempo(programacion_dinamica, A, ofertas, precio_gobierno) for _ in range(n_ejecuciones))
    tiempos_dinamico.append(tiempo_total_dinamico / n_ejecuciones)

    # Medir tiempo para solución voraz
    tiempo_total_voraz = sum(medir_tiempo(voraz, A, ofertas, precio_gobierno) for _ in range(n_ejecuciones))
    tiempos_voraz.append(tiempo_total_voraz / n_ejecuciones)

# Mostrar resultados
print("Tiempos promedio (en segundos):")
for i, (A, ofertas, precio_gobierno) in enumerate(casos):
    print(f"Subasta {i + 1}: Fuerza Bruta: {tiempos_fuerza_bruta[i]:.10f}, Dinámico: {tiempos_dinamico[i]:.10f}, Voraz: {tiempos_voraz[i]:.10f}")

# Graficar resultados
plt.figure(figsize=(10, 6))
plt.plot([f"Subasta {i + 1}" for i in range(len(casos))], tiempos_fuerza_bruta, marker='o', label='Fuerza Bruta')
plt.plot([f"Subasta {i + 1}" for i in range(len(casos))], tiempos_dinamico, marker='o', label='Dinámico')
plt.plot([f"Subasta {i + 1}" for i in range(len(casos))], tiempos_voraz, marker='o', label='Voraz')

plt.title('Comparación de Tiempos de Ejecución para Subastas (Time)')
plt.xlabel('Casos de Subasta')
plt.ylabel('Tiempo Promedio (s)')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# Test con Timeit
# ------------------------------------------------------------

# Funciones para medir el tiempo de ejecución de cada solución con timeit
def medir_tiempo_fuerza_bruta():
    setup = "from SubastaPublica import fuerza_bruta"
    tiempo1 = timeit.timeit("fuerza_bruta(300, [(250, 100, 150), (180, 50, 200)], 200)", setup=setup, number=50)
    tiempo2 = timeit.timeit("fuerza_bruta(400, [(150, 50, 200), (200, 100, 250)], 500)", setup=setup, number=50)
    tiempo3 = timeit.timeit("fuerza_bruta(500, [(300, 50, 200), (400, 100, 300), (350, 50, 150)], 100)", setup=setup, number=50)
    tiempo4 = timeit.timeit("fuerza_bruta(500, [(200, 50, 200), (300, 100, 250), (400, 150, 300)], 250)", setup=setup, number=50)
    tiempo5 = timeit.timeit("fuerza_bruta(600, [(200, 100, 250), (300, 100, 350), (120, 50, 200)], 150)", setup=setup, number=50)
    return tiempo1 + tiempo2 + tiempo3 + tiempo4 + tiempo5 / 50

def medir_tiempo_dinamico():
    setup = "from SubastaPublica import programacion_dinamica"
    tiempo1 = timeit.timeit("programacion_dinamica(300, [(250, 100, 150), (180, 50, 200)], 200)", setup=setup, number=50)
    tiempo2 = timeit.timeit("programacion_dinamica(400, [(150, 50, 200), (200, 100, 250)], 500)", setup=setup, number=50)
    tiempo3 = timeit.timeit("programacion_dinamica(500, [(300, 50, 200), (400, 100, 300), (350, 50, 150)], 100)", setup=setup, number=50)
    tiempo4 = timeit.timeit("programacion_dinamica(500, [(200, 50, 200), (300, 100, 250), (400, 150, 300)], 250)", setup=setup, number=50)
    tiempo5 = timeit.timeit("programacion_dinamica(600, [(200, 100, 250), (300, 100, 350), (120, 50, 200)], 150)", setup=setup, number=50)
    return tiempo1 + tiempo2 + tiempo3 + tiempo4 + tiempo5 / 50

def medir_tiempo_voraz():
    setup = "from SubastaPublica import voraz"
    tiempo1 = timeit.timeit("voraz(300, [(250, 100, 150), (180, 50, 200)], 200)", setup=setup, number=50)
    tiempo2 = timeit.timeit("voraz(400, [(150, 50, 200), (200, 100, 250)], 500)", setup=setup, number=50)
    tiempo3 = timeit.timeit("voraz(500, [(300, 50, 200), (400, 100, 300), (350, 50, 150)], 100)", setup=setup, number=50)
    tiempo4 = timeit.timeit("voraz(500, [(200, 50, 200), (300, 100, 250), (400, 150, 300)], 250)", setup=setup, number=50)
    tiempo5 = timeit.timeit("voraz(600, [(200, 100, 250), (300, 100, 350), (120, 50, 200)], 150)", setup=setup, number=50)
    return tiempo1 + tiempo2 + tiempo3 + tiempo4 + tiempo5 / 50

# Realizar mediciones con timeit
tiempos_fuerza_bruta_timeit = medir_tiempo_fuerza_bruta()
tiempos_dinamico_timeit = medir_tiempo_dinamico()
tiempos_voraz_timeit = medir_tiempo_voraz()

print(f"Tiempo promedio con timeit (fuerza bruta): {tiempos_fuerza_bruta_timeit}")
print(f"Tiempo promedio con timeit (dinámica): {tiempos_dinamico_timeit}")
print(f"Tiempo promedio con timeit (voraz): {tiempos_voraz_timeit}")

# Graficar los resultados de timeit
metodos = ['Fuerza Bruta', 'Dinámico', 'Voraz']
tiempos_timeit = [tiempos_fuerza_bruta_timeit, tiempos_dinamico_timeit, tiempos_voraz_timeit]

plt.bar(metodos, tiempos_timeit, color=['blue', 'orange', 'green'])
plt.xlabel('Método')
plt.ylabel('Tiempo Promedio (segundos)')
plt.title('Comparación de Tiempos de Ejecución con Timeit')
plt.show()