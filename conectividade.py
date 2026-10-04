from collections import deque
from grafo import Grafo


def busca_em_largura(grafo, vertice_inicial):
    # Estruturas principais
    visitados = [vertice_inicial]
    visitados_set = {vertice_inicial}
    fila = deque([vertice_inicial])

    arvore = []
    arvore_arestas = set()

    # 1. Exploração em largura
    while fila:
        u = fila.popleft()
        for viz in grafo.vizinhos(u):
            if viz not in visitados_set:
                # 1. visitados_set.add: registra no conjunto hash para checagens futuras instantâneas O(1)
                visitados_set.add(viz)
                # 2. visitados.append: guarda na lista para registrar a ordem cronológica de visitação
                visitados.append(viz)
                # 3. fila.append: coloca no fim da fila para expandir seus vizinhos no momento certo (FIFO)
                fila.append(viz)

                # Guarda a aresta que descobriu o vizinho
                arvore.append((u, viz))
                arvore_arestas.add((min(u, viz), max(u, viz)))

    # 2. Arestas que não fazem parte da árvore (arestas redundantes na componente)
    fora_arvore = []
    for u in visitados:
        for viz in grafo.vizinhos(u):
            # u < viz garante olhar cada aresta apenas uma vez
            if u < viz and viz in visitados_set:
                aresta = (u, viz)
                if aresta not in arvore_arestas:
                    fora_arvore.append(aresta)

    return visitados, arvore, fora_arvore


def componentes_conexas_roy(grafo):
    n = grafo.ordem()
    if n == 0:
        return 0, []

    # 1. Inicializa a matriz de alcançabilidade R com False
    R = [[False] * (n + 1) for _ in range(n + 1)]

    # Todo vértice alcança a si mesmo e aos seus vizinhos diretos
    for i in range(1, n + 1):
        R[i][i] = True
        for viz in grafo.vizinhos(i):
            R[i][viz] = True

    # 2. Algoritmo clássico de Roy (3 loops tradicionais)
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            if R[i][k]:
                for j in range(1, n + 1):
                    if R[k][j]:
                        R[i][j] = True

    # 3. Agrupa os vértices que se alcançam em componentes
    visitados = set()
    componentes = []

    for i in range(1, n + 1):
        if i not in visitados:
            componente = []
            for j in range(1, n + 1):
                if R[i][j]:
                    componente.append(j)
                    visitados.add(j)
            componentes.append(componente)

    return len(componentes), componentes
