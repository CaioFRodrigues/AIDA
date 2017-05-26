from copy import copy

class Racer:

    def __init__(self, n_features=-1, thetas=None):
        '''
        Use either n_features != -1 to init an empty racer with all the needed thetas,
        or thetas to use the given array of thetas
        '''

        self.__thetas = []
        self.__fitness = None

        if n_features != -1:
            n_thetas = (n_features + 1) * 5
            self.__thetas = [0] * n_thetas

        if thetas is not None:
            self.__thetas = copy(thetas)

    @classmethod
    def from_racer(Racer, r1: 'Racer') -> 'Racer':
        '''
        Don't use = to copy a racer to another -- that'd be a shallow copy.
        Instead, use: r2 = Racer.from_racer(r1)
        '''
        r1_thetas = copy(r1.thetas)
        r2 = Racer(thetas=r1_thetas)
        return r2

    @property
    def thetas(self) -> list:
        return self.__thetas

    @thetas.setter
    def thetas(self, val: list):
        if len(val) == len(self.__thetas):
            self.__thetas = copy(val)

    @property
    def fitness(self):
        return self.__fitness

    def calculate_fitness(self, controller):
        if self.__fitness is None:
            self.__fitness = controller.run_episode(self.__thetas)
