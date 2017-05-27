import controller_template as controller_template
from controller1.genetic_algorithms import Evolution
from controller1.hill_climbing import Hill_Climbing
from controller1.simulated_annealing import Simulated_Annealing
from numpy import array_split, inner as inner_product, arcsin
from math import sqrt
from simulator import Simulation


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

        # features[0] => constant 1.0
        #                   used to multiply the raw affinity for an action

        # features[1] => change in distance to checkpoint_distance
        #                   if positive: getting away from checkpoint
        #                   if negative: getting closer to checkpoint

        # features[2] => angle between car movement and left distance to grass
        #                   if positive: getting away from the grass
        #                   if negative: getting closer to the grass
        #                   the smallest the angle, the more it needs to turn right

        # features[3] => change in distance to grass from the right side
        #                   if positive: getting away from the grass
        #                   if negative: getting closer to the grass
        #                   the smallest the angle, the more it needs to turn left

        # features[4] => adversary proximity
        #                   if zero: not close enough to make the enemy the priority instead of the track
        #                   if positive: getting further away from the enemy_detected
        #                   if negative: getting closer to the enemy_detected
        #                   doesn't matter if adversary is in the front or behind, the closer the more
        #                   it needs to accelerate

        # features[5] => attempt to pass adversary in front_vector
        #               needs to have a little more weight than the grass proximity feature if this is not zero
        #               if positive: turn to the left
        #               if negative: turn to the right

        # possible feature[6] => attempt to stay as close as possible to position 1/-1 to the adversary
        # possible feature[7] => keep as close to the right edge as possible

        features = [1.0]
        if len(self.previous_sensor_values) > 0:

            # features[1]
                features.append(sensors[1] - self.previous_sensor_values[1])

            # features[2]
                front_vector = sensors[1] - self.previous_sensor_values[1]
                left_vector = sensors[0] - self.previous_sensor_values[0]
                if sqrt(front_vector ** 2 + left_vector ** 2) != 0:
                    angle = arcsin(front_vector / sqrt(front_vector ** 2 + left_vector ** 2))
                    features.append( 2* (angle - (-90)/90 - (-90)) -1 )
                else:
                    features.append(0)

            # features[3]
                front_vector = sensors[1] - self.previous_sensor_values[1]
                right_vector = sensors[2] - self.previous_sensor_values[2]
                if sqrt(front_vector ** 2 + right_vector ** 2) != 0:
                    angle = arcsin(front_vector / sqrt(front_vector ** 2 + right_vector ** 2))
                    features.append( 2* (angle - (-90)/90 - (-90)) -1 )
                else:
                    features.append(0)

            # features[4]
                if sensors[8] == 0:
                    features.append(0)
                else:
                    enemy_proximity = sensors[6] - self.previous_sensor_values[6]
                    features.append( 2 * (enemy_proximity/100))

            # features[5]
                if sensors[8] == 0:
                    features.append(0)
                else:
                    # Negative: coming from the left / positive: coming from the right
                    # Absolute value larger than 1: coming from behind / else: coming from the front
                    enemy_position = sensors[7] / 90.0
                    if (abs(enemy_position) > 1):
                        features.append(0)
                    else:
                        features.append(enemy_position)


        else:
            features = [1.0, sensors[4], sensors[0], sensors[2], 0, 0] # No previous values, the features just return the current sensor values

        self.previous_sensor_values = [value for value in sensors]
        return features


    def learn(self, weights) -> list:
        """
        IMPLEMENT YOUR LEARNING METHOD (i.e. YOUR LOCAL SEARCH ALGORITHM) HERE

        HINT: you can call self.run_episode (see controller_template.py) to evaluate a given set of weights
        :param weights: initial weights of the controller (either loaded from a file or generated randomly)
        :return: the best weights found by your learning algorithm, after the learning process is over
        """
        anneal = Simulated_Annealing(weights,self)
        weight = anneal.simulate(self)
        return weight
        #raise NotImplementedError("This Method Must Be Implemented")
