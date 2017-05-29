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
                controller.track = controller.track_1_state.track
                controller.track_name = controller.track_1_state.track
                controller.game_state = controller.track_1_state
                fitness_track_1 = controller.run_episode(self.__thetas)

                controller.bot_type = None
                controller.track = controller.track_2_state.track
                controller.track_name = controller.track_2_state.track
                controller.game_state = controller.track_2_state
                fitness_track_2 = controller.run_episode(self.__thetas)

                controller.bot_type = None
                controller.track = controller.track_3_state.track
                controller.track_name = controller.track_3_state.track
                controller.game_state = controller.track_3_state
                fitness_track_3 = controller.run_episode(self.__thetas)

                controller.bot_type = 'parked_bots'
                controller.track = controller.track_1_parked_state.track
                controller.track_name = controller.track_1_parked_state.track
                controller.game_state = controller.track_1_parked_state
                fitness_parked_track_1 = controller.run_episode(self.__thetas)

                controller.bot_type = 'parked_bots'
                controller.track = controller.track_3_parked_state.track
                controller.track_name = controller.track_3_parked_state.track
                controller.game_state = controller.track_3_parked_state
                fitness_parked_track_3 = controller.run_episode(self.__thetas)

                controller.bot_type = 'ninja_bot'
                controller.track = controller.track_1_ninja_state.track
                controller.track_name = controller.track_1_ninja_state.track
                controller.game_state = controller.track_1_ninja_state
                fitness_ninja_track_1 = controller.run_episode(self.__thetas)

                controller.bot_type = 'ninja_bot'
                controller.track = controller.track_3_ninja_state.track
                controller.track_name = controller.track_3_ninja_state.track
                controller.game_state = controller.track_3_ninja_state
                fitness_ninja_track_3 = controller.run_episode(self.__thetas)

                self.__fitness = (fitness_track_1 + fitness_track_2 + fitness_track_3 +
                                  fitness_parked_track_1 + fitness_parked_track_3 +
                                  fitness_ninja_track_1 + fitness_ninja_track_3) / 7

    def calculate_adjusted_fitness(self, adjust_amount):
        self.__adjusted_fitness = self.__fitness - adjust_amount
