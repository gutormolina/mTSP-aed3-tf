import itertools
import copy
import math
from tqdm import tqdm
from core.utils import calcular_custo, rota_valida

def brute_force(pontos, num_veiculos, capacidade_maxima, adjacencias, deposito):
    pontos_coleta = [p for p in pontos if p['id'] != deposito['id']]
    n = len(pontos_coleta)

    melhor_solucao = None
    melhor_custo = float('inf')

    total_perms = math.factorial(n)
    pbar = tqdm(itertools.permutations(pontos_coleta), total=total_perms, desc="Testando soluções")

    for perm in pbar:
        # gera todas as combinações possíveis de cortes
        # print(f"Permutação: {[p['id'] for p in perm]}")
        for cortes in gerar_cortes(n, num_veiculos):
            # print(f"Cortes: {cortes}")
            rotas = []
            start = 0
            valido = True

            if len(cortes) == 0:
                rota = [deposito] + list(perm) + [deposito]
                if sum(p['carga'] for p in perm) > capacidade_maxima:
                    valido = False
                else:
                    rotas.append(rota)
            else:
                # print(f" Rotas geradas para cortes {cortes}:")
                for end in cortes:
                    subrota = list(perm[start:end])
                    # print(f"  Subrota: {[p['id'] for p in subrota]}")
                    carga_subrota = sum(p['carga'] for p in subrota)
                    if carga_subrota > capacidade_maxima:
                        # print(f"   Capacidade excedida na subrota {[p['id'] for p in subrota]} com carga {carga_subrota}")
                        valido = False
                        break
                    rota = [deposito] + subrota + [deposito]
                    rotas.append(rota)
                    start = end
                    

                    if not rota_valida(rota, adjacencias):
                        valido = False
                        break

                if valido:
                    subrota = list(perm[start:n])
                    # print(f"  Última subrota: {[p['id'] for p in subrota]}")
                    carga_subrota = sum(p['carga'] for p in subrota)
                    if carga_subrota > capacidade_maxima:
                        # print(f"   Capacidade excedida na última subrota {[p['id'] for p in subrota]} com carga {carga_subrota}")
                        valido = False
                    else:
                        rota = [deposito] + subrota + [deposito]
                        rotas.append(rota)

            if not valido:
                continue

            custo_total = calcular_custo(rotas, capacidade_maxima, adjacencias)
            if custo_total < melhor_custo:
                melhor_custo = custo_total
                melhor_solucao = copy.deepcopy(rotas)
                # print(f"Nova melhor solução com custo {melhor_custo}:")
                for i, r in enumerate(melhor_solucao):
                    # print(f"  Rota {i+1}: {[p['id'] for p in r]}")
                    pass

    return melhor_solucao, melhor_custo


def gerar_cortes(n, k):
    if k == 1:
        return[()]
    else:
        return itertools.combinations(range(1, n), k - 1)