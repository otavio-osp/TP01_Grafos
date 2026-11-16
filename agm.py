import heapq
from grafo import Grafo


class UnionFind:
    def __init__(self, n: int):
        # Cada vértice começa sendo seu próprio pai
        self.pai = list(range(n + 1))
        self.rank = [0] * (n + 1)

    def encontrar(self, x: int) -> int:
        # Encontra a raiz do conjunto com compressão de caminho
        if self.pai[x] != x:
            self.pai[x] = self.encontrar(self.pai[x])
        return self.pai[x]

    def unir(self, x: int, y: int) -> bool:
        # Retorna False se já estão na mesma componente (evita ciclo)
        rx = self.encontrar(x)
        ry = self.encontrar(y)

        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.pai[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


def kruskal(grafo: Grafo) -> tuple[list[tuple[int, int, float]], float]:
    n = grafo.ordem()

    # Pega apenas arestas com u < v para não duplicar
    arestas = []
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            peso = grafo.obter_peso(u, v)
            if peso is not None:
                arestas.append((peso, u, v))

    # Ordena pelo menor peso
    arestas.sort()

    uf = UnionFind(n)
    agm = []
    custo_total = 0.0

    for peso, u, v in arestas:
        if uf.unir(u, v):
            agm.append((u, v, peso))
            custo_total += peso
            if len(agm) == n - 1:
                break

    return agm, custo_total


def prim(grafo: Grafo, raiz: int = 1) -> tuple[list[tuple[int, int, float]], float]:
    n = grafo.ordem()
    visitado = [False] * (n + 1)
    agm = []
    custo_total = 0.0

    # Heap armazena (peso, u, v)
    heap = []
    visitado[raiz] = True

    for viz in grafo.vizinhos(raiz):
        heapq.heappush(heap, (grafo.obter_peso(raiz, viz), raiz, viz))

    while heap and len(agm) < n - 1:
        peso, u, v = heapq.heappop(heap)

        if visitado[v]:
            continue

        visitado[v] = True
        agm.append((u, v, peso))
        custo_total += peso

        for viz in grafo.vizinhos(v):
            if not visitado[viz]:
                heapq.heappush(heap, (grafo.obter_peso(v, viz), v, viz))

    return agm, custo_total


if __name__ == "__main__":
    import os

    caminho = os.path.join("instancias", "instancia1.txt")
    if os.path.exists(caminho):
        g = Grafo.carregar_de_arquivo(caminho)
        arestas_k, custo_k = kruskal(g)
        arestas_p, custo_p = prim(g)

        print(f"Kruskal - Custo total: {custo_k:.4f}")
        for u, v, p in arestas_k:
            print(f"  ({u}, {v}) peso = {p}")

        print(f"\nPrim - Custo total: {custo_p:.4f}")
        for u, v, p in arestas_p:
            print(f"  ({u}, {v}) peso = {p}")
