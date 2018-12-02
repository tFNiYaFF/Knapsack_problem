import random


class Individual:
    def __init__(self):
        self.values = list()
        self.cost = int()
        self.selected = False


class Task2:

    POPULATION_SIZE = 200
    SELECTION_K = 0.2

    def load_data_and_set_limits(self):
        with open('12.txt') as f:
            self.max_weight, self.max_volume = [float(x) for x in next(f).split()]
            for line in f:
                self.data.append([float(x) for x in line.split()])

    def calculate_individual_cost(self, individual):
        weight, volume, price = 0, 0, 0
        for (selected, item) in zip(individual.values, self.data):
            if selected:
                weight += item[0]
                volume += item[1]
                price += item[2]
        if weight > self.max_weight or volume > self.max_volume:
            price = 0
        return price

    def create_individual(self):
        individual = Individual()
        for i in range(0, len(self.data)):
            value = random.randint(0, 1)
            individual.values.append(value)
        individual.cost = self.calculate_individual_cost(individual)
        return individual

    def create_population(self):
        for i in range(0, self.POPULATION_SIZE):
            self.population.append(self.create_individual())

    def get_best_not_selected_individual(self):
        maximum = 0
        best_individual = 0
        best_index = 0
        i = 0
        for individual in self.population:
            if individual.selected == False and individual.cost > maximum:
                best_individual = individual
                maximum = individual.cost
                best_index = i
            i += 1
        self.population[best_index].selected = True
        return best_individual

    def selection(self):
        number = int(len(self.population) * self.SELECTION_K)
        selected_population = list()
        for i in range(0, number):
            selected_population.append(self.get_best_not_selected_individual())
        return selected_population

    def crossover(self):
        selection = self.selection()
        return 0

    def __init__(self):
        self.data = list()
        self.population = list()
        self.max_weight = 0
        self.max_volume = 0
        self.load_data_and_set_limits()

    def run(self):
        self.create_population()
        self.crossover()
        return 0
