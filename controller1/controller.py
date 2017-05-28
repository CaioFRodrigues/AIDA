import controller_template as controller_template
from controller1.genetic_algorithms import Evolution
from controller1.hill_climbing import Hill_Climbing
from controller1.simulated_annealing import Simulated_Annealing
from numpy import array_split, inner as inner_product, arcsin
from math import sqrt
from simulator import Simulation
import tracks_config

class Controller(controller_template.Controller):
    def __init__(self, track, evaluate=True, bot_type=None, previous_sensor_values=[]):
        super().__init__(track, evaluate=evaluate, bot_type=bot_type)
        self.previous_sensor_values = previous_sensor_values


    def take_action(self, parameters: list) -> int:
        """
        :param parameters: Current weights/parameters of your controller
        :return: An integer corresponding to an action:
        1 - Right
        2 - Left
        3 - Accelerate
        4 - Brake
        5 - Nothing
        """

        features = self.compute_features(self.sensors)
        q_params = array_split(parameters, 5)
        action_q = [inner_product(q_param, features) for q_param in q_params]
        max_action, _ = max(enumerate(action_q, 1), key=lambda a: a[1])

        return max_action


    def compute_features(self, sensors):
        """
        :param sensors: Car sensors at the current state s_t of the race/game
        contains (in order):
            track_distance_left: 1-100
            track_distance_center: 1-100
            track_distance_right: 1-100
            on_track: 0 or 1
            checkpoint_distance: 0-???
            car_velocity: 10-200
            enemy_distance: -1 or 0-???
            position_angle: -180 to 180
            enemy_detected: 0 or 1
          (see the specification file/manual for more details)
        :return: A list containing the features you defined
        """

        d_left, d_front, d_right, s_on_track = sensors[:4]
        d_next_checkpoint, v_car, d_enemy, a_enemy, s_enemy = sensors[4:]

        feature = [1.0, 0, 0, 0, 0]

        # incentives to accelerate
        feature[1] = 0.0
        if s_on_track and d_left < 100 and d_right < 100:
            feature[1] += 0.5
        else:
            feature[1] -= 0.5
        if d_front == 100 and (not s_enemy or a_enemy < -45 or a_enemy > 45):
            feature[1] += 0.5
        else:
            feature[1] -= 0.5

        # incentives to turn left
        feature[2] = 0.0
        if s_on_track and d_right < 100 and d_front < 100 \
           or s_enemy and d_enemy < 75 and a_enemy > 45 and a_enemy < 135:
            feature[2] += 0.5
        else:
            feature[2] -= 0.5
        if d_left == 100:
            feature[2] += 0.5
        else:
            feature[2] -= 0.5

        # incentives to turn right
        feature[3] = 0.0
        if s_on_track and d_left < 100 and d_front < 100 \
           or s_enemy and d_enemy < 75 and a_enemy < -45 and a_enemy > -135:
            feature[3] += 0.5
        else:
            feature[3] -= 0.5
        if d_right == 100:
            feature[3] += 0.5
        else:
            feature[3] -= 0.5

        # incentives to break
        feature[4] = 0.0
        if s_on_track and d_front < 100:
            feature[4] += 0.5
        else:
            feature[4] -= 0.5
        if s_enemy and a_enemy > -45 and a_enemy < 45:
            feature[4] += 0.5
        else:
            feature[4] -= 0.5

        return feature

    def learn(self, weights) -> list:
        """
        :param weights: initial weights of the controller (either loaded from a file or generated randomly)
        :return: the best weights found by your learning algorithm, after the learning process is over
        """
        #anneal = Simulated_Annealing(weights,self)
        #weight = anneal.simulate(self)
        #return weight
        self.track_1_state = Simulation(tracks_config.track1, None)
        self.track_2_state = Simulation(tracks_config.track2, None)
        self.track_3_state = Simulation(tracks_config.track3, None)
        self.parked_bots_state = Simulation(self.track_name, 'parked_bots')
        self.ninja_bot_state = Simulation(self.track_name, 'ninja_bot')
        evo = Evolution(max_population_size=50, n_actions=5, n_features=5, adam_genes=weights, best_overall=False)
        winner = evo.evolve(generations=500, controller=self)
