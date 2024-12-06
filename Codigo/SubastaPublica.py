'''
Proyecto 1 - SubastaPublica.py
Descripción: La presente implementación contiene las soluciones por fuerza bruta, programación dinámica y voraz para el problema de la subasta pública.
Autores:
            Rodas Arango, Juan Manuel - 2259571
            García Castañeda, Alex - 2259517
            Gómez Agudelo, Juan Sebastián - 2259474
            Henao Aricapa, Stiven - 2259603
Docente:
            Delgado Saavedra, Carlos Andrés
Fecha: 2024-10-25
'''

import numpy as np
#np.set_printoptions(threshold=np.inf) # Descomentar para ver la tabla completa

# Solucion por fuerza bruta generando todas las posibles combinaciones de acciones y seleccionando la mejor combinacion que maximice el valor total
# asignado a las acciones respetando las restricciones de cantidad minima y maxima de acciones por oferta
def fuerza_bruta(A, ofertas, precio_gobierno):
    mejor_valor = 0
    mejor_asignacion = []
    n = len(ofertas)

    # Función recursiva para probar todas las combinaciones de asignación
    def probar_asignaciones(idx, asignacion_actual, acciones_restantes):
        nonlocal mejor_valor, mejor_asignacion
        
        # Caso base: hemos evaluado todas las ofertas
        if idx == n:
            valor_actual = sum(asignacion_actual[i] * ofertas[i][0] for i in range(n))
            valor_actual += acciones_restantes * precio_gobierno  # Agregar lo que queda al gobierno

            if valor_actual > mejor_valor:
                mejor_valor = valor_actual
                mejor_asignacion = asignacion_actual.copy()
            return

        # Obtener detalles de la oferta actual
        precio, minimo, maximo = ofertas[idx]

        # Explorar todas las posibles asignaciones para la oferta actual
        for acciones in range(minimo, min(maximo, acciones_restantes) + 1):
            asignacion_actual[idx] = acciones
            if acciones_restantes - acciones >= 0:  # Solo continuar si no se exceden las acciones
                probar_asignaciones(idx + 1, asignacion_actual, acciones_restantes - acciones)

        # Considerar también la posibilidad de no asignar acciones a esta oferta
        asignacion_actual[idx] = 0
        probar_asignaciones(idx + 1, asignacion_actual, acciones_restantes)

    # Inicializar la búsqueda
    probar_asignaciones(0, [0] * n, A)

    # Asignar las acciones sobrantes al gobierno
    mejor_asignacion.append(A - sum(mejor_asignacion))

    mejor_valor = (sum(mejor_asignacion[i] * ofertas[i][0] for i in range(n)) + mejor_asignacion[-1] * precio_gobierno)
    
    return mejor_asignacion, mejor_valor

# Solución por programación dinámica, donde se calcula el valor máximo que se puede obtener para cada cantidad de acciones
def programacion_dinamica(A, ofertas, precio_gobierno):
    # Inicializar la tabla de programación dinámica y la tabla de asignaciones
    dp = [0] * (A + 1)
    asignaciones = [[0] * len(ofertas) for _ in range(A + 1)]

    # Iterar sobre cada oferta y actualizar la tabla de programación dinámica
    for i, (precio, minimo, maximo) in enumerate(ofertas):
        nuevo_dp = dp[:]
        nuevo_asignaciones = [asign.copy() for asign in asignaciones]
        
        for acciones in range(minimo, maximo + 1):
            for j in range(A, acciones - 1, -1):
                nuevo_valor = dp[j - acciones] + acciones * precio
                if nuevo_valor > nuevo_dp[j]:
                    nuevo_dp[j] = nuevo_valor
                    nuevo_asignaciones[j] = asignaciones[j - acciones].copy()
                    nuevo_asignaciones[j][i] = acciones
        
        dp = nuevo_dp
        asignaciones = nuevo_asignaciones

    mejor_valor = 0
    mejor_asignacion = []
    acciones_sobrantes = 0

    # Encontrar la mejor asignación para la cantidad de acciones A
    for j in range(A + 1):
        valor = dp[j] + (A - j) * precio_gobierno
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_asignacion = asignaciones[j].copy()
            acciones_sobrantes = A - j

    # Asignar acciones sobrantes al gobierno
    mejor_asignacion.append(acciones_sobrantes)

    # Actualizar la última posición de dp
    dp[-1] = mejor_valor

    # Actualizar la última posición de asignaciones
    asignaciones[-1] = mejor_asignacion

    return mejor_asignacion, mejor_valor, dp, asignaciones


# Solución voraz, donde se seleccionan las ofertas con el precio más bajo que el precio del gobierno y se asignan la mayor cantidad de acciones posible
def voraz(A, ofertas, precio_gobierno):
    mejor_valor = 0
    mejor_asignacion = [0] * len(ofertas)
    acciones_restantes = A

    # Ordenar las ofertas por precio
    for i, (precio, minimo, maximo) in enumerate(ofertas):
        if precio <= precio_gobierno:
            continue
        
        if acciones_restantes <= 0:
            break

        # Intentar asignar el máximo posible primero
        acciones = min(maximo, acciones_restantes)
        
        if acciones < minimo:
            # Verificar si podemos reasignar acciones de las ofertas anteriores
            if i > 0 and mejor_asignacion[i-1] > minimo:
                ajuste = min(mejor_asignacion[i-1] - minimo, minimo - acciones)
                mejor_asignacion[i-1] -= ajuste
                acciones += ajuste
            else:
                continue  # Si no se puede ajustar, saltar esta oferta
        
        mejor_asignacion[i] = acciones
        mejor_valor += acciones * precio
        acciones_restantes -= acciones

    # Asignar acciones sobrantes al gobierno
    if acciones_restantes > 0:
        mejor_valor += acciones_restantes * precio_gobierno

    mejor_asignacion.append(A-sum(mejor_asignacion))

    # Asegurar el calculo de mejor_valor:
    mejor_valor = 0
    for i, (precio, minimo, maximo) in enumerate(ofertas):
        mejor_valor += mejor_asignacion[i] * precio
        
    mejor_valor += mejor_asignacion[-1] * precio_gobierno

    
    return mejor_asignacion, mejor_valor
