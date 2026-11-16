# Pasta de Imagens do Relatório LaTeX

Coloque aqui as imagens e diagramas gerados para o relatório:
- `instancia1.png`: Diagrama ou captura da topologia da Instância 1.
- `instancia2.png`: Diagrama ou captura do grafo desconexo da Instância 2.

Para incluir uma imagem no relatório LaTeX (`relatorio.tex`), basta descomentar a linha do `\includegraphics` dentro do ambiente `figure`:

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.7\textwidth]{imagens/instancia1.png}
    \caption{Topologia da rede social para a Instância 1.}
    \label{fig:instancia1}
\end{figure}
```
