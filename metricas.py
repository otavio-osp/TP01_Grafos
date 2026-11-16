from grafo import Grafo
from caminhos_analise import dijkstra


def excentricidade(grafo: Grafo, v: int) -> float:
    # A excentricidade de v é a maior distância mínima dele até qualquer outro vértice
    distancias, _ = dijkstra(grafo, v)

    # Se algum vértice não for alcançável, o grafo é desconexo a partir de v
    if any(d == float("inf") for d in distancias.values()):
        return float("inf")

    return max(distancias.values())


def calcular_todas_excentricidades(grafo: Grafo) -> dict[int, float]:
    n = grafo.ordem()
    return {v: excentricidade(grafo, v) for v in range(1, n + 1)}


def diametro(grafo: Grafo) -> tuple[float, list[int]]:
    excentricidades = calcular_todas_excentricidades(grafo)
    maior_valor = max(excentricidades.values())
    vertices = [v for v, exc in excentricidades.items() if exc == maior_valor]
    return maior_valor, vertices


def raio(grafo: Grafo) -> tuple[float, list[int]]:
    excentricidades = calcular_todas_excentricidades(grafo)
    menor_valor = min(excentricidades.values())
    centro = [v for v, exc in excentricidades.items() if exc == menor_valor]
    return menor_valor, centro


if __name__ == "__main__":
    import os

    caminho = os.path.join("instancias", "instancia1.txt")
    if os.path.exists(caminho):
        g = Grafo.carregar_de_arquivo(caminho)
        excs = calcular_todas_excentricidades(g)
        d_val, d_verts = diametro(g)
        r_val, r_verts = raio(g)

        print("Excentricidades:")
        for v, val in excs.items():
            print(f"  Vértice {v}: {val:.2f}")

        print(f"\nDiâmetro: {d_val:.2f} | Vértices: {d_verts}")
        print(f"Raio: {r_val:.2f} | Centro: {r_verts}")
