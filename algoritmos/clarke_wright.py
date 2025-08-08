import copy
from core.utils import calcular_distancia_total, calcular_custo, rota_valida

def clarke_wright(pontos, num_veiculos, capacidade_maxima, adjacencias):

    rotas = [[ponto] for ponto in pontos]
    
    savings = []
    for i in range(len(pontos)):
        for j in range(i + 1, len(pontos)):
            a, b = pontos[i], pontos[j]
            if a['id'] in adjacencias and b['id'] in adjacencias[a['id']]:
                saving = calcular_distancia_total([a,b])
                savings.append((saving, i, j))
    
    # Ordena savings em ordem decrescente
    savings.sort(reverse=True, key=lambda x: x[0])
    
    # Combina rotas com base nas savings
    for saving, i, j in savings:
        rota_i = next((r for r in rotas if pontos[i] in r), None)
        rota_j = next((r for r in rotas if pontos[j] in r), None)
        
        if rota_i is None or rota_j is None or rota_i == rota_j:
            continue
        
        # Verifica capacidade e valida a rota combinada
        nova_rota = rota_i + rota_j
        carga = sum(p['carga'] for p in nova_rota)
        if carga > capacidade_maxima:
            continue
        
        if rota_valida(nova_rota, adjacencias):
            rotas.remove(rota_i)
            rotas.remove(rota_j)
            rotas.append(nova_rota)
            if len(rotas) <= num_veiculos:
                break

    while len(rotas) > num_veiculos:
        rotas.sort(key=lambda r: sum(p['carga'] for p in r))
        rota1 = rotas.pop(0)
        rota2 = rotas.pop(0)
        rotas.append(rota1 + rota2)
    
    return rotas, calcular_custo(rotas, capacidade_maxima, adjacencias)
