import os
import sys
import time

# Garante que o diretório raiz está no path
diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if diretorio_raiz not in sys.path:
    sys.path.insert(0, diretorio_raiz)

from grafo import Grafo
from agm import kruskal, prim
from metricas import diametro, raio
from cobertura import (
    cobertura_gulosa,
    cobertura_heuristica,
    cobertura_2aprox,
    poda_redundancias,
    eh_cobertura_valida,
    cobertura_gulosa_com_tempo,
    cobertura_heuristica_com_tempo,
    cobertura_2aprox_com_tempo,
    comparar_coberturas,
)


def testar_corretude_cobertura_pequena():
    print("\n--- [1] Testando Algoritmos de Cobertura em Grafo Pequeno Sintético ---")
    # Grafo estrela com 5 pontas: vértice 1 conectado a 2, 3, 4, 5, 6
    # Cobertura ótima é apenas {1} (tamanho 1)
    g = Grafo(6)
    for v in range(2, 7):
        g.adicionar_aresta(1, v, 1.0)

    # 1. Teste do Guloso
    cob_g = cobertura_gulosa(g)
    assert eh_cobertura_valida(g, cob_g), "Guloso deve gerar cobertura válida"
    assert cob_g == {1}, f"Em grafo estrela, guloso deve selecionar {{1}}, obteve {cob_g}"
    print("[OK] Cobertura Gulosa em Grafo Estrela: Selecionou apenas o centro {1}")

    # 2. Teste do GRASP
    cob_h = cobertura_heuristica(g, num_iteracoes=10)
    assert eh_cobertura_valida(g, cob_h), "GRASP deve gerar cobertura válida"
    assert cob_h == {1}, f"GRASP deve encontrar solução ótima {{1}}, obteve {cob_h}"
    print("[OK] Cobertura GRASP em Grafo Estrela: Selecionou {1}")

    # 3. Teste de Poda de Redundâncias
    # Se passarmos {1, 2, 3}, os nós 2 e 3 são redundantes pois 1 já cobre tudo
    cobertura_com_redundancia = {1, 2, 3}
    podada = poda_redundancias(g, cobertura_com_redundancia)
    assert podada == {1}, f"Poda deveria remover 2 e 3, obteve {podada}"
    print("[OK] Poda de Redundâncias: Removeu nós desnecessários com sucesso")


def testar_instancia2():
    print("\n--- [2] Validando Instância 2 (Planejamento Estrutural e Cobertura) ---")
    caminho = os.path.join(diretorio_raiz, "instancias", "instancia2.txt")
    assert os.path.exists(caminho), f"Arquivo {caminho} não encontrado"
    g = Grafo.carregar_de_arquivo(caminho)

    # Requisitos Obrigatórios:
    # 1. Tamanho entre 16 e 30 vértices
    assert 16 <= g.ordem() <= 30, f"Ordem fora do intervalo [16, 30]: {g.ordem()}"
    print(f"[OK] Ordem dentro do padrão: {g.ordem()} vértices")

    # 2. Grafo conexo (AGM deve ter n-1 arestas e cobrir todos os nós)
    arestas_k, custo_k = kruskal(g)
    assert len(arestas_k) == g.ordem() - 1, "Grafo deve ser estritamente conexo"
    print(f"[OK] Conectividade validada: AGM possui {len(arestas_k)} arestas (Custo: {custo_k:.2f})")

    # 3. Validação de pesos repetidos (desempate de AGM)
    pesos = [g.obter_peso(u, v) for u in range(1, g.ordem() + 1) for v in range(u + 1, g.ordem() + 1) if g.tem_aresta(u, v)]
    pesos_unicos = set(pesos)
    assert len(pesos) > len(pesos_unicos), "Deve conter pesos repetidos para avaliar desempate de AGM"
    print(f"[OK] Pesos repetidos confirmados: {len(pesos)} arestas e {len(pesos_unicos)} pesos distintos")

    # 4. Falha controlada no Circuito Euleriano: deve ter vértices de grau ímpar
    graus_impares = [v for v in range(1, g.ordem() + 1) if g.grau(v) % 2 != 0]
    assert len(graus_impares) > 0, "Instância 2 deve conter vértices de grau ímpar para testar ausência de circuito Euleriano"
    print(f"[OK] Vértices ímpares detectados: {len(graus_impares)} vértices (ex: nós {graus_impares[:4]}...)")

    # 5. Avaliação de Cobertura
    rel = comparar_coberturas(g)
    assert rel["guloso"]["valido"], "Solução gulosa deve ser válida"
    assert rel["heuristica_grasp"]["valido"], "Solução GRASP deve ser válida"
    print(f"[OK] Cobertura Gulosa: {rel['guloso']['cardinalidade']} nós ({rel['guloso']['tempo_ms']:.3f} ms)")
    print(f"[OK] Cobertura GRASP:  {rel['heuristica_grasp']['cardinalidade']} nós ({rel['heuristica_grasp']['tempo_ms']:.3f} ms)")
    print(f"[OK] Cobertura 2-Aprox:{rel['heuristica_2aprox']['cardinalidade']} nós ({rel['heuristica_2aprox']['tempo_ms']:.3f} ms)")


def testar_instancia4():
    print("\n--- [3] Validando Instância 4 (Grafo Denso e Teste de Estresse) ---")
    caminho = os.path.join(diretorio_raiz, "instancias", "instancia4.txt")
    assert os.path.exists(caminho), f"Arquivo {caminho} não encontrado"
    g = Grafo.carregar_de_arquivo(caminho)

    # Requisitos Obrigatórios:
    # 1. Vértices no intervalo 201 a 1.000
    assert 201 <= g.ordem() <= 1000, f"Ordem fora do intervalo [201, 1000]: {g.ordem()}"
    print(f"[OK] Ordem no intervalo: {g.ordem()} vértices")

    # 2. Densidade relativa entre 30% e 50%
    dens = g.densidade_relativa()
    assert 0.30 <= dens <= 0.50, f"Densidade fora do intervalo [0.30, 0.50]: {dens:.4f}"
    print(f"[OK] Densidade relativa em conformidade: {dens*100:.2f}% ({g.tamanho()} arestas)")

    # 3. Conectividade
    arestas_k, custo_k = kruskal(g)
    assert len(arestas_k) == g.ordem() - 1, "Grafo denso deve ser conexo"
    print(f"[OK] Conexão confirmada via AGM: Custo total {custo_k:.2f}")

    # 4. Teste de Estresse de Cobertura e Instrumentação de Tempo
    cob_g, tg = cobertura_gulosa_com_tempo(g)
    cob_h, th = cobertura_heuristica_com_tempo(g, num_iteracoes=15)
    cob_2a, t2a = cobertura_2aprox_com_tempo(g)

    assert eh_cobertura_valida(g, cob_g), "Guloso deve ser válido na instância 4"
    assert eh_cobertura_valida(g, cob_h), "GRASP deve ser válido na instância 4"
    assert eh_cobertura_valida(g, cob_2a), "2-Aprox deve ser válida na instância 4"

    print(f"[OK] Guloso:    {len(cob_g)} vértices cobertos em {tg:.2f} ms")
    print(f"[OK] GRASP:     {len(cob_h)} vértices cobertos em {th:.2f} ms")
    print(f"[OK] 2-Aprox:   {len(cob_2a)} vértices cobertos em {t2a:.2f} ms")


def testar_integracao_todas_instancias():
    print("\n--- [4] Teste Integrado nas 4 Instâncias Padronizadas ---")
    arquivos = ["instancia1.txt", "instancia2.txt", "instancia3.txt", "instancia4.txt"]
    for arq in arquivos:
        caminho = os.path.join(diretorio_raiz, "instancias", arq)
        g = Grafo.carregar_de_arquivo(caminho)
        res = comparar_coberturas(g)
        assert res["guloso"]["valido"], f"Guloso falhou em {arq}"
        assert res["heuristica_grasp"]["valido"], f"GRASP falhou em {arq}"
        assert res["heuristica_2aprox"]["valido"], f"2-Aprox falhou em {arq}"
        print(f"[OK] {arq:14s} -> Guloso: {res['guloso']['cardinalidade']:3d} nós ({res['guloso']['tempo_ms']:7.3f} ms) | "
              f"GRASP: {res['heuristica_grasp']['cardinalidade']:3d} nós ({res['heuristica_grasp']['tempo_ms']:8.3f} ms)")


if __name__ == "__main__":
    print("=" * 65)
    print("  TESTES INDEPENDENTES - INTEGRANTE 3 (OTÁVIO PEDROSO - 6593)")
    print("=" * 65)
    testar_corretude_cobertura_pequena()
    testar_instancia2()
    testar_instancia4()
    testar_integracao_todas_instancias()
    print("\n" + "=" * 65)
    print("  TODOS OS TESTES DO INTEGRANTE 3 PASSARAM COM SUCESSO!")
    print("=" * 65 + "\n")
