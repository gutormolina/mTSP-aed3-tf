import random
import math
import copy
from core.utils import calcular_custo, rota_valida

def simulated_annealing(pontos, num_veiculos, capacidade_maxima,
                        temperatura_inicial=None, taxa_resfriamento=0.95, iter_max=10000,
                        adjacencias=None):
    # Calcula temperatura inicial baseada no custo médio de soluções aleatórias
    if temperatura_inicial is None:
        custos = [calcular_custo(gerar_solucao_inicial(pontos, num_veiculos), capacidade_maxima, adjacencias)
           for _ in range(100)]
        temperatura_inicial = 0.1 * sum(custos)/len(custos)
        
    solucao = gerar_solucao_inicial(pontos, num_veiculos)
    melhor_solucao = copy.deepcopy(solucao)
    melhor_custo = calcular_custo(solucao, capacidade_maxima, adjacencias)
    T = temperatura_inicial

    for _ in range(iter_max):
        vizinho = gerar_vizinho(solucao, adjacencias, capacidade_maxima)
        valido = all(
            rota_valida(rota, adjacencias) and 
            sum(p['carga'] for p in rota) <= capacidade_maxima
            for rota in vizinho
        )
        if not valido:
            continue 
        custo_vizinho = calcular_custo(vizinho, capacidade_maxima, adjacencias)
        delta = custo_vizinho - melhor_custo

        if delta < 0 or random.random() < math.exp(-delta / T):
            solucao = vizinho
            if custo_vizinho < melhor_custo:
                melhor_solucao = copy.deepcopy(vizinho)
                melhor_custo = custo_vizinho

        T *= taxa_resfriamento

    return melhor_solucao, melhor_custo

def gerar_solucao_inicial(pontos, num_veiculos):
    pontos = copy.deepcopy(pontos)
    random.shuffle(pontos)
    return [pontos[i::num_veiculos] for i in range(num_veiculos)]

def gerar_vizinho(solucao, adjacencias, capacidade_maxima):
    vizinho = [rota.copy() for rota in solucao]

    # escolhe uma rota aleatória que tenha pelo menos 2 pontos
    rotas_validas = [(i, rota) for i, rota in enumerate(vizinho)
        if sum(p['carga'] for p in rota) <= capacidade_maxima and len(rota) >= 2
    ]
    if not rotas_validas:
        return solucao
    i_rota = random.randrange(len(rotas_validas))
    rota = vizinho[i_rota]

    # tenta encontrar um par de índices consecutivos na rota que sejam vizinhos no grafo
    pares_consecutivos = [i for i in range(len(rota)-1)
                         if rota[i+1]['id'] in adjacencias.get(rota[i]['id'], {})]

    if not pares_consecutivos:
        return solucao  # não há pares consecutivos vizinhos para trocar

    # escolhe um par aleatório para trocar
    i = random.choice(pares_consecutivos)

    # troca os dois pontos na rota
    rota[i], rota[i+1] = rota[i+1], rota[i]

    # garante que a rota ainda é válida após a troca (se não for, retorna solução antiga)
    if not rota_valida(rota, adjacencias):
        return solucao  # rejeita vizinho inválido

    return vizinho
