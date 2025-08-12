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
            
            # calcula distância euclidiana
            dx = p_b['x'] - p_a['x']
            dy = p_b['y'] - p_a['y']
            dist = math.sqrt(dx**2 + dy**2)
            
            # adiciona arestas (grafo não-direcionado)
            adj.setdefault(a, {})[b] = dist
            adj.setdefault(b, {})[a] = dist
    
    return adj

def detectar_componentes(grafo):
    visitados = set()
    componentes = []

    for nodo in grafo.keys():
        if nodo not in visitados:
            fila = [nodo]
            comp = set()
            while fila:
                atual = fila.pop()
                if atual not in visitados:
                    visitados.add(atual)
                    comp.add(atual)
                    fila.extend(grafo.get(atual, {}).keys())
            componentes.append(comp)
    return componentes

def componente_do_deposito(componentes, deposito_id=0):
    for comp in componentes:
        if deposito_id in comp:
            return comp
    return None

def conectar_componentes(grafo, pontos, deposito_id=0):
    import math

    componentes = detectar_componentes(grafo)
    comp_deposito = componente_do_deposito(componentes, deposito_id)

    if len(componentes) <= 1:
        return grafo

    pontos_dict = {p['id']: p for p in pontos}

    for comp in componentes:
        if comp == comp_deposito:
            continue

        menor_dist = float('inf')
        melhor_aresta = None

        for u in comp_deposito:
            for v in comp:
                p_u = pontos_dict[u]
                p_v = pontos_dict[v]
                dx = p_v['x'] - p_u['x']
                dy = p_v['y'] - p_u['y']
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < menor_dist:
                    menor_dist = dist
                    melhor_aresta = (u, v, dist)

        u, v, dist = melhor_aresta
        grafo.setdefault(u, {})[v] = dist
        grafo.setdefault(v, {})[u] = dist

        comp_deposito.update(comp)

    return grafo

def somar_cargas(pontos):
    return sum(ponto['carga'] for ponto in pontos)

def reconstruir_caminho(grafo, inicio, fim):
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

    return []

def plotar_pontos(pontos, rotas=None, adjacencias=None, salvar_em=None):
    plt.figure(figsize=(10, 8))
    pontos_dict = {p['id']: p for p in pontos}
    
    # desenha o grafo de ruas
    if adjacencias:
        for a, vizinhos in adjacencias.items():
            p_a = pontos_dict[a]
            for b in vizinhos:
                p_b = pontos_dict[b]
                plt.plot([p_a['x'], p_b['x']], [p_a['y'], p_b['y']], 
                         color='lightgray', linestyle='-', linewidth=1, zorder=1)

    # desenha os pontos
    for p in pontos:
        if p['id'] == 0:  # Depósito
            plt.scatter(p['x'], p['y'], color='gold', s=150, marker='s', edgecolors='black', zorder=4)
        else:  # Pontos de coleta
            plt.scatter(p['x'], p['y'], color='red', s=100, zorder=3)
        plt.text(p['x'], p['y'], str(p['id']), 
                 fontsize=8, ha='center', va='center', zorder=5)

    # desenha as rotas com offset
    if rotas and adjacencias:
        cores = ['#1f77b4', 
                 '#ff7f0e', 
                 '#2ca02c', 
                 '#d62728', 
                 '#9467bd', 
                 '#8c564b',
                 '#17becf',
                 '#e377c2']
        offset_step = 0.05
        
        for i, rota in enumerate(rotas):
            cor = cores[i % len(cores)]
            offset_x = offset_step * (i - len(rotas)/2)
            offset_y = offset_step * (i - len(rotas)/2)
            
            for j in range(len(rota) - 1):
                inicio = rota[j]['id']
                fim = rota[j+1]['id']
                
                caminho_ids = reconstruir_caminho(adjacencias, inicio, fim)
                
                xs = [pontos_dict[n]['x'] + offset_x for n in caminho_ids]
                ys = [pontos_dict[n]['y'] + offset_y for n in caminho_ids]
                
                # desenha a rota
                plt.plot(xs, ys, color=cor, linewidth=1.5, zorder=2,
                         label=f'Caminhão {i+1}' if j == 0 else "")
                
                # setas de direção
                if len(xs) >= 2:
                    plt.annotate("",
                        xy=(xs[-1], ys[-1]),
                        xytext=(xs[-2], ys[-2]),
                        arrowprops=dict(arrowstyle="->", color=cor, lw=1.5),
                        zorder=3
                    )

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