import os
import sys
from grafo import Grafo

# Importa as funções dos módulos dos colegas com fallback para None,
# permitindo testar o menu mesmo antes de eles finalizarem suas partes.
try:
    from conectividade import busca_em_largura, componentes_conexas_roy
except (ImportError, ModuleNotFoundError):
    busca_em_largura = None
    componentes_conexas_roy = None

try:
    from caminhos_analise import dijkstra, possui_ciclo, verificar_articulacao
except (ImportError, ModuleNotFoundError):
    dijkstra = None
    possui_ciclo = None
    verificar_articulacao = None


def exibir_menu() -> None:
    # Exibe o menu principal com as opções de 1 a 10 sugeridas no trabalho
    print("\n" + "=" * 40)
    print("        ANÁLISE DE REDE SOCIAL")
    print("=" * 40)
    print("1  - Informar ordem do grafo")
    print("2  - Informar tamanho do grafo")
    print("3  - Calcular densidade")
    print("4  - Informar vizinhos de um vértice")
    print("5  - Informar grau de um vértice")
    print("6  - Verificar se um vértice é articulação")
    print("7  - Executar busca em largura")
    print("8  - Identificar componentes conexas")
    print("9  - Verificar existência de ciclos")
    print("10 - Calcular caminhos mínimos")
    print("0  - Sair")
    print("=" * 40)


def ler_vertice(grafo: Grafo, mensagem: str) -> int:
    # Lê um vértice do teclado e valida se ele pertence ao intervalo [1, N]
    while True:
        try:
            v = int(input(mensagem))
            if 1 <= v <= grafo.ordem():
                return v
            print(f"[!] Vértice inválido! Escolha um valor entre 1 e {grafo.ordem()}.")
        except ValueError:
            print("[!] Digite um número inteiro válido.")


def main():
    print("=" * 40)
    print("  TP01 - BIBLIOTECA DE GRAFOS")
    print("=" * 40)

    # Solicita o arquivo e carrega a estrutura do grafo
    caminho = input("Caminho do arquivo do grafo (ex: instancias/instancia1.txt): ").strip()
    if not os.path.exists(caminho):
        print(f"[ERRO] Arquivo '{caminho}' não encontrado.")
        sys.exit(1)

    try:
        grafo = Grafo.carregar_de_arquivo(caminho)
        print(f"[OK] Grafo carregado com sucesso (|V| = {grafo.ordem()}).")
    except Exception as e:
        print(f"[ERRO] Falha ao carregar grafo: {e}")
        sys.exit(1)

    # Loop de interação com o usuário
    while True:
        exibir_menu()
        opcao = input("Opção: ").strip()

        match opcao:
            # 1. Ordem do grafo
            case "1":
                print(f"\n-> Ordem do grafo (|V|): {grafo.ordem()}")

            # 2. Tamanho do grafo
            case "2":
                print(f"\n-> Tamanho do grafo (|E|): {grafo.tamanho()}")

            # 3. Densidade do grafo
            case "3":
                print(f"\n-> Densidade epsilon(G) (|E|/|V|): {grafo.densidade():.4f}")
                print(f"-> Densidade relativa: {grafo.densidade_relativa():.4f}")

            # 4. Vizinhos de um vértice
            case "4":
                v = ler_vertice(grafo, "Vértice para consultar vizinhos: ")
                print(f"\n-> Vizinhos do vértice {v}: {grafo.vizinhos(v)}")

            # 5. Grau de um vértice
            case "5":
                v = ler_vertice(grafo, "Vértice para consultar grau: ")
                print(f"\n-> Grau do vértice {v}: {grafo.grau(v)}")

            # 6. Vértice de articulação (Módulo Gabriel / Aluno 3)
            case "6":
                if verificar_articulacao is None:
                    print("\n[PENDENTE] Função ainda não implementada em caminhos_analise.py (Gabriel).")
                    continue
                v = ler_vertice(grafo, "Vértice para verificar articulação: ")
                try:
                    eh_art = verificar_articulacao(grafo, v)
                    print(f"\n-> Vértice {v} é de articulação: {'SIM' if eh_art else 'NÃO'}")
                except Exception as e:
                    print(f"\n[ERRO]: {e}")

            # 7. Busca em largura (Módulo Pedro)
            case "7":
                v = ler_vertice(grafo, "Vértice inicial para busca em largura: ")
                try:
                    visitados, arvore, fora_arvore = busca_em_largura(grafo, v)
                    print(f"\n-> Vértices visitados (BFS): {visitados}")
                    print(f"-> Arestas da árvore: {arvore}")
                    print(f"-> Arestas fora da árvore: {fora_arvore}")
                except Exception as e:
                    print(f"\n[ERRO]: {e}")

            # 8. Componentes conexas (Módulo Pedro)
            case "8":
                if componentes_conexas_roy is None:
                    print("\n[PENDENTE] Função ainda não implementada em conectividade.py (Pedro).")
                    continue
                try:
                    qtd, componentes = componentes_conexas_roy(grafo)
                    print(f"\n-> Quantidade de componentes conexas: {qtd}")
                    for i, comp in enumerate(componentes, start=1):
                        print(f"   Componente {i}: {comp}")
                except Exception as e:
                    print(f"\n[ERRO]: {e}")

            # 9. Detecção de ciclos (Módulo Gabriel)
            case "9":
                if possui_ciclo is None:
                    print("\n[PENDENTE] Função ainda não implementada em caminhos_analise.py (Gabriel).")
                    continue
                try:
                    tem_ciclo = possui_ciclo(grafo)
                    print(f"\n-> Possui ciclo: {'SIM' if tem_ciclo else 'NÃO'}")
                except Exception as e:
                    print(f"\n[ERRO]: {e}")

            # 10. Caminhos mínimos (Módulo Gabriel)
            case "10":
                if dijkstra is None:
                    print("\n[PENDENTE] Função ainda não implementada em caminhos_analise.py (Gabriel).")
                    continue
                origem = ler_vertice(grafo, "Vértice de origem: ")
                try:
                    distancias, caminhos = dijkstra(grafo, origem)
                    print(f"\n-> Caminhos mínimos a partir do vértice {origem}:")
                    for destino in range(1, grafo.ordem() + 1):
                        d = distancias.get(destino, float("inf"))
                        rota = caminhos.get(destino, [])
                        if d == float("inf"):
                            print(f"   Destino {destino}: Inalcançável")
                        else:
                            rota_str = " -> ".join(map(str, rota))
                            print(f"   Destino {destino}: Distância = {d:.2f} | Rota: [{rota_str}]")
                except Exception as e:
                    print(f"\n[ERRO]: {e}")

            # 0. Sair do programa
            case "0":
                print("\nEncerrando...")
                break

            # Opção inválida (default)
            case _:
                print("[!] Opção inválida.")


if __name__ == "__main__":
    main()
