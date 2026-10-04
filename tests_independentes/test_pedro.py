import os
import sys

# Garante que o diretório raiz está no path
diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if diretorio_raiz not in sys.path:
    sys.path.insert(0, diretorio_raiz)

from grafo import Grafo
from conectividade import (
    busca_em_largura,
    componentes_conexas_roy,
    verificar_articulacao,
    possui_ciclo,
)


def testar_instancia1():
    print("--- Testando Instancia 1 (Conexo, 10 vertices) ---")
    caminho = os.path.join(diretorio_raiz, "instancias", "instancia1.txt")
    g = Grafo.carregar_de_arquivo(caminho)

    # 1. Componentes Conexas (Roy)
    qtd, comps = componentes_conexas_roy(g)
    assert qtd == 1, f"Esperado 1 componente, obtido {qtd}"
    assert len(comps[0]) == 10
    print("[OK] Componentes conexas: 1 componente com 10 vertices")

    # 2. Articulacao
    art = [v for v in range(1, 11) if verificar_articulacao(g, v)]
    assert art == [], f"Esperado nenhuma articulacao, obtido {art}"
    print("[OK] Articulacoes: Nenhuma (grafo biconexo)")

    # 3. BFS a partir do vertice 1
    vis, arv, fora = busca_em_largura(g, 1)
    assert len(vis) == 10
    assert len(arv) == 9
    assert len(fora) == 4
    print(f"[OK] BFS: {len(vis)} visitados | {len(arv)} arestas arvore | {len(fora)} fora da arvore")

    # 4. Ciclos
    assert possui_ciclo(g) is True
    print("[OK] Possui ciclo: True")


def testar_instancia2():
    print("\n--- Testando Instancia 2 (Desconexo, 12 vertices) ---")
    caminho = os.path.join(diretorio_raiz, "instancias", "instancia2.txt")
    g = Grafo.carregar_de_arquivo(caminho)

    # 1. Componentes Conexas (Roy)
    qtd, comps = componentes_conexas_roy(g)
    assert qtd == 3, f"Esperado 3 componentes, obtido {qtd}"
    print(f"[OK] Componentes conexas: {qtd} componentes ({comps})")

    # 2. Articulacao (apenas vertices 2 e 4)
    art = [v for v in range(1, 13) if verificar_articulacao(g, v)]
    assert set(art) == {2, 4}, f"Esperado {{2, 4}}, obtido {art}"
    print(f"[OK] Articulacoes: {art} (vertices 2 e 4)")

    # 3. BFS a partir do vertice 1
    vis, arv, fora = busca_em_largura(g, 1)
    assert vis == [1, 2, 3, 4, 5]
    assert len(arv) == 4
    assert fora == [(2, 3)]
    print(f"[OK] BFS(1): Visitados={vis} | Arvore={arv} | Fora={fora}")

    # 4. Ciclos
    assert possui_ciclo(g) is True
    print("[OK] Possui ciclo: True")


if __name__ == "__main__":
    print("=" * 50)
    print("  TESTES INDEPENDENTES - PEDRO")
    print("=" * 50)
    testar_instancia1()
    testar_instancia2()
    print("\nTODOS OS TESTES PASSARAM COM SUCESSO!\n")
