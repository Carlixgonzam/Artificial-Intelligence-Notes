# Hay alguna estructura de datos que se necesite para estos ejercicios?
from collections import deque
import heapq


def breadth_first_search(start, goal, get_neighbors):
    """
    Breadth-First Search

    Args:
        start: Posición de Inicio (tuple)
        goal: Posición de la Meta (tuple)
        get_neighbors: Función que toma la posición y retorna una lista de (vecino, costo) tuplas

    Returns:
        tuple: (path, nodos_explorados)
            - path: Lista de posiciones de comienzo a la meta o [] si no hay un path
            - nodos_explorados: Lista de posiciones en el orden explorado (para visualización)

    TODO: Implementar algoritmo de BFS
    """

    # TODO: Aquí va su implementación
    # Hints:
    # - frontera -> Qué tipo de fila necesito?
    # - visitados -> Qué tipo de estructura de datos necesito para acumular los visitados? Cuáles son las restricciones?
    # - nodos_explorados -> Qué tipo de estructura de datos necesito? Es diferente a visitados?
    # - Acuerdense de grabar la exploración! Cómo puedo hacer esto? Qué tipo de estructuras de datos necesito?
    frontera = deque()
    frontera.append((start, [start]))
    visitados = set()
    visitados.add(start)
    nodos_explorados = []
    while frontera:
        posi, camino = frontera.popleft()
        nodos_explorados.append(posi)
        if posi == goal:
            return camino, nodos_explorados
        for veci, costo in get_neighbors(posi):
            if veci not in visitados:
                visitados.add(veci)
                if veci == goal:
                    return camino + [veci], nodos_explorados
                frontera.append((veci, camino + [veci]))
    return [], nodos_explorados

    raise NotImplementedError("BFS no se ha implementado")


def depth_first_search(start, goal, get_neighbors):
    """
    Depth-First Search
    Args:
        start: Posición de Inicio (tuple)
        goal: Posición de la Meta (tuple)
        get_neighbors: Función que toma la posición y retorna una lista de (vecino, costo) tuplas

    Returns:
        tuple: (path, nodos_explorados)
            - path: Lista de posiciones de comienzo a la meta o [] si no hay un path
            - nodos_explorados: Lista de posiciones en el orden explorado (para visualización)

    TODO: Implementar el algoritmo de DFS
    """

    # TODO: Aquí va su implementación
    # Hints:
    # - frontera -> Qué tipo de fila necesito?
    # - Qué operación necesito para remover elementos de la fila que estoy manejando?
    # para este algoritmo, necesito la fila LIFO(Last In First Out)
    fronterita = []
    fronterita.append((start, [start]))
    visitados = set()
    visitados.add(start)
    nodos_explorados = []
    while fronterita:
        pos, camin = fronterita.pop()
        nodos_explorados.append(pos)
        if pos == goal:
            return camin, nodos_explorados
        for vecino, costo in get_neighbors(pos):
            if vecino not in visitados:
                visitados.add(vecino)
                if vecino == goal:
                    return camin + [vecino], nodos_explorados
                fronterita.append((vecino, camin + [vecino]))
    return [], nodos_explorados

    raise NotImplementedError("DFS no se ha implementado")


def uniform_cost_search(start, goal, get_neighbors):
    """
    Uniform Cost Search

    Args:
        start: Posición de Inicio (tuple)
        goal: Posición de la Meta (tuple)
        get_neighbors: Función que toma la posición y retorna una lista de (vecino, costo) tuplas

    Returns:
        tuple: (path, nodos_explorados)
            - path: Lista de posiciones de comienzo a la meta o [] si no hay un path
            - nodos_explorados: Lista de posiciones en el orden explorado (para visualización)

    TODO: Implementar algoritmo UCS


    IMPORTANTE: Usar counter para cuando halla empates!
    """

    # TODO: Aquí va su implementación
    # Hints:
    # - Qué tipo de estructuras de datos necesito que me contemple el costo? Qué operaciones necesito?
    # tengo costo acumulado, contador que desempata si dos nodos tienen igual costo, posicion y camino

    frontera = [(0, 0, start, [start])]
    visitados = set()
    contador = 0
    nodos_explorados = []
    while frontera:
        costo, _, pos, camino = heapq.heappop(frontera)
        if pos in visitados:
            continue
        visitados.add(pos)
        nodos_explorados.append(pos)
        if pos == goal:
            return camino, nodos_explorados
        for vecinos, costico_actual in get_neighbors(pos):
            if vecinos not in visitados:
                contador += 1
                heapq.heappush(
                    frontera,
                    (costo + costico_actual, contador, vecinos, camino + [vecinos]),
                )

    return [], nodos_explorados

    raise NotImplementedError("UCS no se ha implementado")


def bidirectional_search(start, goal, get_neighbors):
    """
    Bidirectional Search

    Args:
        start: Posición de Inicio (tuple)
        goal: Posición de la Meta (tuple)
        get_neighbors: Función que toma la posición y retorna una lista de (vecino, costo) tuplas

    Returns:
        tuple: (path, nodos_explorados)
            - path: Path combinado de comienzo a final.
            - nodos_explorados: Estructura de datos de posiciones en el orden explorado (para visualización)

    TODO: Implementar búsqueda bidireccional


    RETO: Combinación de Paths!
    - Cómo es el primer path y el segundo? Qué diferencias hay?
    - Cómo se deben duplicar ambos planes? Hay puntos repetidos?
    """

    # TODO: Aquí su implementación
    # Hints:
    # - Necesito el mismo tipo de filas para los caminos?
    # - Qué tipo de estructura de datos necesito para los nodos visitados? Necesito 1 o 2?
    # - Qué tipo de estructura de datos necesito para mantener registro de los nodos explorados?
    fronterainicio = deque()
    fronterainicio.append((start, [start]))
    fronteragoal = deque()
    fronteragoal.append((goal, [goal]))
    visitadosinicio = {start: [start]}
    visitadosgoal = {goal: [goal]}
    exploradosi = []
    exploradosg = []

    while fronterainicio and fronteragoal:
        i, camino_i = fronterainicio.popleft()
        exploradosi.append(i)
        if i in visitadosgoal:
            return camino_i + visitadosgoal[i][::-1][1:], {
                "start": exploradosi,
                "goal": exploradosg,
            }
        for vecino, cos in get_neighbors(i):
            if vecino not in visitadosinicio:
                visitadosinicio[vecino] = camino_i + [vecino]
                fronterainicio.append((vecino, camino_i + [vecino]))
        j, camino_j = fronteragoal.popleft()
        exploradosg.append(j)
        if j in visitadosinicio:
            return camino_j + visitadosinicio[j][::-1][1:], {
                "start": exploradosi,
                "goal": exploradosg,
            }
        for veci, costo in get_neighbors(j):
            if veci not in visitadosgoal:
                visitadosgoal[veci] = camino_j + [veci]
                fronteragoal.append((veci, camino_j + [veci]))
    return [], {"start": exploradosi, "goal": exploradosg}

    raise NotImplementedError("Búsqueda bidireccional no se ha implementado")


# =============================================================================
# FUNCIONES PARA HACER TESTS
# =============================================================================


def test_algorithm(algorithm_func, test_name="Test"):
    """
    Probar algoritmo

    Grilla Simple:
    S . . .
    . # # .
    . . . G

    Where S = start, G = goal, # = Pared
    """
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print("=" * 60)

    # Simple 4x4 grid
    walls = {(1, 1), (1, 2), (2, 1)}

    def get_neighbors(pos):
        """Función de vecinos para hacer tests"""
        x, y = pos
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 4 and 0 <= ny < 3 and (nx, ny) not in walls:
                neighbors.append(((nx, ny), 1))  # Todos los costos son 1
        return neighbors

    start = (0, 0)
    goal = (3, 2)

    try:
        result = algorithm_func(start, goal, get_neighbors)

        # Manejo de búsqueda bidireccional (formato de return diferente)
        if isinstance(result[1], dict):
            path, explored_dict = result
            explored = explored_dict.get("start", []) + explored_dict.get("goal", [])
        else:
            path, explored = result

        print(f"✓ Algortimo se completó de forma satisfactoria!")
        print(f"  Camino hallado: {len(path) > 0}")
        if path:
            print(f"  Longitud Camino: {len(path)} pasos")
            print(f"  Camino: {' -> '.join(map(str, path))}")
        print(f"  Nodos explorados: {len(explored)}")
        print(f"  Orden de exploración: {explored}")

    except NotImplementedError as e:
        print(f"✗ {e}")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    """
    Correr este archivo para verificar tu implementación!
    No GUI needed - pure algorithm testing!
    """

    print("\n" + "=" * 60)
    print("TEST DE ALGORITMOS")
    print("=" * 60)

    # Probar todos los algoritmos
    test_algorithm(breadth_first_search, "Breadth-First Search")
    test_algorithm(depth_first_search, "Depth-First Search")
    test_algorithm(uniform_cost_search, "Uniform Cost Search")
    test_algorithm(bidirectional_search, "Búsqueda Bidireccional")

    print("\n" + "=" * 60)
    print("Prueba Completada!")
    print("=" * 60)
