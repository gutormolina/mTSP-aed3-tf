import pandas as pd
import matplotlib.pyplot as plt
import math
import os

def carregar_pontos(path):
    df = pd.read_csv(path)
    if 'carga' not in df.columns:
        df['carga'] = 1  # atribui carga padrão
    return df[['id', 'x', 'y', 'carga']].to_dict(orient='records')

def carregar_adjacencias(path, pontos):
    df = pd.read_csv(path)
    # Map id -> ponto
    pontos_dict = {p['id']: p for p in pontos}
    adj = {}
    for _, row in df.iterrows():
        a, b = int(row['from_id']), int(row['to_id'])
        p_a, p_b = pontos_dict[a], pontos_dict[b]
        dx = p_b['x'] - p_a['x']
        dy = p_b['y'] - p_a['y']
        dist = math.sqrt(dx*dx + dy*dy)
        adj.setdefault(a, {})[b] = dist
        adj.setdefault(b, {})[a] = dist
    return adj


def plotar_pontos(pontos, rotas=None, adjacencias=None, salvar_em=None):
    import matplotlib.pyplot as plt
    import os

    plt.figure(figsize=(8, 6))

    # Desenha o grafo de ruas
    if adjacencias:
        for a, vizinhos in adjacencias.items():
            p_a = next(p for p in pontos if p['id'] == a)
            for b in vizinhos:
                p_b = next(p for p in pontos if p['id'] == b)
                plt.plot([p_a['x'], p_b['x']], [p_a['y'], p_b['y']], color='lightgray', linestyle='-', linewidth=2)

    # Pontos
    for ponto in pontos:
        plt.scatter(ponto['x'], ponto['y'], color='blue')
        plt.text(ponto['x'], ponto['y'], str(ponto['id']), fontsize=9)

    # Rotas
    if rotas:
        cores = ['red', 'green', 'orange', 'purple']
        for i, rota in enumerate(rotas):
            xs = [p['x'] for p in rota]
            ys = [p['y'] for p in rota]
            plt.plot(xs, ys, color=cores[i % len(cores)], linestyle='--', linewidth=2, marker='o')

    plt.title('Pontos de Coleta e Rotas')
    plt.grid()

    if salvar_em:
        plt.savefig(os.path.join(salvar_em, "rotas_geradas.png"))
    else:
        plt.savefig("output/rotas_geradas.png")
