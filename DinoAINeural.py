import pygame
import os
import random
import time
from sys import exit
pygame.init()

global aiPlayer

# Valid values: HUMAN_MODE or AI_MODE
GAME_MODE = "AI_MODE"
RENDER_GAME = False

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
if RENDER_GAME:
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus4.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 90
    Y_POS = 330
    Y_POS_DUCK = 355
    JUMP_VEL = 17
    JUMP_GRAV = 1.1

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = 0
        self.jump_grav = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck and not self.dino_jump:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 20:
            self.step_index = 0

        if userInput == "K_UP" and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput == "K_DOWN" and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif userInput == "K_DOWN":
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = True
        elif not (self.dino_jump or userInput == "K_DOWN"):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_duck:
            self.jump_grav = self.JUMP_GRAV * 4
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel
            self.jump_vel -= self.jump_grav
        if self.dino_rect.y > self.Y_POS + 10:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            self.jump_grav = self.JUMP_GRAV
            self.dino_rect.y = self.Y_POS

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def getXY(self):
        return (self.dino_rect.x, self.dino_rect.y)


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle():
    def __init__(self, image, type):
        super().__init__()
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()

        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < - self.rect.width:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

    def getXY(self):
        return (self.rect.x, self.rect.y)

    def getHeight(self):
        return y_pos_bg - self.rect.y

    def getType(self):
        return (self.type)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 345


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)

        # High, middle or ground
        if random.randint(0, 3) == 0:
            self.rect.y = 345
        elif random.randint(0, 2) == 0:
            self.rect.y = 260
        else:
            self.rect.y = 300
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 19:
            self.index = 0
        SCREEN.blit(self.image[self.index // 10], self.rect)
        self.index += 1


class KeyClassifier:
    def __init__(self, state):
        pass

    def keySelector(self, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):
        pass

    def updateState(self, state):
        pass


def first(x):
    return x[0]

class KeyNNClassifier(KeyClassifier):
    def __init__(self, state):
        super().__init__(state)
        self.state = state
        self.model = self.build_model(state)

    def build_model(self, state):
        # Use o state para inicializar os pesos e bias diretamente
        model = {
            'W1': state['W1'],
            'b1': state['b1'],
            'W2': state['W2'],
            'b2': state['b2'],
            'W3': state['W3'],
            'b3': state['b3']
        }
        return model

    def relu(self, Z):
        return np.maximum(0, Z)

    def softmax(self, Z):
        expZ = np.exp(Z - np.max(Z))
        return expZ / expZ.sum(axis=1, keepdims=True)

    def forward_propagation(self, X):
        model = self.model

        model['Z1'] = np.dot(X, model['W1']) + model['b1']
        model['A1'] = self.relu(model['Z1'])
        model['Z2'] = np.dot(model['A1'], model['W2']) + model['b2']
        model['A2'] = self.relu(model['Z2'])
        model['Z3'] = np.dot(model['A2'], model['W3']) + model['b3']
        model['A3'] = self.softmax(model['Z3'])

        return model['A3']

    def train_model(self, X_train, y_train, epochs=10, learning_rate=0.01):
        m = X_train.shape[0]

        for epoch in range(epochs):
            A3 = self.forward_propagation(X_train)

            # One-hot encoding dos rótulos
            y_one_hot = np.eye(3)[y_train]

            # Backpropagation
            dZ3 = A3 - y_one_hot
            dW3 = np.dot(self.model['A2'].T, dZ3) / m
            db3 = np.sum(dZ3, axis=0, keepdims=True) / m

            dA2 = np.dot(dZ3, self.model['W3'].T)
            dZ2 = dA2 * (self.model['A2'] > 0)
            dW2 = np.dot(self.model['A1'].T, dZ2) / m
            db2 = np.sum(dZ2, axis=0, keepdims=True) / m

            dA1 = np.dot(dZ2, self.model['W2'].T)
            dZ1 = dA1 * (self.model['A1'] > 0)
            dW1 = np.dot(X_train.T, dZ1) / m
            db1 = np.sum(dZ1, axis=0, keepdims=True) / m

            # Atualização dos parâmetros
            self.model['W3'] -= learning_rate * dW3
            self.model['b3'] -= learning_rate * db3
            self.model['W2'] -= learning_rate * dW2
            self.model['b2'] -= learning_rate * db2
            self.model['W1'] -= learning_rate * dW1
            self.model['b1'] -= learning_rate * db1

    def keySelector(self, distance, obHeight, speed, obType, nextObDistance, nextObHeight, nextObType):
        obType_encoded = 1 if isinstance(obType, Bird) else 0
        nextObType_encoded = 1 if isinstance(nextObType, Bird) else 0
        input_data = np.array([[distance, obHeight, speed, obType_encoded, nextObDistance, nextObHeight, nextObType_encoded]])
        predictions = self.forward_propagation(input_data)
        action = np.argmax(predictions)

        if action == 0:
            return "K_NO"
        elif action == 1:
            return "K_UP"
        elif action == 2:
            return "K_DOWN"

    def updateState(self, state):
        self.state = state

class KeySimplestClassifier(KeyClassifier):
    def __init__(self, state):
        self.state = state

    def keySelector(self, distance, obHeight, speed, obType, nextObDistance, nextObHeight,nextObType):
        self.state = sorted(self.state, key=first)
        for s, d in self.state:
            if speed < s:
                limDist = d
                break
        if distance <= limDist:
            if isinstance(obType, Bird) and obHeight > 50:
                return "K_DOWN"
            else:
                return "K_UP"
        return "K_NO"

    def updateState(self, state):
        self.state = state


def playerKeySelector():
    userInputArray = pygame.key.get_pressed()

    if userInputArray[pygame.K_UP]:
        return "K_UP"
    elif userInputArray[pygame.K_DOWN]:
        return "K_DOWN"
    else:
        return "K_NO"


def playGame():
    global aiPlayer
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True

    clock = pygame.time.Clock()
    cloud = Cloud()
    font = pygame.font.Font('freesansbold.ttf', 20)

    player = Dinosaur()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 383
    points = 0

    obstacles = []
    death_count = 0
    spawn_dist = 0

    def score():
        global points, game_speed
        points += 0.25
        if points % 100 == 0:
            game_speed += 1

        if RENDER_GAME:
            text = font.render("Points: " + str(int(points)), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (1000, 40)
            SCREEN.blit(text, textRect)


    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

        if RENDER_GAME:
            SCREEN.fill((255, 255, 255))

        distance = 1500
        nextObDistance = 2000
        obHeight = 0
        nextObHeight = 0
        obType = 2
        nextObType = 2
        if len(obstacles) != 0:
            xy = obstacles[0].getXY()
            distance = xy[0]
            obHeight = obstacles[0].getHeight()
            obType = obstacles[0]

        if len(obstacles) == 2:
            nextxy = obstacles[1].getXY()
            nextObDistance = nextxy[0]
            nextObHeight = obstacles[1].getHeight()
            nextObType = obstacles[1]

        if GAME_MODE == "HUMAN_MODE":
            userInput = playerKeySelector()
        else:
            userInput = aiPlayer.keySelector(distance, obHeight, game_speed, obType, nextObDistance, nextObHeight,
                                             nextObType)

        if len(obstacles) == 0 or obstacles[-1].getXY()[0] < spawn_dist:
            spawn_dist = random.randint(0, 670)
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 5) == 5:
                obstacles.append(Bird(BIRD))

        player.update(userInput)

        if RENDER_GAME:
            player.draw(SCREEN)

        for obstacle in list(obstacles):
            obstacle.update()
            if RENDER_GAME:
                obstacle.draw(SCREEN)


        if RENDER_GAME:
            background()
            cloud.draw(SCREEN)

        cloud.update()

        score()

        if RENDER_GAME:
            clock.tick(60)
            pygame.display.update()

        for obstacle in obstacles:
            if player.dino_rect.colliderect(obstacle.rect):
                if RENDER_GAME:
                    pygame.time.delay(2000)
                death_count += 1
                return points



from scipy import stats
import numpy as np


def manyPlaysResults(rounds):
    # Parâmetros do algoritmo genético
    population_size = 200
    generations = 100
    mutation_rate = 0.03

    # Inicialização da população
    def initialize_population(size):
        population = []
        for _ in range(size):
            individual = {
            'W1': np.random.randn(7, 64) * 0.01,
            'b1': np.zeros((1, 64)),
            'W2': np.random.randn(64, 64) * 0.01,
            'b2': np.zeros((1, 64)),
            'W3': np.random.randn(64, 3) * 0.01,
            'b3': np.zeros((1, 3))
            }
            population.append(individual)
        return population

    # Função de aptidão
    def fitness(individual, rounds):
        global aiPlayer
        aiPlayer = KeyNNClassifier(individual)  # Define o aiPlayer como o indivíduo atual
        results = []
        for _ in range(rounds):
            results.append(playGame())  # Chama a função playGame para avaliar a aptidão do indivíduo
        npResults = np.asarray(results)
        return npResults.mean() - npResults.std()

    # Seleção dos indivíduos mais aptos
    def select(population, fitnesses):
        indices = np.argsort(fitnesses)
        # Seleciona os dois melhores indivíduos usando compreensão de lista
        return [population[i] for i in indices[-2:]]

    def crossover(parent1, parent2):
        child1, child2 = {}, {}
        
        # Realiza crossover para cada chave no dicionário
        for key in parent1.keys():
            # Gera um ponto de crossover aleatório dentro do intervalo do array
            crossover_point = np.random.randint(1, parent1[key].size)  # Usa o tamanho total do array
            # Achata os arrays para facilitar o crossover
            flat_parent1 = parent1[key].flatten()
            flat_parent2 = parent2[key].flatten()
            # Realiza o crossover
            flat_child1 = np.concatenate((flat_parent1[:crossover_point], flat_parent2[crossover_point:]))
            flat_child2 = np.concatenate((flat_parent2[:crossover_point], flat_parent1[crossover_point:]))
            # Reshape dos arrays para a forma original
            child1[key] = flat_child1.reshape(parent1[key].shape)
            child2[key] = flat_child2.reshape(parent2[key].shape)
        
        return child1, child2

    def mutate(individual, rate):
        mutated_individual = {}
        for key in individual.keys():
            mutated_array = individual[key].copy()  # Copia o array original para não alterar o original diretamente
            for idx, _ in np.ndenumerate(mutated_array):
                if np.random.rand() < rate:
                    mutated_array[idx] = np.random.randn() * 0.01  # Aplica uma mutação (pequena alteração aleatória)
            mutated_individual[key] = mutated_array
        return mutated_individual

    # Algoritmo Genético
    population = initialize_population(population_size)
    for generation in range(generations):
        fitnesses = np.array([fitness(individual, 3) for individual in population])
        new_population = []
        for _ in range(population_size // 2):
            parents = select(population, fitnesses)
            child1, child2 = crossover(parents[0], parents[1])
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = np.array(new_population)

    # Selecionar o melhor indivíduo da população final
    fitnesses = np.array([fitness(individual, 3) for individual in population])
    best_individual = population[np.argmax(fitnesses)]
    best_fitness = max(fitnesses)
    print(best_fitness)
    return best_individual, best_fitness



def main():
    global aiPlayer

    res, value = manyPlaysResults(1)


main()
