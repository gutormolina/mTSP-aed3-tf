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
    
    # Desenha o grafo de ruas (fundo cinza)
    if adjacencias:
        for a, vizinhos in adjacencias.items():
            p_a = pontos_dict[a]
            for b in vizinhos:
                p_b = pontos_dict[b]
                plt.plot([p_a['x'], p_b['x']], [p_a['y'], p_b['y']], 
                         color='lightgray', linestyle='-', linewidth=1, zorder=1)

    # Desenha os pontos
    for p in pontos:
        if p['id'] == 0:  # Depósito
            plt.scatter(p['x'], p['y'], color='gold', s=150, marker='s', edgecolors='black', zorder=4)
        else:  # Pontos de coleta
            plt.scatter(p['x'], p['y'], color='red', s=100, zorder=3)
        plt.text(p['x'], p['y'], str(p['id']), 
                 fontsize=8, ha='center', va='center', zorder=5)

    # Desenha as rotas com offset
    if rotas and adjacencias:
        cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        offset_step = 0.3  # Valor do deslocamento
        
        for i, rota in enumerate(rotas):
            cor = cores[i % len(cores)]
            offset_x = offset_step * (i - len(rotas)/2)
            offset_y = offset_step * (i - len(rotas)/2)
            
            for j in range(len(rota) - 1):
                inicio = rota[j]['id']
                fim = rota[j+1]['id']
                
                # Pega o caminho completo entre os pontos
                caminho_ids = reconstruir_caminho(adjacencias, inicio, fim)
                
                # Aplica offset
                xs = [pontos_dict[n]['x'] + offset_x for n in caminho_ids]
                ys = [pontos_dict[n]['y'] + offset_y for n in caminho_ids]
                
                # Desenha a rota
                plt.plot(xs, ys, color=cor, linewidth=2.5, zorder=2,
                         label=f'Caminhão {i+1}' if j == 0 else "")
                
                # Setas de direção
                if len(xs) >= 2:
                    plt.arrow(xs[-2], ys[-2], (xs[-1]-xs[-2])*0.8, (ys[-1]-ys[-2])*0.8,
                              color=cor, width=0.2, length_includes_head=True, zorder=3)

    plt.title('Rotas de Coleta de Lixo', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    if salvar_em:
        os.makedirs(salvar_em, exist_ok=True)
        plt.savefig(os.path.join(salvar_em, "rotas_geradas.png"), dpi=200, bbox_inches='tight')
    else:
        os.makedirs("output", exist_ok=True)
        plt.savefig("output/rotas_geradas.png", dpi=200, bbox_inches='tight')
    plt.close()