# 🎬 ROTEIRO COMPLETO DO VÍDEO — TP02 GRAFOS (CCF-331)

> **Apresentador:** Gabriel Marcos de Oliveira Félix (Matrícula: 5792)  
> **Grupo:** Pedro Mendes Gonzaga (6563), Otávio Soares Pedroso (6593), Gabriel Marcos de Oliveira Félix (5792)  
> **Tempo Alvo:** Entre 7 e 8 minutos (Mínimo: 5 min | Máximo obrigatório: 10 min)  
> **Gravação:** Use OBS Studio ou **Win + G** (Xbox Game Bar do Windows) em 1080p.

---

## CENA 1 — ABERTURA E APRESENTAÇÃO (30 a 45 segundos)

**O que mostrar na tela:** VS Code aberto com os arquivos do projeto visíveis na barra lateral esquerda.

**O que falar:**
> "Olá, professor Marcus e colegas. Meu nome é Gabriel Marcos de Oliveira Félix, matrícula 5792. Junto com os integrantes Pedro Mendes Gonzaga (matrícula 6563) e Otávio Soares Pedroso (matrícula 6593), apresento o Trabalho Prático II da disciplina de Teoria e Modelo de Grafos (CCF-331) da Universidade Federal de Viçosa – Campus Florestal.
> 
> Neste TP2, estendemos a biblioteca modular desenvolvida no TP1, implementando quatro novos grandes módulos: Circuito Euleriano via Algoritmo de Hierholzer, Árvore Geradora Mínima com Kruskal e Prim, Métricas de Distância e Centralidade, e Cobertura Mínima de Vértices comparando abordagem Gulosa e Meta-heurística GRASP."

---

## CENA 2 — ESTRUTURA MODULAR DO PROJETO (45 segundos)

**O que mostrar na tela:** No explorador de arquivos do VS Code, clique brevemente em cada arquivo correspondente enquanto cita seu nome.

**O que falar:**
> "Mantivemos a arquitetura estritamente desacoplada com a matriz de adjacência implementada na classe base `grafo.py`.
> 
> A divisão do trabalho foi estruturada da seguinte forma:
> - O Integrante 1 (minha parte) ficou responsável pelo módulo `euler.py`, implementando a verificação de eulerianidade e o algoritmo de Hierholzer, além do planejamento da `instancia1.txt`, sua validação manual e a gravação deste vídeo explicativo.
> - O Integrante 2 (Pedro) implementou o módulo `agm.py` com Kruskal e Prim, o módulo `metricas.py` com excentricidade, diâmetro e raio, além da `instancia3.txt` e unificação do relatório em LaTeX.
> - O Integrante 3 (Otávio) implementou o módulo `cobertura.py` com algoritmo Guloso e GRASP com busca local, além da geração das instâncias 2 e 4 e seus testes de estresse."

---

## CENA 3 — INSTÂNCIA 1: VALIDAÇÃO COMPLETA E CIRCUITO EULERIANO (2 min a 2 min 30 s)

**O que fazer no terminal:**
Abra o terminal integrado e execute:
```powershell
python main.py
```
Digite:
```
instancias/instancia1.txt
```

**O que falar:**
> "Vamos carregar a `instancia1.txt`. Ela possui 10 vértices e 15 arestas com pesos reais positivos todos distintos. Todos os vértices têm graus pares (grau 2 ou 4), o que garante a existência de um Circuito Euleriano."

**No terminal:** Digite `11` (Circuito Euleriano).
**O que falar:**
> "Na opção 11, o algoritmo de Hierholzer confirma a eulerianidade e extrai a sequência exata:
> `1 -> 3 -> 6 -> 8 -> 10 -> 9 -> 7 -> 8 -> 5 -> 7 -> 4 -> 2 -> 5 -> 3 -> 2 -> 1`.
> Note que todas as 15 arestas do grafo são percorridas exatamente uma única vez, retornando ao vértice 1."

**No terminal:** Digite `12` (Árvore Geradora Mínima).
**O que falar:**
> "Na opção 12, tanto o algoritmo de Kruskal quanto o de Prim convergem exatamente para o mesmo custo total de 20.70, selecionando as 9 arestas mínimas da árvore."

**No terminal:** Digite `13` (Métricas de Distância).
**O que falar:**
> "Na opção 13, temos as excentricidades calculadas via Dijkstra. O diâmetro do grafo é 11.20, correspondente aos nós periféricos 4 e 6, e o raio é 7.10, com o centro topológico no vértice 5."

**No terminal:** Digite `14` (Cobertura Mínima de Vértices).
**O que falar:**
> "Na opção 14, tanto o algoritmo Guloso quanto a heurística GRASP encontram a cobertura ótima global com apenas 5 vértices: os nós 2, 3, 7, 8 e 9. Provamos no relatório que 5 é o limite inferior matemático absoluto devido a um emparelhamento de 5 arestas disjuntas."

**No terminal:** Digite `0` para sair.

---

## CENA 4 — INSTÂNCIA 2: FALHA CONTROLADA E PESOS REPETIDOS (1 min 30 s)

**O que fazer no terminal:**
Execute:
```powershell
python main.py
```
Digite:
```
instancias/instancia2.txt
```

**O que falar:**
> "Agora carregamos a `instancia2.txt`, planejada com 20 vértices e 33 arestas para avaliar desempate de AGM e ausência de circuito Euleriano."

**No terminal:** Digite `11` (Circuito Euleriano).
**O que falar:**
> "Na opção 11, o sistema acusa corretamente que o grafo NÃO possui circuito Euleriano. Isso valida a nossa verificação, pois essa instância possui 16 vértices com grau ímpar."

**No terminal:** Digite `12` (AGM).
**O que falar:**
> "Na opção 12, a instância possui vários pesos repetidos (1.50 e 2.00 repetidos 7 vezes cada). Mesmo com múltiplos empates na ordenação, Kruskal e Prim resolvem com segurança e encontram o custo ótimo de 48.50."

**No terminal:** Digite `14` (Cobertura Mínima).
**O que falar:**
> "Na opção 14, vemos a eficácia da busca local do GRASP: o algoritmo Guloso selecionou 12 vértices em 0.12 ms, enquanto o GRASP eliminou nós redundantes através da poda e encontrou uma cobertura menor, com 11 vértices."

**No terminal:** Digite `0` para sair.

---

## CENA 5 — INSTÂNCIA 3: GRAFO ESPARSO (1 minuto)

**O que fazer no terminal:**
Execute:
```powershell
python main.py
```
Digite:
```
instancias/instancia3.txt
```

**O que falar:**
> "A `instancia3.txt` possui 80 vértices e 114 arestas, sendo um grafo esparso com densidade relativa de apenas 3.6%."

**No terminal:** Digite `12` (AGM).
**O que falar:**
> "A AGM foi determinada com 79 arestas e custo total de 453.90."

**No terminal:** Digite `13` (Métricas).
**O que falar:**
> "Por ter uma estrutura predominantemente ramificada e linear, o diâmetro da rede atinge 85.20 e o raio é 42.90, tendo o nó 75 como centro."

**No terminal:** Digite `14` (Cobertura).
**O que falar:**
> "Na cobertura, tanto o Guloso quanto o GRASP cobrem a rede com 45 vértices."

**No terminal:** Digite `0` para sair.

---

## CENA 6 — INSTÂNCIA 4: TESTE DE ESTRESSE EM REDE DENSA (1 minuto)

**O que fazer no terminal:**
Execute:
```powershell
python main.py
```
Digite:
```
instancias/instancia4.txt
```

**O que falar:**
> "Para finalizar os testes, a `instancia4.txt` é nosso teste de estresse: são 250 vértices e quase 11 mil arestas (10.893 arestas), representando 35% de densidade."

**No terminal:** Digite `12` (AGM).
**O que falar:**
> "Mesmo com mais de 10 mil arestas, o Kruskal com Union-Find otimizado computa a árvore geradora de custo 415.99 em apenas alguns milissegundos."

**No terminal:** Digite `14` (Cobertura).
**O que falar:**
> "Na Cobertura de Vértices, o algoritmo Guloso processou todas as arestas em cerca de 22 ms cobrindo com 237 vértices. Já o GRASP, através da exploração semi-randomizada e busca local, conseguiu reduzir ainda mais e encontrou uma cobertura de 236 vértices. Isso demonstra com clareza o compromisso entre tempo de computação e qualidade da solução."

**No terminal:** Digite `0` para sair.

---

## CENA 7 — CONCLUSÃO (30 segundos)

**O que mostrar na tela:** Terminal limpo ou a primeira página do relatório em PDF.

**O que falar:**
> "Demonstramos assim o funcionamento integral de todos os algoritmos exigidos no TP2. Toda a biblioteca foi desenvolvida em Python sem uso de pacotes externos, validada analiticamente na Instância 1 e estressada em instâncias de até 250 vértices e mais de 10 mil arestas. O relatório em PDF detalha todos os cálculos manuais, complexidades e tabelas comparativas.
> 
> Muito obrigado pela atenção!"

---

> [!TIP]
> **Dicas para uma Gravação Impecável:**
> 1. Respire fundo e leia as falas de forma pausada e tranquila.
> 2. Se gaguejar numa palavra, não pare a gravação: apenas repita a frase com calma.
> 3. O tempo total ficará entre 7 e 8 minutos, bem dentro da margem permitida de até 10 minutos.
