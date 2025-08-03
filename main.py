from core.grafo import carregar_pontos, plotar_pontos, carregar_adjacencias
from algoritmos.simulated_annealing import simulated_annealing
from core.utils import calcular_distancia_total
import os

caso_nome = "caso_01"
entrada_path = f"data/{caso_nome}.csv"
saida_dir = f"output/{caso_nome}"
os.makedirs(saida_dir, exist_ok=True)

pontos = carregar_pontos(entrada_path)

# parâmetros
num_veiculos = 2
capacidade_maxima = 5
pontos = carregar_pontos(entrada_path)
adjacencias = carregar_adjacencias(f"data/{caso_nome}_adjacencia.csv", pontos)

melhor_solucao, custo = simulated_annealing(
    pontos, num_veiculos, capacidade_maxima,
    temperatura_inicial=1000, taxa_resfriamento=0.995, iter_max=5000,
    adjacencias=adjacencias
)

print(f"Custo total das rotas: {custo:.2f}")

for i, rota in enumerate(melhor_solucao):
    distancia = calcular_distancia_total(rota)
    carga = sum(p['carga'] for p in rota)
    print(f"  Caminhão {i+1}: {len(rota)} pontos | Distância = {distancia:.2f} | Carga = {carga}")

# plotar as rotas geradas
plotar_pontos(pontos, melhor_solucao, adjacencias=adjacencias, salvar_em=saida_dir)

with open(os.path.join(saida_dir, "resumo.txt"), "w") as f:
    f.write(f"Custo total das rotas: {custo:.2f}\n")
    for i, rota in enumerate(melhor_solucao):
        distancia = calcular_distancia_total(rota)
        carga = sum(p['carga'] for p in rota)
        f.write(f"  Caminhão {i+1}: {len(rota)} pontos | Distância = {distancia:.2f} | Carga = {carga}\n")
