from typing import List, Optional


class Grafo:
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        # Matriz de adjacência (N+1) x (N+1) inicializada com None para indicar ausência de aresta.
        # A posição 0 é ignorada para permitir indexação direta de 1 a N.
        self.matriz: List[List[Optional[float]]] = [
            [None] * (num_vertices + 1) for _ in range(num_vertices + 1)
        ]

    def adicionar_aresta(self, u: int, v: int, peso: float) -> None:
        # Define o peso da aresta nos dois sentidos, pois o grafo é não direcionado
        self.matriz[u][v] = peso
        self.matriz[v][u] = peso

    def tem_aresta(self, u: int, v: int) -> bool:
        # Retorna True se houver aresta entre u e v (valor diferente de None)
        return self.matriz[u][v] is not None

    def obter_peso(self, u: int, v: int) -> Optional[float]:
        # Retorna o peso associado à aresta ou None se ela não existir
        return self.matriz[u][v]

    @classmethod
    def carregar_de_arquivo(cls, caminho_arquivo: str) -> "Grafo":
        # Lê o arquivo ignorando linhas em branco e comentários iniciados por '#'
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            linhas = [linha.strip() for linha in f if linha.strip() and not linha.strip().startswith("#")]

        # A primeira linha define o número total de vértices
        num_vertices = int(linhas[0])
        grafo = cls(num_vertices)

        # As linhas seguintes definem as arestas: vértice origem, destino e peso
        for linha in linhas[1:]:
            partes = linha.split()
            u, v, peso = int(partes[0]), int(partes[1]), float(partes[2])
            grafo.adicionar_aresta(u, v, peso)

        return grafo

    def ordem(self) -> int:
        # Retorna o número total de vértices (|V|)
        return self.num_vertices

    def tamanho(self) -> int:
        # Conta as arestas únicas no triângulo superior da matriz para não contar arestas duplicadas
        count = 0
        for i in range(1, self.num_vertices + 1):
            for j in range(i, self.num_vertices + 1):
                if self.matriz[i][j] is not None:
                    count += 1
        return count

    def densidade(self) -> float:
        # Calcula a densidade ε(G) = |E| / |V| (razão arestas por vértice)
        v = self.ordem()
        if v == 0:
            return 0.0
        return self.tamanho() / v

    def densidade_relativa(self) -> float:
        # Calcula a densidade normalizada entre 0 e 1: 2*|E| / (|V|*(|V|-1))
        v = self.ordem()
        if v <= 1:
            return 0.0
        return (2.0 * self.tamanho()) / (v * (v - 1))

    def vizinhos(self, v: int) -> List[int]:
        # Retorna todos os vértices ligados a 'v' (adjacências na linha v da matriz)
        if v < 1 or v > self.num_vertices:
            return []
        return [u for u in range(1, self.num_vertices + 1) if self.matriz[v][u] is not None]

    def grau(self, v: int) -> int:
        # Retorna o grau do vértice (quantidade de vizinhos conectados a ele)
        return len(self.vizinhos(v))


if __name__ == "__main__":
    import os
    caminho = os.path.join("instancias", "instancia1.txt")
    if os.path.exists(caminho):
        g = Grafo.carregar_de_arquivo(caminho)
        print(f"Ordem: {g.ordem()} | Tamanho: {g.tamanho()} | Densidade: {g.densidade():.4f}")
        print(f"Vizinhos do vértice 5: {g.vizinhos(5)} | Grau: {g.grau(5)}")
