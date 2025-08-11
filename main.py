from core.grafo import carregar_pontos, plotar_pontos, carregar_adjacencias, somar_cargas, reconstruir_caminho
from algoritmos.simulated_annealing import simulated_annealing
from algoritmos.clarke_wright import clarke_wright
from core.utils import calcular_distancia_total
import os
import time
import argparse
import math

def main():
    parser = argparse.ArgumentParser(description='Otimizador de Rotas de Coleta')
    parser.add_argument('caso', help='Nome do caso (ex: caso_01)')
    parser.add_argument('-a', '--algoritmo', choices=['sa', 'cw', 'fb'], 
                       help='Algoritmo: sa (Simulated Annealing), cw (Clarke-Wright)')
    args = parser.parse_args()
  
    caso_nome = args.caso
    entrada_path = f"data/{caso_nome}.csv"
    adjacencia_path = f"data/{caso_nome}_adjacencia.csv"
    saida_dir = f"output/{caso_nome}"
    os.makedirs(saida_dir, exist_ok=True)

    pontos = carregar_pontos(entrada_path)
    adjacencias = carregar_adjacencias(adjacencia_path, pontos)
    total_carga = somar_cargas(pontos)

    # parâmetros
    capacidade_maxima = 5
    num_veiculos = math.ceil(total_carga / capacidade_maxima)
    
    start_time = time.time()

    print(f"\nOtimizando rotas para {len(pontos)} pontos com {num_veiculos} veículos...")
    print(f"Algoritmo selecionado: {'Simulated Annealing' if args.algoritmo == 'sa' else 'Clarke-Wright'}")

    deposito = next((p for p in pontos if p['id'] == 0), None)
    if not deposito:
        raise ValueError("Arquivo CSV não contém um depósito (ponto com id=0)")
    
    if args.algoritmo == 'sa':
        solucao, custo = simulated_annealing(
            pontos, num_veiculos, capacidade_maxima,
            temperatura_inicial=1000, taxa_resfriamento=0.95, iter_max=10000,
            adjacencias=adjacencias, deposito=deposito
        )
    elif args.algoritmo == 'cw':
        solucao, custo = clarke_wright(pontos, num_veiculos, capacidade_maxima, adjacencias)
   
            
    print(f"Custo total das rotas: {custo:.2f}")

    for i, rota in enumerate(solucao):
        distancia = calcular_distancia_total(rota)
        carga = sum(p['carga'] for p in rota)
        print(f"  Caminhão {i+1}: {len(rota)} pontos | Distância = {distancia:.2f} | Carga = {carga}/{capacidade_maxima}")
    
    print(f"\nTempo de execução: {time.time()-start_time:.2f} segundos")
    
    # plotar as rotas geradas
    plotar_pontos(pontos, solucao, adjacencias=adjacencias, salvar_em=saida_dir)

    with open(os.path.join(saida_dir, "resumo.txt"), "w") as f:
        f.write(f"Custo total das rotas: {custo:.2f}\n")
        f.write(f"Número de veículos: {len(solucao)}\n")
        f.write(f"Capacidade máxima por veículo: {capacidade_maxima}\n\n")

        for i, rota in enumerate(solucao):
            carga_acumulada = 0
            f.write(f"=== Caminhão {i+1} ===\n")
            f.write(f"Pontos visitados: {len(rota)}\n")
            f.write(f"Distância total: {calcular_distancia_total(rota):.2f}\n")
            f.write("Trajeto:\n")

            for j, ponto in enumerate(rota):
                carga_acumulada += ponto['carga']
                f.write(f"  Ponto {ponto['id']} (Carga: {ponto['carga']} | Acumulado: {carga_acumulada}/{capacidade_maxima})\n")

            f.write("\n")

if __name__ == "__main__":
	main()
