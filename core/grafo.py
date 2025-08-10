import matplotlib.pyplot as plt
import math
import os
import csv
import heapq

def carregar_pontos(path):
    pontos = []
    with open(path, 'r') as f:
        leitor = csv.reader(f)
        next(leitor)  # pula o cabeçalho
        for id_p, x, y, carga in leitor:
            pontos.append({
                'id': int(id_p),
                'x': float(x),
                'y': float(y),
                'carga': int(carga)
            })
    return pontos

def carregar_adjacencias(path, pontos):
    adj = {}
    pontos_dict = {p['id']: p for p in pontos}
    
    with open(path, 'r') as f:
        leitor = csv.reader(f)
        next(leitor)  # pula o cabeçalho
        
        for from_id, to_id in leitor:
            a, b = int(from_id), int(to_id)
            p_a, p_b = pontos_dict[a], pontos_dict[b]
            
            # Calcula distância euclidiana
            dx = p_b['x'] - p_a['x']
            dy = p_b['y'] - p_a['y']
            dist = math.sqrt(dx**2 + dy**2)
            
            # Adiciona arestas (grafo não-direcionado)
            adj.setdefault(a, {})[b] = dist
            adj.setdefault(b, {})[a] = dist
    
    return adj

def somar_cargas(pontos):
    return sum(ponto['carga'] for ponto in pontos)

def reconstruir_caminho(grafo, inicio, fim):
    """Reconstrói o caminho mais curto entre dois nós usando Dijkstra."""
    fila = [(0, inicio, [inicio])]
    visitados = set()

    while fila:
        custo, atual, caminho = heapq.heappop(fila)

        if atual == fim:
            return caminho

        if atual in visitados:
            continue
        visitados.add(atual)

        for vizinho, peso in grafo[atual].items():
            if vizinho not in visitados:
                heapq.heappush(fila, (custo + peso, vizinho, caminho + [vizinho]))

    return []  # sem caminho

def plotar_pontos(pontos, rotas=None, adjacencias=None, salvar_em=None):
    plt.figure(figsize=(10, 8))
    pontos_dict = {p['id']: p for p in pontos}
    offset = 0.5  # Ajuste conforme necessário

    # Desenha o grafo de ruas (fundo cinza)
    if adjacencias:
        for a, vizinhos in adjacencias.items():
            p_a = pontos_dict[a]
            for b in vizinhos:
                p_b = pontos_dict[b]
                plt.plot([p_a['x'], p_b['x']], [p_a['y'], p_b['y']], 
                         color='lightgray', linestyle='-', linewidth=2, zorder=1)

    # Pontos (azuis)
    for ponto in pontos:
        plt.scatter(ponto['x'], ponto['y'], color='blue', s=100, zorder=3)
        plt.text(ponto['x'], ponto['y'], str(ponto['id']), 
                 fontsize=9, ha='center', va='center', color='white', zorder=4)

    # Rotas (com offset)
    if rotas and adjacencias:
        cores = ['red', 'green', 'orange', 'purple', 'brown', 'pink']
        
        for i, rota in enumerate(rotas):
            cor = cores[i % len(cores)]
            offset_x = offset * (i - len(rotas)/2)  # Centraliza os offsets
            offset_y = offset * (i - len(rotas)/2)
            
            for j in range(len(rota) - 1):
                inicio = rota[j]['id']
                fim = rota[j+1]['id']
                caminho_ids = reconstruir_caminho(adjacencias, inicio, fim)
                
                # Aplica offset
                xs = [pontos_dict[n]['x'] + offset_x for n in caminho_ids]
                ys = [pontos_dict[n]['y'] + offset_y for n in caminho_ids]
                
                plt.plot(xs, ys, color=cor, linestyle='-', linewidth=2, 
                         marker='o', markersize=5, zorder=2, 
                         label=f'Rota {i+1}' if j == 0 else "")

        plt.legend(loc='upper right')

    plt.title('Otimização de Rotas de Coleta', pad=20)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    if salvar_em:
        os.makedirs(salvar_em, exist_ok=True)
        plt.savefig(os.path.join(salvar_em, "rotas_geradas.png"), dpi=300)
    else:
        os.makedirs("output", exist_ok=True)
        plt.savefig("output/rotas_geradas.png", dpi=300)
    plt.close()