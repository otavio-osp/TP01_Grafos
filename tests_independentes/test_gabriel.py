import os
import sys

# Garante que o diretório raiz está no path
diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if diretorio_raiz not in sys.path:
    sys.path.insert(0, diretorio_raiz)

from grafo import Grafo
from euler import tem_circuito_euleriano, circuito_euleriano
from agm import kruskal, prim
from metricas import calcular_todas_excentricidades, diametro, raio
from cobertura import cobertura_gulosa, cobertura_heuristica, eh_cobertura_valida


def testar_grafo_sintetico_euleriano():
    print("\n--- [1] Testando Circuito Euleriano em Grafo Sintético (Ciclo C4) ---")
    g = Grafo(4)
    g.adicionar_aresta(1, 2, 1.0)
    g.adicionar_aresta(2, 3, 2.0)
    g.adicionar_aresta(3, 4, 3.0)
    g.adicionar_aresta(4, 1, 4.0)

    assert tem_circuito_euleriano(g), "Ciclo C4 com graus todos iguais a 2 deve ser Euleriano"
    circuito = circuito_euleriano(g)
    assert circuito is not None, "Circuito não deve ser None"
    assert len(circuito) == 5, f"Circuito de C4 deve ter 5 vértices (4 arestas + retorno), obteve {len(circuito)}"
    assert circuito[0] == circuito[-1], "Circuito deve começar e terminar no mesmo vértice"
    print(f"[OK] Grafo Sintético Euleriano validado: {' -> '.join(map(str, circuito))}")


def testar_grafo_sintetico_nao_euleriano():
    print("\n--- [2] Testando Grafo Sintético Não Euleriano (Caminho P3) ---")
    g = Grafo(3)
    g.adicionar_aresta(1, 2, 1.0)
    g.adicionar_aresta(2, 3, 2.0)

    assert not tem_circuito_euleriano(g), "Grafo com vértices de grau ímpar não pode ter circuito Euleriano"
    assert circuito_euleriano(g) is None, "circuito_euleriano deve retornar None quando não existir circuito"
    print("[OK] Detecção de ausência de circuito Euleriano validada com sucesso")


def testar_grafo_desconexo():
    print("\n--- [3] Testando Grafo Desconexo com Subgrafos Pares ---")
    # Dois triângulos desconexos: {1,2,3} e {4,5,6}
    g = Grafo(6)
    g.adicionar_aresta(1, 2, 1.0)
    g.adicionar_aresta(2, 3, 1.0)
    g.adicionar_aresta(3, 1, 1.0)
    g.adicionar_aresta(4, 5, 1.0)
    g.adicionar_aresta(5, 6, 1.0)
    g.adicionar_aresta(6, 4, 1.0)

    # Embora todos tenham grau par, o grafo possui duas componentes conexas com arestas!
    assert not tem_circuito_euleriano(g), "Grafo desconexo não deve admitir circuito Euleriano global"
    assert circuito_euleriano(g) is None
    print("[OK] Requisito de conectividade única validado com sucesso")


def testar_instancia1_completo():
    print("\n--- [4] Validando Instância 1 Oficial (Conferência Completa) ---")
    caminho = os.path.join(diretorio_raiz, "instancias", "instancia1.txt")
    assert os.path.exists(caminho), f"Arquivo {caminho} não encontrado"
    g = Grafo.carregar_de_arquivo(caminho)

    # 1. Ordem entre 8 e 15 vértices
    assert 8 <= g.ordem() <= 15, f"Ordem fora do intervalo permitido: {g.ordem()}"
    print(f"[OK] Ordem validada: {g.ordem()} vértices")

    # 2. Pesos reais positivos todos distintos
    pesos = []
    for u in range(1, g.ordem() + 1):
        for v in range(u + 1, g.ordem() + 1):
            if g.tem_aresta(u, v):
                p = g.obter_peso(u, v)
                assert p > 0, "Peso deve ser positivo"
                pesos.append(p)
    assert len(pesos) == len(set(pesos)), "Todos os pesos devem ser distintos"
    print(f"[OK] Pesos reais positivos e distintos confirmados: {len(pesos)} arestas")

    # 3. Todos os vértices com grau par
    graus_impares = [v for v in range(1, g.ordem() + 1) if g.grau(v) % 2 != 0]
    assert len(graus_impares) == 0, f"Todos os vértices devem ter grau par. Ímpares: {graus_impares}"
    print(f"[OK] Graus pares confirmados em todos os vértices: {[g.grau(v) for v in range(1, g.ordem() + 1)]}")

    # 4. Circuito Euleriano
    assert tem_circuito_euleriano(g), "Instância 1 deve admitir circuito Euleriano"
    circ = circuito_euleriano(g)
    assert circ is not None
    assert len(circ) == g.tamanho() + 1, f"Tamanho do circuito deve ser {g.tamanho() + 1}, obteve {len(circ)}"
    assert circ[0] == circ[-1], "Circuito deve ser fechado"

    # Confere se todas as arestas foram percorridas exatamente uma vez
    arestas_percorridas = set()
    for i in range(len(circ) - 1):
        u, v = circ[i], circ[i + 1]
        e = (min(u, v), max(u, v))
        assert e not in arestas_percorridas, f"Aresta {e} foi repetida no circuito!"
        arestas_percorridas.add(e)
    assert len(arestas_percorridas) == g.tamanho(), "Nem todas as arestas foram percorridas"
    print(f"[OK] Circuito Euleriano verificado: {len(circ) - 1} arestas percorridas sem repetição")
    print(f"     Sequência: {' -> '.join(map(str, circ))}")

    # 5. Árvore Geradora Mínima (Kruskal e Prim)
    arestas_k, custo_k = kruskal(g)
    arestas_p, custo_p = prim(g)
    assert len(arestas_k) == g.ordem() - 1, "AGM deve conter N - 1 arestas"
    assert abs(custo_k - 20.70) < 1e-4, f"Custo da AGM esperado é 20.70, obteve {custo_k:.2f}"
    assert abs(custo_k - custo_p) < 1e-4, "Kruskal e Prim devem convergir para o mesmo custo"
    print(f"[OK] AGM validada: {len(arestas_k)} arestas, custo total = {custo_k:.2f}")

    # 6. Métricas de Distância
    excs = calcular_todas_excentricidades(g)
    val_diam, verts_diam = diametro(g)
    val_raio, verts_raio = raio(g)
    assert abs(val_diam - 11.20) < 1e-4, f"Diâmetro esperado: 11.20, obteve {val_diam:.2f}"
    assert set(verts_diam) == {4, 6}, f"Vértices de diâmetro esperados: {{4, 6}}, obteve {verts_diam}"
    assert abs(val_raio - 7.10) < 1e-4, f"Raio esperado: 7.10, obteve {val_raio:.2f}"
    assert set(verts_raio) == {5}, f"Centro esperado: {{5}}, obteve {verts_raio}"
    print(f"[OK] Métricas de Distância: Diâmetro = {val_diam:.2f} (vértices {verts_diam}), Raio = {val_raio:.2f} (centro {verts_raio})")

    # 7. Cobertura de Vértices
    cob_g = cobertura_gulosa(g)
    cob_h = cobertura_heuristica(g)
    assert eh_cobertura_valida(g, cob_g), "Cobertura Gulosa deve ser válida"
    assert eh_cobertura_valida(g, cob_h), "Cobertura GRASP deve ser válida"
    assert len(cob_g) == 5, f"Esperado 5 vértices para Guloso, obteve {len(cob_g)}"
    assert len(cob_h) == 5, f"Esperado 5 vértices para GRASP, obteve {len(cob_h)}"
    print(f"[OK] Cobertura de Vértices: Guloso = {len(cob_g)} nós, GRASP = {len(cob_h)} nós (solução ótima minimal)")


def testar_instancia2_nao_euleriana():
    print("\n--- [5] Validando Ausência de Circuito Euleriano na Instância 2 ---")
    caminho = os.path.join(diretorio_raiz, "instancias", "instancia2.txt")
    if os.path.exists(caminho):
        g = Grafo.carregar_de_arquivo(caminho)
        assert not tem_circuito_euleriano(g), "Instância 2 deve falhar no teste de circuito Euleriano (possui graus ímpares)"
        assert circuito_euleriano(g) is None
        print("[OK] Falha controlada de circuito Euleriano na Instância 2 confirmada")


if __name__ == "__main__":
    testar_grafo_sintetico_euleriano()
    testar_grafo_sintetico_nao_euleriano()
    testar_grafo_desconexo()
    testar_instancia1_completo()
    testar_instancia2_nao_euleriana()
    print("\n=======================================================")
    print("  TODOS OS TESTES DE GABRIEL FORAM APROVADOS COM SUCESSO! ")
    print("=======================================================\n")
