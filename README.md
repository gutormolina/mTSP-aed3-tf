# Otimização de Rotas de Coleta de Lixo com Simulated Annealing (mTSP)

Este projeto é o trabalho final da disciplina **Algoritmos e Estruturas de Dados III**, e tem como objetivo resolver uma variação do problema do caixeiro viajante com múltiplos veículos (mTSP), aplicada ao cenário de **coleta de lixo** em uma cidade.

A solução utiliza o algoritmo **Simulated Annealing** para encontrar rotas otimizadas, respeitando restrições como:
- Capacidade máxima de carga dos caminhões.
- Conectividade real entre pontos (restrição de vizinhança via grafo).
- Custo baseado na distância percorrida em ruas reais.

---

## 📁 Estrutura do Projeto

```
mTSP-aed3-tf/
├── algoritmos/
│   └── simulated_annealing.py     # Algoritmo principal
├── core/
│   ├── grafo.py                   # Funções de grafo e visualização
│   ├── utils.py                   # Funções auxiliares (distância, custo, etc.)
├── data/
│   ├── caso.csv                   # Pontos de coleta
│   └── caso_adjacencia.csv        # Conexões (arestas) entre os pontos
├── output/
│   └── caso/                      # Resultados gerados (imagens e resumo)
├── main.py                        # Script principal de execução
└── requirements.txt               # Dependências
```

---

## 🚀 Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/mTSP-aed3-tf.git
cd mTSP-aed3-tf
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o projeto:

```bash
python main.py
```

5. Os resultados (rotas e resumo) serão gerados na pasta `output`.

---

## ⚙️ Parâmetros

Os principais parâmetros do algoritmo podem ser ajustados diretamente no `main.py`:

```python
num_veiculos = 2
capacidade_maxima = 5
temperatura_inicial = 1000
taxa_resfriamento = 0.995
iter_max = 5000
```

---

## 🛠️ Tecnologias Utilizadas

- Python 3.12+
- Pandas
- Matplotlib
- Algoritmo probabilístico Simulated Annealing
- Estrutura de grafos com Dijkstra para rotas reais

---

## ✍️ Autores

- Augusto Molina  
- Eduarda Louzada

Projeto desenvolvido como trabalho prático da disciplina **Algoritmos e Estruturas de Dados III** — 2025/2  
Universidade Federal de Pelotas (UFPel)