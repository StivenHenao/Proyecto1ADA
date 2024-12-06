'''
Proyecto 1 - TerminalInteligente.py
Descripción: Implementación de un terminal inteligente que permite realizar operaciones sobre una cadena de texto.
             Por medio de tres algoritmos diferentes, se busca encontrar la secuencia de operaciones más eficiente.
Autores:
            Rodas Arango, Juan Manuel - 2259571
            García Castañeda, Alex - 2259517
            Gómez Agudelo, Juan Sebastián - 2259474
            Henao Aricapa, Stiven - 2259603
Docente:
            Delgado Saavedra, Carlos Andrés
Fecha: 2024-10-25
'''


import copy

costos_global = {'a': 1, 'd': 2, 'r': 3, 'i': 2, 'k': 1}

# Funciones de operaciones
def advance(cadena, cursor, costos):
    if cursor < len(cadena):
        cursor += 1
        costos['a'] += 1
    return cursor, costos

def delete(cadena, cursor, costos):
    if cursor < len(cadena):
        cadena = cadena[:cursor] + cadena[cursor+1:]
        costos['d'] += 1
    return cadena, cursor, costos

def replace(cadena, cursor, costos, caracter):
    if cursor < len(cadena):
        cadena = cadena[:cursor] + caracter + cadena[cursor+1:]
        cursor += 1
        costos['r'] += 1
    return cadena, cursor, costos

def insert(cadena, cursor, costos, caracter):
    cadena = cadena[:cursor] + caracter + cadena[cursor:]
    cursor += 1
    costos['i'] += 1
    return cadena, cursor, costos

def kill(cadena, cursor, costos):
    cadena = cadena[:cursor]
    costos['k'] += 1
    return cadena, cursor, costos

# Función para generar la cadena de costos factorizada
def calcular_costo_total(operaciones):
    conteo = {}
    for operacion in operaciones:
        if operacion in conteo:
            conteo[operacion] += 1
        else:
            conteo[operacion] = 1
    resultado = []
    for operacion, cantidad in conteo.items():
        if cantidad > 1:
            resultado.append(f"{cantidad}{operacion}")
        else:
            resultado.append(operacion)
    return " + ".join(resultado)

# Formatear costos para la tabla
def formatear_costos(costos):
    resultado = []
    for operacion, cantidad in costos.items():
        if cantidad > 0:
            resultado.append(f"{cantidad}{operacion}")
    return " + ".join(resultado)

# Solución Ingenua (Fuerza Bruta)
def solucion_ingenua(cadena_inicial, cadena_final, cursor, costos, operaciones):
    # Verificar si ya llegamos al final de ambas cadenas
    if cursor >= len(cadena_inicial) and cursor >= len(cadena_final):
        return cadena_inicial, costos, operaciones
    # Verificar si podemos avanzar
    if cursor < len(cadena_inicial) and cursor < len(cadena_final) and cadena_inicial[cursor] == cadena_final[cursor]:
        costos_a = costos.copy()
        operaciones_a = operaciones + ['advance']
        costos_a['a'] += 1
        return solucion_ingenua(cadena_inicial, cadena_final, cursor + 1, costos_a, operaciones_a)
    posibles_solu = []
    # Verificar si podemos insertar
    if cursor < len(cadena_final) and (cursor >= len(cadena_inicial) or cadena_inicial[cursor] != cadena_final[cursor]):
        costos_i = costos.copy()
        operaciones_i = operaciones + [f'insert {cadena_final[cursor]}']
        costos_i['i'] += 1
        nueva_cadena = cadena_inicial[:cursor] + cadena_final[cursor] + cadena_inicial[cursor:]
        posibles_solu.append(
            solucion_ingenua(nueva_cadena, cadena_final, cursor + 1, costos_i, operaciones_i)
        )
    # Verificar si podemos reemplazar
    if cursor < len(cadena_inicial) and cursor < len(cadena_final) and cadena_inicial[cursor] != cadena_final[cursor]:
        costos_r = costos.copy()
        operaciones_r = operaciones + [f'replace with {cadena_final[cursor]}']
        costos_r['r'] += 1
        nueva_cadena = cadena_inicial[:cursor] + cadena_final[cursor] + cadena_inicial[cursor+1:]
        posibles_solu.append(
            solucion_ingenua(nueva_cadena, cadena_final, cursor + 1, costos_r, operaciones_r)
        )
    # Verificar si podemos eliminar
    if cursor < len(cadena_inicial) and cursor >= len(cadena_final):
        costos_d = costos.copy()
        operaciones_d = operaciones + ['delete']
        costos_d['d'] += 1
        nueva_cadena = cadena_inicial[:cursor] + cadena_inicial[cursor+1:]
        posibles_solu.append(
            solucion_ingenua(nueva_cadena, cadena_final, cursor, costos_d, operaciones_d)
        )
    # Verificar si podemos usar kill
    if cursor < len(cadena_inicial):
        costos_k = costos.copy()
        operaciones_k = operaciones + ['kill']
        costos_k['k'] += 1
        nueva_cadena = cadena_inicial[:cursor]
        posibles_solu.append(
            solucion_ingenua(nueva_cadena, cadena_final, cursor, costos_k, operaciones_k)
        )
    # Seleccionar la mejor solución
    for solu in posibles_solu:
        if solu[0] == cadena_final:
            return solu
    return None, None, None

# Aplicar operaciones para verificar la cadena final
def aplicar_operaciones(operaciones, cadena_inicial):
    cadena_resultante = list(cadena_inicial)
    cursor = 0
    estados = [("-", ''.join(cadena_resultante))]
    costos_finales = {'a': 0, 'd': 0, 'r': 0, 'i': 0, 'k': 0}
    
    for op in operaciones:
        if op == 'advance':
            cursor += 1
            costos_finales['a'] += 1
        elif op.startswith('replace with '):
            caracter = op.split(' ')[-1]
            if cursor < len(cadena_resultante):
                cadena_resultante[cursor] = caracter
            cursor += 1
            costos_finales['r'] += 1
        elif op.startswith('insert '):
            caracter = op.split(' ')[-1]
            cadena_resultante.insert(cursor, caracter)
            cursor += 1
            costos_finales['i'] += 1
        elif op == 'kill':
            del cadena_resultante[cursor:]
            costos_finales['k'] += 1
        elif op == 'delete':
            if cursor < len(cadena_resultante):
                del cadena_resultante[cursor]
            costos_finales['d'] += 1
        estados.append((op, ''.join(cadena_resultante)))
    costo_total = formatear_costos(costos_finales)
    return ''.join(cadena_resultante), costos_finales, costo_total, estados

# Solución Dinámica
def solucion_dinamica(cadena_inicial, cadena_final, costos_operaciones):
    len_inicial = len(cadena_inicial)
    len_final = len(cadena_final)
    matriz_costos = [[0] * (len_final + 1) for _ in range(len_inicial + 1)]
    kill_aplicado = [False] * (len_inicial + 1)  # Marca si se ha aplicado `kill` en cada fila

    # Inicializar la primera columna
    for i in range(1, len_inicial + 1):
        matriz_costos[i][0] = matriz_costos[i - 1][0] + costos_operaciones['d']

    # Inicializar la primera fila
    for j in range(1, len_final + 1):
        matriz_costos[0][j] = matriz_costos[0][j - 1] + costos_operaciones['i']

    # Llenar la matriz de costos
    for i in range(1, len_inicial + 1):
        for j in range(1, len_final + 1):
            if cadena_inicial[i - 1] == cadena_final[j - 1]:
                costo_reemplazo = matriz_costos[i - 1][j - 1]
            else:
                costo_reemplazo = matriz_costos[i - 1][j - 1] + costos_operaciones['r']
            costo_insercion = matriz_costos[i][j - 1] + costos_operaciones['i']
            costo_eliminacion = matriz_costos[i - 1][j] + costos_operaciones['d']
            costo_kill = matriz_costos[i][0] + costos_operaciones['k']

            # Si `kill` se ha aplicado en una fila anterior, ignoramos `delete`
            if kill_aplicado[i - 1]:
                costo_eliminacion = float('inf')

            # Elegir el mínimo entre todas las opciones
            matriz_costos[i][j] = min(costo_reemplazo, costo_insercion, costo_eliminacion, costo_kill)

            # Marcar si se aplica `kill`
            if matriz_costos[i][j] == costo_kill:
                kill_aplicado[i] = True

    # Reconstruir operaciones
    i, j = len_inicial, len_final
    operaciones = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and cadena_inicial[i - 1] == cadena_final[j - 1]:
            operaciones.append('advance')
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and matriz_costos[i][j] == matriz_costos[i - 1][j - 1] + costos_operaciones['r']:
            operaciones.append(f'replace with {cadena_final[j - 1]}')
            i -= 1
            j -= 1
        elif j > 0 and matriz_costos[i][j] == matriz_costos[i][j - 1] + costos_operaciones['i']:
            operaciones.append(f'insert {cadena_final[j - 1]}')
            j -= 1
        elif i > 0 and not kill_aplicado[i] and matriz_costos[i][j] == matriz_costos[i - 1][j] + costos_operaciones['d']:
            operaciones.append('delete')
            i -= 1
        elif matriz_costos[i][j] == matriz_costos[i][0] + costos_operaciones['k']:
            operaciones.append('kill')
            i = 0  # Después de un 'kill', no quedan caracteres por eliminar
        else:
            break

    operaciones.reverse()
    costo_total = matriz_costos[len_inicial][len_final]
    return matriz_costos, costo_total, operaciones

# Solución voraz considerando costos dinámicos
def solucion_voraz(cadena_inicial, cadena_final, costos):
    cursor_inicial = 0
    cursor_final = 0
    operaciones = []
    cadena = list(cadena_inicial)  # Convertimos la cadena en una lista para operaciones más eficientes
    costo_total = 0

    # Mientras tengamos caracteres en la cadena final o en la cadena inicial
    while cursor_final < len(cadena_final) or cursor_inicial < len(cadena):
        # Verificar si estamos aún dentro de ambas cadenas
        if cursor_inicial < len(cadena) and cursor_final < len(cadena_final):
            if cadena[cursor_inicial] == cadena_final[cursor_final]:
                # Si los caracteres son iguales, avanzamos
                cursor_inicial += 1
                cursor_final += 1
                costo_total += costos['a']
                operaciones.append('advance')
            else:
                # Si son diferentes, seleccionamos la operación óptima entre reemplazar, eliminar, insertar
                costo_replace = costos['r']
                costo_delete = costos['d']
                costo_insert = costos['i']

                # Verificamos la operación más barata
                if cursor_inicial < len(cadena) and costo_delete <= costo_replace and costo_delete <= costo_insert:
                    # Eliminar el carácter en la cadena inicial
                    cadena.pop(cursor_inicial)
                    costo_total += costo_delete
                    operaciones.append('delete')
                elif cursor_inicial < len(cadena) and costo_delete > costo_replace and costo_delete > costo_insert:
                    # Aplicar kill
                    cadena = cadena[:cursor_inicial]
                    costo_total += costos['k']
                    operaciones.append('kill')
                elif costo_replace <= costo_delete and costo_replace <= costo_insert:
                    # Reemplazar el carácter
                    cadena[cursor_inicial] = cadena_final[cursor_final]
                    cursor_inicial += 1
                    cursor_final += 1
                    costo_total += costo_replace
                    operaciones.append(f'replace with {cadena_final[cursor_final - 1]}')
                else:
                    # Insertar un carácter desde la cadena final en la cadena inicial
                    cadena.insert(cursor_inicial, cadena_final[cursor_final])
                    cursor_inicial += 1
                    cursor_final += 1
                    costo_total += costos['i']
                    operaciones.append(f'insert {cadena_final[cursor_final - 1]}')

        # Si llegamos al final de la cadena inicial pero aún hay caracteres en la cadena final
        elif cursor_final < len(cadena_final):
            # Insertar los caracteres restantes
            cadena.insert(cursor_inicial, cadena_final[cursor_final])
            cursor_inicial += 1
            cursor_final += 1
            costo_total += costos['i']
            operaciones.append(f'insert {cadena_final[cursor_final - 1]}')

        # Si llegamos al final de la cadena final pero aún quedan caracteres en la cadena inicial
        elif cursor_inicial < len(cadena):
            # Verificar si usar 'kill' es más barato que eliminar
            if cursor_inicial < len(cadena):
                # Eliminar los caracteres sobrantes uno por uno
                costo_kill = costos['k']
                costo_resto = (len(cadena) - cursor_inicial) * costos['d']

                if costo_kill < costo_resto:
                    # Aplicar kill
                    cadena = cadena[:cursor_inicial]
                    costo_total += costos['k']
                    operaciones.append('kill')
                else:
                    # Eliminar los caracteres sobrantes uno por uno
                    cadena.pop(cursor_inicial)
                    costo_total += costos['d']
                    operaciones.append('delete')

    return ''.join(cadena), costo_total, operaciones

def generar_cadena_costos(costos):
    resultado = []
    for operacion, cantidad in costos.items():
        if cantidad > 0:
            if cantidad == 1:
                resultado.append(f"{operacion}")
            else:
                resultado.append(f"{cantidad}{operacion}")
    return ' + '.join(resultado)

# Pasar de operaciones a diccionario de costos
def operaciones_a_costos(operaciones):
    costos = {'a': 0, 'd': 0, 'r': 0, 'i': 0, 'k': 0}
    for op in operaciones:
        if op == 'advance':
            costos['a'] += 1
        elif op == 'delete':
            costos['d'] += 1
        elif op.startswith('replace with '):
            costos['r'] += 1
        elif op.startswith('insert '):
            costos['i'] += 1
        elif op == 'kill':
            costos['k'] += 1
    return costos
