import math
import heapq

def calcular_distancia_total(rota):
    distancia = 0
    for i in range(len(rota) - 1):
        dx = rota[i+1]['x'] - rota[i]['x']
        dy = rota[i+1]['y'] - rota[i]['y']
        distancia += math.sqrt(dx*dx + dy*dy)
    return distancia

def dijkstra(grafo, inicio, fim):
    fila = []
    heapq.heappush(fila, (0, inicio))
    distancias = {no: float('inf') for no in grafo}
    distancias[inicio] = 0

    while fila:
        custo_atual, no_atual = heapq.heappop(fila)

        if no_atual == fim:
            return custo_atual

        if custo_atual > distancias[no_atual]:
            continue

        for vizinho, peso in grafo[no_atual].items():
            nova_dist = custo_atual + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                heapq.heappush(fila, (nova_dist, vizinho))

    return float('inf')  # caminho não encontrado

def calcular_custo(solucao, capacidade_maxima, grafo):
    custo_total = 0
    penalidade = 0

    for rota in solucao:
        carga_total = sum(p.get('carga', 1) for p in rota)

        for i in range(len(rota) - 1):
            origem = rota[i]['id']
            destino = rota[i+1]['id']
            dist = dijkstra(grafo, origem, destino)
            if dist == float('inf'):
                penalidade += 10000  # rota inválida
            else:
                custo_total += dist

        if carga_total > capacidade_maxima:
            penalidade += (carga_total - capacidade_maxima) * 1000

    return custo_total + penalidade

def rota_valida(rota, adjacencias):
    for i in range(len(rota) - 1):
        if rota[i+1]['id'] not in adjacencias.get(rota[i]['id'], {}):
            return False
    return True