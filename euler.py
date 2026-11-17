# ==============================================================================
# Módulo: Circuito Euleriano (euler.py)
# Responsável: Gabriel Marcos de Oliveira Félix (Matrícula: 5792)
#
# Funções:
# 1. tem_circuito_euleriano(grafo) - Verifica se o grafo admite circuito Euleriano
# 2. circuito_euleriano(grafo) - Extrai a sequência do circuito via Hierholzer
# ==============================================================================

from collections import deque
from typing import List, Optional
from grafo import Grafo


def tem_circuito_euleriano(grafo: Grafo) -> bool:
    # De acordo com o Teorema de Euler:
    # 1. Todos os vértices com grau > 0 devem pertencer a uma única componente conexa.
    # 2. Todos os vértices devem possuir grau par.
    n = grafo.ordem()
    if n == 0 or grafo.tamanho() == 0:
        return False

    # 1. Verifica paridade de graus
    for v in range(1, n + 1):
        if grafo.grau(v) % 2 != 0:
            return False

    # 2. Encontra o primeiro vértice com arestas para iniciar a busca de conectividade
    inicio = None
    for v in range(1, n + 1):
        if grafo.grau(v) > 0:
            inicio = v
            break

    if inicio is None:
        return False

    # BFS simples para conferir se todos os vértices que possuem arestas se alcançam
    visitados = {inicio}
    fila = deque([inicio])

    while fila:
        u = fila.popleft()
        for viz in grafo.vizinhos(u):
            if viz not in visitados:
                visitados.add(viz)
                fila.append(viz)

    # Verifica se algum vértice com grau > 0 ficou de fora
    for v in range(1, n + 1):
        if grafo.grau(v) > 0 and v not in visitados:
            return False

    return True


def circuito_euleriano(grafo: Grafo) -> Optional[List[int]]:
    # Extrai o circuito Euleriano usando o Algoritmo de Hierholzer.
    # Retorna a lista ordenada de vértices do percurso fechado.
    if not tem_circuito_euleriano(grafo):
        return None

    n = grafo.ordem()

    # Copia a lista de adjacências para permitir remoção controlada de arestas
    adj = {u: list(grafo.vizinhos(u)) for u in range(1, n + 1)}

    # Ponto de partida: primeiro vértice de grau positivo
    inicio = 1
    for v in range(1, n + 1):
        if len(adj[v]) > 0:
            inicio = v
            break

    pilha = [inicio]
    circuito = []

    while pilha:
        atual = pilha[-1]
        if adj[atual]:
            # Escolhe o próximo vizinho e remove a aresta não direcionada em ambos os lados
            proximo = adj[atual].pop()
            adj[proximo].remove(atual)
            pilha.append(proximo)
        else:
            # Vértice sem arestas restantes é inserido no circuito
            circuito.append(pilha.pop())

    # Inverte para obter o circuito na ordem cronológica de percurso
    return circuito[::-1]


if __name__ == "__main__":
    import os

    caminho = os.path.join("instancias", "instancia1.txt")
    if os.path.exists(caminho):
        g = Grafo.carregar_de_arquivo(caminho)
        print("Tem circuito:", tem_circuito_euleriano(g))
        circ = circuito_euleriano(g)
        if circ:
            print("Circuito:", " -> ".join(map(str, circ)))
