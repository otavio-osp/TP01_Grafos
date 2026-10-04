"""
Módulo: Caminhos Mínimos e Vulnerabilidade (caminhos_analise.py)
Responsável: Aluno 3

Funções:
1. dijkstra(grafo, origem) - Algoritmo de caminhos mínimos de origem única.
2. verificar_articulacao(grafo, vertice) - Verifica se um vértice é ponto de articulação.
3. possui_ciclo(grafo) - Verifica a existência de ciclos no grafo.
"""

import heapq
from collections import deque
from grafo import Grafo


def dijkstra(grafo: Grafo, origem: int) -> tuple[dict[int, float], dict[int, list[int]]]:
    """
    Calcula os caminhos mínimos a partir de um vértice de origem para todos os outros
    vértices do grafo utilizando o algoritmo de Dijkstra.

    Args:
        grafo (Grafo): Instância do grafo.
        origem (int): Vértice de origem.

    Returns:
        tuple: (distancias, caminhos)
            - distancias: dict mapeando vértice -> menor distância a partir da origem.
            - caminhos: dict mapeando vértice -> lista de vértices representando a rota mínima.
    """
    n = grafo.ordem()
    # Inicializa todas as distâncias com infinito
    distancias = {v: float('inf') for v in range(1, n + 1)}
    distancias[origem] = 0.0

    # Dicionário para rastrear os predecessores na reconstrução do caminho
    predecessores = {v: None for v in range(1, n + 1)}
    
    # Fila de prioridade que armazena tuplas (distancia_acumulada, vertice)
    # A heapq nativa do Python é um min-heap.
    fila_prioridade = [(0.0, origem)]
    visitados = set()

    while fila_prioridade:
        dist_atual, u = heapq.heappop(fila_prioridade)

        # Se já encontramos um caminho menor para u antes, ignoramos a entrada obsoleta
        if dist_atual > distancias[u]:
            continue
            
        visitados.add(u)

        for vizinho in grafo.vizinhos(u):
            if vizinho in visitados:
                continue

            peso_aresta = grafo.obter_peso(u, vizinho)
            if peso_aresta is None:
                continue
                
            dist_alternativa = dist_atual + peso_aresta

            # Se a nova distância é menor, atualizamos os registros
            if dist_alternativa < distancias[vizinho]:
                distancias[vizinho] = dist_alternativa
                predecessores[vizinho] = u
                heapq.heappush(fila_prioridade, (dist_alternativa, vizinho))

    # Reconstrução dos caminhos (de origem até cada destino)
    caminhos = {}
    for destino in range(1, n + 1):
        if distancias[destino] == float('inf'):
            caminhos[destino] = []
        else:
            rota = []
            atual = destino
            while atual is not None:
                rota.append(atual)
                atual = predecessores[atual]
            caminhos[destino] = rota[::-1]  # Inverte para ficar [origem, ..., destino]

    return distancias, caminhos


def verificar_articulacao(grafo: Grafo, vertice: int) -> bool:
    """
    Verifica se um dado vértice é um ponto de articulação. Um ponto de articulação é
    aquele cuja remoção aumenta o número de componentes conexas do grafo.

    A lógica verifica se os vizinhos do vértice em teste continuam conectados entre si
    após a exclusão virtual (ignorar na travessia) do próprio vértice.

    Args:
        grafo (Grafo): Instância do grafo.
        vertice (int): Vértice a ser testado.

    Returns:
        bool: True se for articulação, False caso contrário.
    """
    vizinhos = grafo.vizinhos(vertice)
    
    # Se o vértice tem 0 ou 1 vizinho, removê-lo nunca desconectará o grafo.
    if len(vizinhos) <= 1:
        return False

    # Inicia uma Busca em Largura (BFS) pelo primeiro vizinho
    vertice_inicial_bfs = vizinhos[0]
    visitados = {vertice_inicial_bfs}
    fila = deque([vertice_inicial_bfs])

    while fila:
        u = fila.popleft()
        for vizinho in grafo.vizinhos(u):
            # Condição de exclusão virtual: agimos como se o 'vertice' testado não existisse
            if vizinho != vertice and vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)

    # Verifica se todos os demais vizinhos foram alcançados. 
    # Se algum não foi, o vértice testado era o elo que mantinha a componente conexa.
    for vizinho in vizinhos[1:]:
        if vizinho not in visitados:
            return True

    return False


def possui_ciclo(grafo: Grafo) -> bool:
    """
    Verifica a existência de pelo menos um ciclo no grafo utilizando Busca em Largura (BFS).

    Args:
        grafo (Grafo): Instância do grafo.

    Returns:
        bool: True se o grafo possuir ciclo(s), False se for acíclico (uma floresta).
    """
    n = grafo.ordem()
    visitados = set()

    # O loop externo garante que todos os componentes conexos serão testados
    for i in range(1, n + 1):
        if i not in visitados:
            # A fila armazena tuplas: (vertice_atual, vértice_pai_de_onde_veio)
            fila = deque([(i, None)])
            visitados.add(i)

            while fila:
                u, pai = fila.popleft()
                for vizinho in grafo.vizinhos(u):
                    # Ignorar a aresta que nos trouxe até 'u'
                    if vizinho == pai:
                        continue

                    # Se encontrarmos um vizinho que já foi visitado, detectamos um ciclo!
                    if vizinho in visitados:
                        return True

                    visitados.add(vizinho)
                    fila.append((vizinho, u))

    return False
