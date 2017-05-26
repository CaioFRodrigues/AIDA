from time import time
from numpy import random
from copy import copy
from operator import attrgetter
from controller1.racer import Racer

class Evolution:
    def __init__(self, population_size, n_thetas, seed=None):
        self.__population_size = 2
        self.__n_thetas = 0
        self.__seed = 0
        self.__population = []
        self.__percentage_mutation = 0.01
        self.__percentage_elitism = 0.10
        self.__percentage_roulette = 0.10
        self.__percentage_children = 1.0 - (self.__percentage_elitism + self.__percentage_roulette)

        if population_size <= n_thetas:
            raise ValueError("population_size must be larger than n_thetas")

        # TODO: check if min and max population sizes are appropriate
        if population_size < 2 or population_size > 100:
            raise ValueError("population_size must be between 2 and 100")

        if n_thetas <= 0:
            raise ValueError("n_thetas must be greater than 0")

        self.__population_size = population_size
        self.__n_thetas = n_thetas
        if (seed is not None):
            self.__seed = seed
        else:
            self.__seed = int(time())
        random.seed(self.__seed)

    @property
    def seed(self):
        return self.__seed

    def random_theta(self, n=None):
        # TODO: check if [-1, 1] is an appropriate range for the thetas
        return random.uniform(-1.0, 1.0, size=n)

    def random_racer(self):
        random_thetas = self.random_theta(n=self.__n_thetas)
        return Racer(thetas=random_thetas)

    def random_population(self, controller):
        population = [self.random_racer() for _ in range(0, self.__population_size)]

        for p in population:
            p.calculate_fitness(controller)

        population.sort(key=attrgetter('fitness'), reverse=True)

        return population

    def evolve(self, controller):
        print("seed:", self.seed)

        self.__population = list(self.random_population(controller))

        gen = 0
        while True:
            gen += 1

            best_fitness = self.__population[0].fitness

            self.__population = self.next_generation(controller)
            new_best_fitness = self.__population[0].fitness

            print('Current best at gen %d: %f' % (gen, new_best_fitness))

            delta_fitness = (new_best_fitness - best_fitness) / best_fitness

            # TODO: check if these parameters are appropriate for termination
            if gen > 1000 and delta_fitness < 0.005:
                break

        return self.__population[0]

    def next_generation(self, controller):
        cur_population = copy(self.__population)

        elite_population, cur_population = self.select_elitism(cur_population)
        roulette_population, cur_population = self.select_roulette(cur_population)
        adult_population = elite_population + roulette_population

        children_population = self.select_children(adult_population)
        for c in children_population:
            c.calculate_fitness(controller)

        new_population = adult_population + children_population
        new_population.sort(key=attrgetter('fitness'), reverse=True)

        return new_population

    def select_elitism(self, population):
        elite_slots = int(len(population) * self.__percentage_elitism)

        return population[:elite_slots], population[elite_slots:]

    def select_roulette(self, population):
        roulette_slots = int(len(population) * self.__percentage_roulette)

        sum_fitnesses = sum(p.fitness for p in population)

        roulette_selected = []
        for _ in range(0, roulette_slots):
            r = random.uniform(0, sum_fitnesses)
            t = 0
            for i,p in enumerate(population):
                t += p.fitness

                if t >= r:
                    roulette_selected.append(population.pop(i))
                    break

        return roulette_selected, population

    def select_children(self, population):
        children_slots = int(self.__population_size * self.__percentage_children)

        children = []
        for _ in range(0, children_slots):
            # TODO: stop selecting random parents to breed?
            r1, r2 = random.choice(population, 2)
            c1, c2 = self.breed(r1, r2)
            children.extend([c1, c2])

        return children

    def breed(self, r1: Racer, r2: Racer):
        child1 = self.crossover(r1, r2)
        child2 = self.crossover(r1, r2)

        if random.ranf() < self.__percentage_mutation:
            child1 = self.mutate(child1)
        if random.ranf() < self.__percentage_mutation:
            child2 = self.mutate(child2)

        return child1, child2

    def crossover(self, r1: Racer, r2: Racer) -> Racer:
        selected_thetas = [random.choice(thetas) for thetas in zip(r1.thetas, r2.thetas)]
        return Racer(thetas=selected_thetas)

    def mutate(self, racer: Racer) -> Racer:
        new_thetas = racer.thetas
        theta_idx = random.random_integers(0, self.__n_thetas - 1)
        new_thetas[theta_idx] = self.random_theta()
        racer.thetas = new_thetas
        return racer
