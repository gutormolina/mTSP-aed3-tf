import random
import math
import copy
from core.utils import calcular_custo, rota_valida

def simulated_annealing(pontos, num_veiculos, capacidade_maxima,
                        temperatura_inicial=None, taxa_resfriamento=0.95, iter_max=10000,
                        adjacencias=None, deposito=None):
    # Calcula temperatura inicial baseada no custo médio de soluções aleatórias
    if temperatura_inicial is None:
        custos = [calcular_custo(gerar_solucao_inicial_valida(pontos, num_veiculos, capacidade_maxima, deposito), capacidade_maxima, adjacencias)
           for _ in range(100)]
        temperatura_inicial = 0.1 * sum(custos)/len(custos)

    solucao = gerar_solucao_inicial_valida(pontos, num_veiculos, capacidade_maxima, deposito)
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

def gerar_solucao_inicial_valida(pontos, num_veiculos, capacidade_maxima, deposito=None):
    pontos = copy.deepcopy(pontos)
    if deposito:  # Remove o depósito da lista de pontos (se já estiver incluso)
        pontos = [p for p in pontos if p['id'] != deposito['id']]
    
    random.shuffle(pontos)
    rotas = []
    
    for _ in range(num_veiculos):
        rota = []
        if deposito:
            rota.append(deposito)  # Inicia no depósito
        rotas.append(rota)
    
    cargas = [0] * num_veiculos
    
    for p in pontos:
        colocado = False
        for i in range(num_veiculos):
            if cargas[i] + p['carga'] <= capacidade_maxima:
                rotas[i].append(p)
                cargas[i] += p['carga']
                colocado = True
                break
        
        if not colocado:
            idx_min = min(range(num_veiculos), key=lambda i: cargas[i])
            rotas[idx_min].append(p)
            cargas[idx_min] += p['carga']
    
    if deposito:  # Adiciona depósito no final de cada rota
        for rota in rotas:
            rota.append(deposito)
    
    return rotas


def gerar_vizinho(solucao, adjacencias, capacidade_maxima):
    vizinho = copy.deepcopy(solucao)

    n_rotas = len(vizinho)
    if n_rotas == 0:
        return solucao

    ops = ['2opt', 'swap', 'move']
    random.shuffle(ops)

    def carga_rota(rota):
        return sum(p['carga'] for p in rota)

    for op in ops:
        rotas_com_interior = [i for i, r in enumerate(vizinho) if len(r) >= 3]
        if op == '2opt':
            if not rotas_com_interior:
                continue
            idx_rota = random.choice(rotas_com_interior)
            rota = vizinho[idx_rota]

            if len(rota) - 2 < 2:
                continue  # não há subsequência suficiente para 2-opt
            i = random.randint(1, len(rota) - 3)
            j = random.randint(i + 1, len(rota) - 2)

            # aplica 2-opt 
            rota[i:j+1] = list(reversed(rota[i:j+1]))

            # valida rota
            if rota_valida(rota, adjacencias) and carga_rota(rota) <= capacidade_maxima:
                return vizinho
            else:
                # desfazer alteração para tentar outra operação
                vizinho = copy.deepcopy(solucao)
                continue

        elif op == 'swap':
            if len(rotas_com_interior) < 2:
                continue
            r1, r2 = random.sample(rotas_com_interior, 2)
            rota1, rota2 = vizinho[r1], vizinho[r2]

            # índices interiores
            i = random.randint(1, len(rota1) - 2)
            j = random.randint(1, len(rota2) - 2)

            # swap
            rota1[i], rota2[j] = rota2[j], rota1[i]

            # valida ambas as rotas (capacidade e adjacências)
            if (rota_valida(rota1, adjacencias) and rota_valida(rota2, adjacencias)
                and carga_rota(rota1) <= capacidade_maxima and carga_rota(rota2) <= capacidade_maxima):
                return vizinho
            else:
                vizinho = copy.deepcopy(solucao)
                continue

        elif op == 'move':
            if not rotas_com_interior or len(rotas_com_interior) < 1:
                continue
            # escolha de rota origem com interior
            r_from = random.choice(rotas_com_interior)
            # escolha de rota destino
            possible_dest = [i for i in range(n_rotas) if i != r_from]
            if not possible_dest:
                continue
            r_to = random.choice(possible_dest)

            rota_from, rota_to = vizinho[r_from], vizinho[r_to]
            if len(rota_from) < 3:
                continue

            # escolhe índice interior na origem e posição de inserção na destino
            idx_from = random.randint(1, len(rota_from) - 2)
            insert_pos = random.randint(1, len(rota_to) - 1)

            ponto = rota_from.pop(idx_from)
            rota_to.insert(insert_pos, ponto)

            # valida ambas as rotas
            if (rota_valida(rota_from, adjacencias) and rota_valida(rota_to, adjacencias)
                and carga_rota(rota_from) <= capacidade_maxima and carga_rota(rota_to) <= capacidade_maxima):
                # sucesso
                return vizinho
            else:
                # desfazer (reconstruir da solução original)
                vizinho = copy.deepcopy(solucao)
                continue

    return solucao
