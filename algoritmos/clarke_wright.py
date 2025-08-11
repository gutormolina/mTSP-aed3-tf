import copy
import math
from core.utils import calcular_custo, rota_valida

def clarke_wright(pontos, num_veiculos, capacidade_maxima, adjacencias, deposito):
    # inicializa rotas onde cada ponto tem uma rota com depósito no começo e no fim
    rotas = [[deposito, ponto, deposito] for ponto in pontos if ponto['id'] != deposito['id']]

    def dist(p1, p2):
        return calcular_distancia(p1, p2)

    savings = []
    pontos_coleta = [p for p in pontos if p['id'] != deposito['id']]

    for i in range(len(pontos_coleta)):
        for j in range(i + 1, len(pontos_coleta)):
            a = pontos_coleta[i]
            b = pontos_coleta[j]
            if a['id'] in adjacencias and b['id'] in adjacencias[a['id']]:
                saving = dist(deposito, a) + dist(deposito, b) - dist(a, b)
                savings.append((saving, a, b))

    # ordena savings em ordem decrescente
    savings.sort(key=lambda x: x[0], reverse=True)

    # achar rota que contém um ponto e se esse ponto é nas extremidades
    def encontrar_rota_e_pos(rotas, ponto):
        for r in rotas:
            if ponto in r:
                if r[1] == ponto:
                    return r, 'inicio'
                elif r[-2] == ponto:
                    return r, 'fim'
        return None, None

    for saving, a, b in savings:
        rota_a, pos_a = encontrar_rota_e_pos(rotas, a)
        rota_b, pos_b = encontrar_rota_e_pos(rotas, b)

        if not rota_a or not rota_b or rota_a == rota_b:
            continue

        if (pos_a == 'fim' and pos_b == 'inicio'):
            nova_rota = rota_a[:-1] + rota_b[1:]
        elif (pos_a == 'inicio' and pos_b == 'fim'):
            nova_rota = rota_b[:-1] + rota_a[1:]
        else:
            continue

        carga = sum(p['carga'] for p in nova_rota if p['id'] != deposito['id'])
        if carga > capacidade_maxima:
            continue

        if not rota_valida(nova_rota, adjacencias):
            continue

        rotas.remove(rota_a)
        rotas.remove(rota_b)
        rotas.append(nova_rota)

        if len(rotas) <= num_veiculos:
            break

    while len(rotas) > num_veiculos:
        rotas.sort(key=lambda r: sum(p['carga'] for p in r if p['id'] != deposito['id']))
        r1 = rotas.pop(0)
        r2 = rotas.pop(0)
        nova_rota = r1[:-1] + r2[1:]
        if sum(p['carga'] for p in nova_rota if p['id'] != deposito['id']) <= capacidade_maxima and rota_valida(nova_rota, adjacencias):
            rotas.append(nova_rota)
        else:
            rotas.append(r1)
            rotas.append(r2)
            break

    custo = calcular_custo(rotas, capacidade_maxima, adjacencias)
    return rotas, custo

def calcular_distancia(p1, p2):
    dx = p2['x'] - p1['x']
    dy = p2['y'] - p1['y']
    return math.sqrt(dx*dx + dy*dy)