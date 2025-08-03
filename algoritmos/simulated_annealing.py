import random
import math
from core.utils import calcular_custo, rota_valida

def simulated_annealing(pontos, num_veiculos, capacidade_maxima,
                        temperatura_inicial=1000, taxa_resfriamento=0.995, iter_max=10000,
                        adjacencias=None):
    
    solucao = gerar_solucao_inicial(pontos, num_veiculos)
    melhor_solucao = solucao
    melhor_custo = calcular_custo(solucao, capacidade_maxima, adjacencias)
    T = temperatura_inicial

    for _ in range(iter_max):
        vizinho = gerar_vizinho(solucao, adjacencias)
        custo_vizinho = calcular_custo(vizinho, capacidade_maxima, adjacencias)
        delta = custo_vizinho - melhor_custo

        if delta < 0 or random.random() < math.exp(-delta / T):
            solucao = vizinho
            if custo_vizinho < melhor_custo:
                melhor_solucao = vizinho
                melhor_custo = custo_vizinho

        T *= taxa_resfriamento

    return melhor_solucao, melhor_custo

def gerar_solucao_inicial(pontos, num_veiculos):
    random.shuffle(pontos)
    return [pontos[i::num_veiculos] for i in range(num_veiculos)]

def gerar_vizinho(solucao, adjacencias):
    import random
    vizinho = [rota[:] for rota in solucao]

    # escolhe uma rota aleatória que tenha pelo menos 2 pontos
    rotas_validas = [r for r in vizinho if len(r) >= 2]
    if not rotas_validas:
        return vizinho
    rota = random.choice(rotas_validas)
    i_rota = vizinho.index(rota)

    # tenta encontrar um par de índices consecutivos na rota que sejam vizinhos no grafo
    pares_consecutivos = [(i, i+1) for i in range(len(rota)-1)
                         if rota[i+1]['id'] in adjacencias.get(rota[i]['id'], {})]

    if not pares_consecutivos:
        return vizinho  # não há pares consecutivos vizinhos para trocar

    # escolhe um par aleatório para trocar
    a, b = random.choice(pares_consecutivos)

    # troca os dois pontos na rota
    vizinho[i_rota][a], vizinho[i_rota][b] = vizinho[i_rota][b], vizinho[i_rota][a]

    # garante que a rota ainda é válida após a troca (se não for, retorna solução antiga)
    if not rota_valida(vizinho[i_rota], adjacencias):
        return solucao  # rejeita vizinho inválido

    return vizinho