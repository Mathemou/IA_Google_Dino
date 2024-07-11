# Projeto de Algoritmo Genético para Treinamento de Redes Neurais

Este projeto implementa um algoritmo genético para treinar redes neurais representadas por indivíduos, com o objetivo de otimizar suas performances em um ambiente de simulação.

## Classe KeyNNClassifier
A classe KeyNNClassifier representa uma rede neural que é treinada utilizando o algoritmo genético. A rede neural possui a seguinte arquitetura:

- **Camada de Entrada:** 7 neurônios
- **Primeira Camada Oculta:** 64 neurônios
- **Segunda Camada Oculta:** 64 neurônios
- **Camada de Saída:** 3 neurônios


## Estrutura do Projeto

- **`initialize_population(size)`**: Inicializa a população com indivíduos contendo pesos e bias de redes neurais.
- **`fitness(individual, rounds=10)`**: Calcula a aptidão de um indivíduo através de múltiplas simulações.
- **`crossover(parent1, parent2)`**: Realiza o cruzamento de dois pais para gerar dois filhos.
- **`mutate(individual, rate)`**: Aplica mutações a um indivíduo com base em uma taxa de mutação.
- **`genetic_algorithm(population_size, generations, mutation_rate)`**: Implementa o algoritmo genético com elitismo e geração aleatória de novos indivíduos.

## Pré-requisitos

- Python 3.x
- NumPy

## Como Executar

1. Clone o repositório:

    ```sh
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Instale as dependências:

    ```sh
    pip install numpy
    ```

3. Execute o script principal:

    ```sh
    python DinoAINeural.py
    ```

## Estrutura de Dados

Cada indivíduo é representado como um dicionário contendo arrays NumPy para os pesos e bias da rede neural:

```python
individual = {
    'W1': np.random.randn(7, 64) * 0.01,
    'b1': np.zeros((1, 64)),
    'W2': np.random.randn(64, 64) * 0.01,
    'b2': np.zeros((1, 64)),
    'W3': np.random.randn(64, 3) * 0.01,
    'b3': np.zeros((1, 3))
}
