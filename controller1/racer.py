import copy

class Racer:

    def __init__(self, n_features=-1, theta=None):
        '''
        Use either n_features != -1 to init an empty racer with all the needed thetas,
        or data to use the given array of thetas
        '''

        self.__theta = []

        if n_features != -1:
            n_thetas = (n_features + 1) * 5
            self.__theta = [0] * n_thetas

        if theta is not None:
            self.__theta = copy.copy(theta)

    @property
    def theta(self) -> list:
        return self.__theta

    @theta.setter
    def theta(self, val: list):
        if len(val) == len(self.__theta):
            self.__theta = copy.copy(val)

    @classmethod
    def from_racer(Racer, r1: 'Racer') -> 'Racer':
        '''
        Don't use = to copy a racer to another -- that'd be a shallow copy.
        Instead, use: r2 = Racer.from_racer(r1)
        '''
        data = copy.copy(r1.theta)
        r2 = Racer(-1, data)   # ignore n_features
        return r2   
        
    @property
    def fitness(self, controller):
        if self.__fitness is None:
            self.__fitness = controller.run_episodes(self.__thetas)
        return self.__fitness