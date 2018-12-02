import random


class Individual:
    def __init__(self):

        # Вектор значений для каждой вещи есть/нет
        self.values = list()

        # Суммарная стоимость (функция приспособленности)
        self.cost = int()

        # Для отбора в 20% перед скрещиванием. Не самая лучшая реализация.
        self.selected = False

        # Перед созданием потомков ставим всем существующим особям флаг, что они старые.
        self.old = False


class Task2:

    POPULATION_SIZE = 200
    GENERATIONS_NUMBER = 500

    # Вероятности соответствующих событий
    SELECTION_K = 0.2
    MUTATE_K = 0.1
    SELECTION_DELTA = 0.1

    def clean_selected_in_population(self):
        for individual in self.population:
            individual.selected = False

    def set_old_individuals_to_old(self):
        for individual in self.population:
            individual.old = True

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
        """Создание каждого индивида в популяции рандомом."""

        individual = Individual()
        for i in range(0, len(self.data)):
            value = random.randint(0, 1)
            individual.values.append(value)
        individual.cost = self.calculate_individual_cost(individual)
        return individual

    def create_population(self):
        """Создание начальной популяции. Рандомом."""

        for i in range(0, self.POPULATION_SIZE):
            self.population.append(self.create_individual())

    def get_best_not_selected_individual(self):
        """Выбираем лучший из еще не выбранных 20% для скрещивания. Возможно стоило просто отсортировать, как в конце"""

        maximum = -1
        best_individual = 0
        best_index = 0
        i = 0
        for individual in self.population:
            if individual.selected is False and individual.cost > maximum:
                best_individual = individual
                maximum = individual.cost
                best_index = i
            i += 1
        self.population[best_index].selected = True
        return best_individual

    def selection(self):
        """Отбор особей для скрещивания. Выбираем только 20% самых лучших."""

        number = int(len(self.population) * self.SELECTION_K)
        selected_population = list()
        for i in range(0, number):
            selected_population.append(self.get_best_not_selected_individual())
        self.clean_selected_in_population()
        return selected_population

    def make_children(self, parent1, parent2):
        """Делаем результат скрещивания."""

        child1 = Individual()
        child2 = Individual()
        for index, (value1, value2) in enumerate(zip(parent1.values, parent2.values)):
            rnd = random.random()
            if rnd >= 0.5:
                child1.values.insert(index, value1)
                child2.values.insert(index, value2)
            else:
                child1.values.insert(index, value2)
                child2.values.insert(index, value1)
        child1.cost = self.calculate_individual_cost(child1)
        child2.cost = self.calculate_individual_cost(child2)
        return child1, child2

    def crossover(self):
        """Скрещивание. Однородное (каждый бит от случайного родителя)"""

        selection = self.selection()
        next_generation = list()
        self.set_old_individuals_to_old()
        for index in range(0, len(selection) - 1, 2):
            parent1 = selection[index]
            parent2 = selection[index + 1]
            children = self.make_children(parent1, parent2)
            next_generation.append(children[0])
            next_generation.append(children[1])
        self.population.extend(next_generation)

    def mutate(self):
        """Мутация. Добавление 1 случайной вещи 10% индивидов. Если вещь установлена, то она такой и будет."""
        number = int(self.MUTATE_K * len(self.population))
        for i in range(0, number):
            population_index = random.randint(0, len(self.population) - 1)
            bit_index = random.randint(0, len(self.population[0].values) - 1)

            # будем считать, что неважно, установлена ли эта вещь или нет.
            self.population[population_index].values[bit_index] = 1

    def select_new_generation(self):
        """Формирование новой популяции, штраф за старость -20%. Выбор лучших POPULATION_SIZE индивидов."""

        for individual in self.population:
            if individual.old is True:
                individual.cost *= 0.8
        self.population.sort(key=lambda x: x.cost, reverse=True)
        self.population = self.population[0:self.POPULATION_SIZE]

    def create_result(self, result):
        items = []
        for i in range(0, len(result.values)):
            if result.values[i] == 1:
                items.append(i+1)
        real_volume = 0
        real_weight = 0
        real_price = 0
        for i in range(0, len(items)):
            real_volume += self.data[items[i] - 1][1]
            real_weight += self.data[items[i] - 1][0]
            real_price += self.data[items[i] - 1][2]
        j = dict(value=real_price, weight=real_weight, volume=real_volume, items=items)
        return j

    def __init__(self):
        self.data = list()
        self.population = list()
        self.max_weight = 0
        self.max_volume = 0
        self.load_data_and_set_limits()

    def run(self):
        prev_best = 0
        for i in range(0, self.GENERATIONS_NUMBER):
            self.create_population()
            self.crossover()
            self.mutate()
            self.select_new_generation()
            if prev_best == 0:
                prev_best = self.calculate_individual_cost(self.population[0])
            else:
                delta = self.calculate_individual_cost(self.population[0]) / prev_best - 1
                if delta < self.SELECTION_DELTA:
                    break
                else:
                    prev_best = self.calculate_individual_cost(self.population[0])
        return self.create_result(self.population[0])



