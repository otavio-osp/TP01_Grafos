# TP01 — Biblioteca de Grafos (Rede Social)

Biblioteca em Python para manipulação e análise de grafos não direcionados e ponderados com matriz de adjacência.

---

## 👥 Divisão de Tarefas

* **Otávio:** 
  * Estrutura do grafo (`grafo.py`), leitura de arquivo `.txt` e métricas básicas (ordem, tamanho, densidade, vizinhos, grau).
  * Programa principal com menu interativo (`main.py`).
  * Instâncias de teste (`instancias/`).
* **Pedro:** 
  * Busca em Largura (BFS, ordem de visita, árvore e arestas fora da árvore) e Componentes Conexas via Algoritmo de Roy (`conectividade.py`).
* **Gabriel:** 
  * Caminhos mínimos com Dijkstra, detecção de ciclos e verificação de vértice de articulação (`caminhos_analise.py`).

---

## 🚀 Como Executar

```bash
python main.py
```

Informe o caminho da instância desejada (ex: `instancias/instancia1.txt`) e escolha as opções no menu:

* `1` - Ordem do grafo
* `2` - Tamanho do grafo
* `3` - Calcular densidade ε(G)
* `4` - Vizinhos de um vértice
* `5` - Grau de um vértice
* `6` - Verificar vértice de articulação
* `7` - Busca em largura (BFS)
* `8` - Componentes conexas
* `9` - Detecção de ciclos
* `10` - Caminhos mínimos (Dijkstra)
* `0` - Sair
