import random
import numpy as np
from NeuralNetwork import NeuralNetwork

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [NeuralNetwork() for _ in range(population_size)]

    def evaluate_population(self, fitness_scores):
        scores = []
        for net, fitness in zip(self.population, fitness_scores):
            scores.append((net, fitness))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:self.population_size // 2]

    def crossover(self, parent1, parent2):
        child = NeuralNetwork()
        for i in range(len(child.weights_input_hidden)):
            if random.random() > 0.5:
                child.weights_input_hidden[i] = parent1.weights_input_hidden[i]
            else:
                child.weights_input_hidden[i] = parent2.weights_input_hidden[i]
        for i in range(len(child.weights_hidden_output)):
            if random.random() > 0.5:
                child.weights_hidden_output[i] = parent1.weights_hidden_output[i]
            else:
                child.weights_hidden_output[i] = parent2.weights_hidden_output[i]
        return child

    def mutate(self, child):
        for i in range(len(child.weights_input_hidden)):
            if random.random() < self.mutation_rate:
                child.weights_input_hidden[i] += np.random.randn() * 0.1
        for i in range(len(child.weights_hidden_output)):
            if random.random() < self.mutation_rate:
                child.weights_hidden_output[i] += np.random.randn() * 0.1

    def create_new_generation(self, parents):
        new_population = []
        for _ in range(self.population_size // 2):
            parent1, parent2 = random.sample(parents, 2)
            child = self.crossover(parent1[0], parent2[0])
            self.mutate(child)
            new_population.append(child)
        self.population = new_population + [p[0] for p in parents]
