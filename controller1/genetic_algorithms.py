import time
import random
import numpy
from operator import attrgetter
from controller1.racer import Racer

class Evolution:
    def __init__(self, population_size, n_thetas):
        self.__population_size = 2
        self.__n_thetas = 0
        self.__seed = 0
        self.__population = []

        if population_size <= n_thetas:
            raise ValueError("population_size must be larger than n_thetas")

        # TODO: check if min and max population sizes are appropriate
        if population_size < 2 or population_size > 100:
            raise ValueError("population_size must be between 2 and 100")

        if n_thetas <= 0:
            raise ValueError("n_thetas must be greater than 0")

        self.__population_size = population_size
        self.__n_thetas = n_thetas
        self.__seed = time.time()
        random.seed(self.__seed)

    @property
    def seed(self):
        return self.__seed

    def colonize(self):
        for _ in range(0, self.__n_thetas):
            random_thetas = numpy.random.ranf(size=self.__n_thetas)
            # TODO: check if [0, 100) is an appropriate range for the thetas
            map((lambda x: 100*x), random_thetas)
            self.__population.append(Racer(theta=random_thetas))

    def evolve(self, controller):
        if self.__population == []:
            self.colonize()

        # This is a placeholder
        # TODO: code this

        for candidate in self.__population:
            candidate.calculate_fitness(controller)

        fittest = max(self.__population, key=attrgetter('fitness'))

        return fittest

    def breed(self, r1: Racer, r2: Racer):
        child1 = mutate(crossover(r1, r2))
        child2 = mutate(crossover(r1, r2))
        return child1, child2

    def crossover(self, r1: Racer, r2: Racer) -> Racer:
        new_thetas = []
        for i in range(0, self.__nthetas):
            if random.randint(0, 1) == 0: # 50% chance
                new_thetas.append(r1.theta[i])
            else:
                new_thetas.append(r2.theta[i])

        return Racer(theta=new_thetas)

    def mutate(self, racer: Racer) -> Racer:
        theta_idx = random.randint(0, self.__n_thetas)
        new_theta = racer.theta()
        # TODO: check if [0, 100) is an appropriate range for the thetas
        new_theta[theta_idx] = 100*numpy.random.ranf()
        return Racer(theta=new_theta)
