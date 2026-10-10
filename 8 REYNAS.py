import random
import time

NUM_REINAS = 8          # tamaño del tablero y número de reinas
DURACION_TABU = 7       # cuántas iteraciones dura una prohibición
MAX_ITERACIONES = 1000  # límite de iteraciones


def costo(estado):
    """Cuenta los pares de reinas que se atacan."""
    ataques = 0
    for i in range(NUM_REINAS):
        for j in range(i + 1, NUM_REINAS):
            misma_fila = estado[i] == estado[j]
            misma_diagonal = abs(estado[i] - estado[j]) == j - i
            if misma_fila or misma_diagonal:
                ataques += 1
    return ataques


def mostrar_tablero(estado):
    for fila in range(NUM_REINAS):
        linea = ""
        for columna in range(NUM_REINAS):
            linea += "R" if estado[columna] == fila else ". "
        print(linea)


#programa principal

inicio = time.perf_counter()

#estado inicial aleatorio
actual = [random.randrange(NUM_REINAS) for _ in range(NUM_REINAS)]
estado_inicial = actual[:]

mejor = actual[:]
mejor_costo = costo(actual)

tabu = {}          
movimientos = 0
iteracion = 0

# repetir hasta encontrar solución o llegar al límite
while mejor_costo > 0 and iteracion < MAX_ITERACIONES:
    iteracion += 1

    mejores_movimientos = []     # los mejores movimientos de este paso
    menor_costo = 999

    #probar mover cada reina a cada fila distinta
    for columna in range(NUM_REINAS):
        for fila in range(NUM_REINAS):
            if fila == actual[columna]:
                continue

            vecino = actual[:]
            vecino[columna] = fila
            costo_vecino = costo(vecino)

            
            prohibido = tabu.get((columna, fila), 0) >= iteracion
            if prohibido and costo_vecino >= mejor_costo:
                continue

            #guardar solo los mejores movimientos
            if costo_vecino < menor_costo:
                menor_costo = costo_vecino
                mejores_movimientos = [(columna, fila)]
            elif costo_vecino == menor_costo:
                mejores_movimientos.append((columna, fila))

    if not mejores_movimientos:
        continue

    # elegir uno de los mejores (al azar si hay empate) y hacerlo
    columna, fila = random.choice(mejores_movimientos)
    tabu[(columna, actual[columna])] = iteracion + DURACION_TABU   # prohibir regresar
    actual[columna] = fila
    movimientos += 1

    # guardar si es la mejor solución hasta ahora
    if menor_costo < mejor_costo:
        mejor = actual[:]
        mejor_costo = menor_costo

tiempo = time.perf_counter() - inicio

#resultados

print("Estado inicial:", estado_inicial)
print("Conflictos iniciales:", costo(estado_inicial))
mostrar_tablero(estado_inicial)

print("\nSolución:", mejor)
print("Conflictos finales:", mejor_costo)
mostrar_tablero(mejor)

print("\n--- Métricas ---")
print(f"Tiempo: {tiempo * 1000:.2f} ms")
print("Movimientos:", movimientos)
print("Resultado:", "SOLUCIÓN VÁLIDA" if mejor_costo == 0 else "No se encontró solución")