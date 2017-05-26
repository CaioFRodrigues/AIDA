from time import time
from numpy import random
from copy import copy
from functools import reduce
from operator import attrgetter
from controller1.racer import Racer

class Evolution:
    def __init__(self, population_size, n_thetas):
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
        self.__seed = int(time())
        random.seed(self.__seed)

    @property
    def seed(self):
        return self.__seed

    def random_theta(self, n=None):
        # TODO: check if [-100, 100] is an appropriate range for the thetas
        return random.uniform(-100.0, 100.0, size=self.__n_thetas)

    def random_racer(self):
        random_thetas = self.random_theta(n=self.__n_thetas)
        return Racer(thetas=random_thetas)

    def random_population(self, controller):
        r = self.random_racer()
        t1 = time()
        r.calculate_fitness(controller)
        t2 = time()
        print('%0.3f ms' % ((t2-t1)*1000.0))
        return
        population = [self.random_racer() for _ in range(0, self.__population_size)]
        [p.calculate_fitness(controller) for p in population]
        population.sort(key=attrgetter('fitness'), reverse=True)
        return population

    def evolve(self, controller):
        self.__population = list(self.random_population(controller))
        return
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
        [c.calculate_fitness(controller) for c in children_population]

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
        selected_thetas = []
        for i in range(0, self.__n_thetas):
            if random.ranf() < 0.50: # 50% chance
                selected_theta = r1.theta[i]
            else:
                selected_theta = r2.theta[i]

            ''' this could be used as a third kind of crossover: mixing both parents '''
#            chance = random.ranf()
#            if chance < 0.50: # 50% chance
#                selected_theta = r1.theta[i]
#            else:# if chance < 0.95: # another 47.5% chance
#                selected_theta = r2.theta[i]
#            else: # 5% chance
#                selected_theta = (r1.theta[i] + r2.theta[i]) / 2

            selected_thetas.append(selected_theta)

        return Racer(thetas=selected_thetas)

    def mutate(self, racer: Racer) -> Racer:
        theta_idx = random.random_integers(0, self.__n_thetas - 1)
        new_thetas = racer.thetas
        new_thetas[theta_idx] = self.random_theta()
        racer.thetas(new_thetas)
        return racer
