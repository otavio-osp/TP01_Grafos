import random
import time
from typing import Dict, List, Optional, Set, Tuple
from grafo import Grafo


def extrair_arestas(grafo: Grafo) -> Set[Tuple[int, int]]:
    """
    Retorna o conjunto de todas as arestas não direcionadas do grafo como tuplas (u, v)
    com u < v para evitar duplicações.
    """
    arestas: Set[Tuple[int, int]] = set()
    n = grafo.ordem()
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if grafo.tem_aresta(u, v):
                arestas.add((u, v))
    return arestas


def eh_cobertura_valida(grafo: Grafo, cobertura: Set[int]) -> bool:
    """
    Verifica formalmente se o conjunto 'cobertura' é uma cobertura de vértices válida,
    isto é, se toda aresta {u, v} de G possui ao menos uma de suas pontas em 'cobertura'.
    """
    n = grafo.ordem()
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if grafo.tem_aresta(u, v):
                if u not in cobertura and v not in cobertura:
                    return False
    return True


def poda_redundancias(grafo: Grafo, cobertura: Set[int]) -> Set[int]:
    """
    Busca Local / Poda de Vértices Redundantes:
    Dado um conjunto de cobertura válido, verifica se algum vértice pode ser removido
    sem violar a propriedade de cobertura.
    
    Um vértice u pertencente à cobertura é redundante se para todo vizinho v com {u, v} in E,
    o vizinho v também pertence à cobertura.
    
    A verificação avalia primeiro os vértices de menor grau original para preservar
    nós de alta conectividade que cobrem múltiplos outros nós.
    """
    solucao = set(cobertura)
    candidatos = sorted(solucao, key=lambda v: grafo.grau(v))

    for u in candidatos:
        if u not in solucao:
            continue
        
        # u é redundante se todos os seus vizinhos já estão em solucao
        redundante = True
        for viz in grafo.vizinhos(u):
            if viz not in solucao:
                redundante = False
                break
        
        if redundante:
            solucao.remove(u)

    return solucao


def cobertura_gulosa(grafo: Grafo) -> Set[int]:
    """
    Algoritmo Guloso para Cobertura de Vértices (Chvátal / Johnson):
    A cada iteração, seleciona o vértice que possui o maior grau residual atual
    (quantidade de arestas incidentes ainda não cobertas). Remove todas as arestas
    incidentes a esse vértice e repete o processo até cobrir todas as conexões.
    
    Em caso de empate no grau residual, o desempate ocorre pelo menor índice numérico
    do vértice para assegurar comportamento determinístico e reprodutível.
    """
    n = grafo.ordem()
    adj_residual: Dict[int, Set[int]] = {
        u: set(grafo.vizinhos(u)) for u in range(1, n + 1)
    }
    graus: Dict[int, int] = {u: len(adj_residual[u]) for u in range(1, n + 1)}

    cobertura: Set[int] = set()
    arestas_cobertas_total = 0
    total_arestas = grafo.tamanho()

    while arestas_cobertas_total < total_arestas:
        melhor_vertice = -1
        maior_grau = 0

        for u in range(1, n + 1):
            g = graus[u]
            if g > maior_grau:
                maior_grau = g
                melhor_vertice = u

        if melhor_vertice == -1 or maior_grau == 0:
            break

        cobertura.add(melhor_vertice)
        vizinhos_cobertos = list(adj_residual[melhor_vertice])

        for viz in vizinhos_cobertos:
            adj_residual[viz].discard(melhor_vertice)
            graus[viz] -= 1
            arestas_cobertas_total += 1

        adj_residual[melhor_vertice].clear()
        graus[melhor_vertice] = 0

    return cobertura


def construcao_gulosa_randomizada(
    grafo: Grafo, alpha: float = 0.85, rng: Optional[random.Random] = None
) -> Set[int]:
    """
    Fase de Construção do GRASP:
    Gera uma cobertura de vértices via guloso adaptativo semi-randomizado.
    Calcula a Lista Restrita de Candidatos (RCL) contendo vértices cujo grau residual
    está acima de:
        limiar = d_max - alpha * (d_max - d_min)
    Sorteia aleatoriamente um nó da RCL e atualiza o estado residual das arestas.
    """
    if rng is None:
        rng = random.Random()

    n = grafo.ordem()
    adj_residual: Dict[int, Set[int]] = {
        u: set(grafo.vizinhos(u)) for u in range(1, n + 1)
    }
    graus: Dict[int, int] = {u: len(adj_residual[u]) for u in range(1, n + 1)}

    cobertura: Set[int] = set()
    arestas_cobertas_total = 0
    total_arestas = grafo.tamanho()

    while arestas_cobertas_total < total_arestas:
        graus_positivos = [g for g in graus.values() if g > 0]
        if not graus_positivos:
            break

        d_max = max(graus_positivos)
        d_min = min(graus_positivos)
        limiar = d_max - alpha * (d_max - d_min)

        rcl = [u for u in range(1, n + 1) if graus[u] >= limiar and graus[u] > 0]
        if not rcl:
            break

        vertice_escolhido = rng.choice(rcl)
        cobertura.add(vertice_escolhido)

        vizinhos_cobertos = list(adj_residual[vertice_escolhido])
        for viz in vizinhos_cobertos:
            adj_residual[viz].discard(vertice_escolhido)
            graus[viz] -= 1
            arestas_cobertas_total += 1

        adj_residual[vertice_escolhido].clear()
        graus[vertice_escolhido] = 0

    return cobertura


def cobertura_heuristica(
    grafo: Grafo,
    num_iteracoes: int = 25,
    alpha: float = 0.85,
    seed: Optional[int] = 42
) -> Set[int]:
    """
    Meta-heurística GRASP (Greedy Randomized Adaptive Search Procedure) com Busca Local:
    Realiza iterações compostas por:
    1. Construção gulosa semi-randomizada (RCL orientada pelo parâmetro alpha).
    2. Busca Local pós-construção mediante Poda de Vértices Redundantes.
    Retorna a cobertura minimal com menor cardinalidade encontrada no conjunto de iterações.
    """
    rng = random.Random(seed)
    melhor_solucao: Optional[Set[int]] = None

    for _ in range(num_iteracoes):
        sol_inicial = construcao_gulosa_randomizada(grafo, alpha=alpha, rng=rng)
        sol_refinada = poda_redundancias(grafo, sol_inicial)

        if melhor_solucao is None or len(sol_refinada) < len(melhor_solucao):
            melhor_solucao = sol_refinada

    if melhor_solucao is None:
        return set()

    return melhor_solucao


def cobertura_2aprox(grafo: Grafo) -> Set[int]:
    """
    Heurística Clássica de 2-Aproximação (Emparelhamento Maximal):
    Itera sobre as arestas. Ao encontrar uma aresta {u, v} ainda descoberta,
    adiciona ambos os extremos u e v à cobertura e descarta todas as arestas incidentes em u ou v.
    Garante teoricamente |S| <= 2 * |S*| e roda em tempo linear O(|V| + |E|).
    """
    arestas = list(extrair_arestas(grafo))
    cobertura: Set[int] = set()

    for u, v in arestas:
        if u not in cobertura and v not in cobertura:
            cobertura.add(u)
            cobertura.add(v)

    return cobertura


def cobertura_gulosa_com_tempo(grafo: Grafo) -> Tuple[Set[int], float]:
    """
    Executa a cobertura gulosa e retorna: (conjunto_vertices, tempo_execucao_em_ms)
    """
    t0 = time.perf_counter()
    solucao = cobertura_gulosa(grafo)
    t1 = time.perf_counter()
    return solucao, (t1 - t0) * 1000.0


def cobertura_heuristica_com_tempo(
    grafo: Grafo,
    num_iteracoes: int = 25,
    alpha: float = 0.85,
    seed: Optional[int] = 42
) -> Tuple[Set[int], float]:
    """
    Executa a meta-heurística GRASP com busca local e retorna: (conjunto_vertices, tempo_execucao_em_ms)
    """
    t0 = time.perf_counter()
    solucao = cobertura_heuristica(grafo, num_iteracoes=num_iteracoes, alpha=alpha, seed=seed)
    t1 = time.perf_counter()
    return solucao, (t1 - t0) * 1000.0


def cobertura_2aprox_com_tempo(grafo: Grafo) -> Tuple[Set[int], float]:
    """
    Executa a heurística de 2-aproximação e retorna: (conjunto_vertices, tempo_execucao_em_ms)
    """
    t0 = time.perf_counter()
    solucao = cobertura_2aprox(grafo)
    t1 = time.perf_counter()
    return solucao, (t1 - t0) * 1000.0


def comparar_coberturas(grafo: Grafo) -> Dict[str, dict]:
    """
    Executa os métodos de cobertura sobre o grafo, valida formalmente a integridade
    e retorna um resumo comparativo com cardinalidade, tempo de execução e validação.
    """
    cob_g, tempo_g = cobertura_gulosa_com_tempo(grafo)
    cob_h, tempo_h = cobertura_heuristica_com_tempo(grafo)
    cob_2a, tempo_2a = cobertura_2aprox_com_tempo(grafo)

    return {
        "guloso": {
            "cardinalidade": len(cob_g),
            "tempo_ms": tempo_g,
            "valido": eh_cobertura_valida(grafo, cob_g),
            "vertices": sorted(cob_g),
        },
        "heuristica_grasp": {
            "cardinalidade": len(cob_h),
            "tempo_ms": tempo_h,
            "valido": eh_cobertura_valida(grafo, cob_h),
            "vertices": sorted(cob_h),
        },
        "heuristica_2aprox": {
            "cardinalidade": len(cob_2a),
            "tempo_ms": tempo_2a,
            "valido": eh_cobertura_valida(grafo, cob_2a),
            "vertices": sorted(cob_2a),
        },
    }


if __name__ == "__main__":
    import os

    caminho = os.path.join("instancias", "instancia1.txt")
    if os.path.exists(caminho):
        g = Grafo.carregar_de_arquivo(caminho)
        rel = comparar_coberturas(g)
        print("=== Teste Comparativo de Cobertura (Instância 1) ===")
        print(f"Guloso:      {rel['guloso']['cardinalidade']} nós ({rel['guloso']['tempo_ms']:.4f} ms) | Válido: {rel['guloso']['valido']}")
        print(f"GRASP:       {rel['heuristica_grasp']['cardinalidade']} nós ({rel['heuristica_grasp']['tempo_ms']:.4f} ms) | Válido: {rel['heuristica_grasp']['valido']}")
        print(f"2-Aprox:     {rel['heuristica_2aprox']['cardinalidade']} nós ({rel['heuristica_2aprox']['tempo_ms']:.4f} ms) | Válido: {rel['heuristica_2aprox']['valido']}")
