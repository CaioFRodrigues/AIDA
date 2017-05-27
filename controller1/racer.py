from copy import copy

class Racer:

    def __init__(self, thetas=None, n_features=-1):
        '''
        Use either n_features != -1 to init an empty racer with all the needed thetas,
        or thetas to use the given array of thetas
        '''

        self.__thetas = []
        self.__fitness = None
        self.__adjusted_fitness = None

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

    @property
    def adjusted_fitness(self):
        return self.__adjusted_fitness

    def calculate_fitness(self, controller, evaluate_averages=False):
        if self.__fitness is None:
            if not evaluate_averages:
                self.__fitness = controller.run_episode(self.__thetas)
            else:
                controller.bot_type = None
                controller.game_state = controller.no_bot_state
                fitness_none = controller.run_episode(self.__thetas)
                controller.bot_type = 'parked_bots'
                controller.game_state = controller.parked_bots_state
                fitness_parked = controller.run_episode(self.__thetas)
                controller.bot_type = 'ninja_bot'
                controller.game_state = controller.ninja_bot_state
                fitness_ninja = controller.run_episode(self.__thetas)
                self.__fitness = (fitness_none + fitness_parked + fitness_ninja) / 3

    def calculate_adjusted_fitness(self, adjust_amount):
        self.__adjusted_fitness = self.__fitness - adjust_amount
