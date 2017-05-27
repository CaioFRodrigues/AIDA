from time import time
from numpy import random
from copy import copy
from operator import attrgetter
from controller1.racer import Racer

class Evolution:
    def __init__(self, max_population_size, n_thetas, seed=None, adam_genes=None):
        if max_population_size <= n_thetas:
            raise ValueError("max_population_size must be larger than n_thetas")

        # TODO: check if min and max population sizes are appropriate
        if max_population_size < 2 or max_population_size > 100:
            raise ValueError("max_population_size must be between 2 and 100")

        if n_thetas <= 0:
            raise ValueError("n_thetas must be greater than 0")

        self.__max_population_size = max_population_size
        self.__n_thetas = n_thetas
        self.__seed = seed
        self.__population = []
        self.__percentage_mutation = 0.01
        self.__percentage_elitism = 0.10
        self.__elite_slots = int(self.__max_population_size * self.__percentage_elitism)
        self.__children_slots = self.__max_population_size - self.__elite_slots
        self.__breedings_per_gen = int(self.__children_slots / 2)

        if adam_genes is not None:
            self.__population = [Racer(adam_genes)]

        if self.__seed is None:
            self.__seed = int(time())
        random.seed(self.__seed)

    @property
    def seed(self):
        return self.__seed

    def evolve(self, generations, controller):
        print("Random seed:", self.seed)

        self.produce_random_population(controller)

        gen = 0
        prev_best_fitness = float("-inf")
        while True:
            gen += 1

            best_fitness = self.__population[0].fitness
            print('Current best at gen %d: %f' % (gen, best_fitness))
            if best_fitness > prev_best_fitness:
                print('Current best thetas:', self.__population[0].thetas)

            new_population = self.select_elitism()
            new_population += self.produce_children(controller)
            new_population.sort(key=attrgetter('fitness'), reverse=True)

            self.__population = new_population
            prev_best_fitness = best_fitness

            if gen >= generations:
                break

        return self.__population[0]

    def produce_random_population(self, controller):
        n_random_individuals = self.__max_population_size - len(self.__population)
        random_population = [self.random_racer() for _ in range(0, n_random_individuals)]
        self.__population += random_population

        for p in self.__population:
            p.calculate_fitness(controller)

        self.__population.sort(key=attrgetter('fitness'), reverse=True)

    def random_racer(self):
        random_thetas = self.random_theta(n=self.__n_thetas)
        return Racer(random_thetas)

    def random_theta(self, n=None):
        # TODO: check if [-1, 1] is an appropriate range for the thetas
        return random.uniform(-1.0, 1.0, size=n)

    def select_elitism(self):
        return self.__population[:self.__elite_slots]

    def produce_children(self, controller):
        min_fitness = self.__population[-1].fitness

        for p in self.__population:
            p.calculate_adjusted_fitness(min_fitness)

        roulette_max = sum(p.adjusted_fitness for p in self.__population)

        children_population = []
        for _ in range(0, self.__breedings_per_gen):
            r1 = self.select_roulette(roulette_max)
            r2 = self.select_roulette(roulette_max)
            c1 = self.breed(r1, r2)
            c2 = self.breed(r1, r2)
            children_population += [c1, c2]

        for c in children_population:
            c.calculate_fitness(controller)

        return children_population

    def select_roulette(self, roulette_max) -> Racer:
        roll = random.uniform(0, roulette_max)
        for i,p in enumerate(self.__population):
            roll -= p.adjusted_fitness
            if roll <= 0:
                return self.__population[i]

    def breed(self, r1: Racer, r2: Racer) -> Racer:
        child = self.crossover(r1, r2)
        self.mutate(child)
        return child

    def crossover(self, r1: Racer, r2: Racer) -> Racer:
        selected_thetas = [random.choice(theta_options) for theta_options in zip(r1.thetas, r2.thetas)]
        return Racer(selected_thetas)

    def mutate(self, racer: Racer):
        for i in range(0, self.__n_thetas):
            if random.ranf() < self.__percentage_mutation:
                racer.thetas[i] = self.random_theta()
