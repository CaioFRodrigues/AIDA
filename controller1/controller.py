import controller_template as controller_template
from controller1.genetic_algorithms import Evolution
from numpy import array_split, inner as inner_product

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

        # features[2] => change in distance to grass from the left side
        #                   if positive: getting away from the grass
        #                   if negative: getting closer to the grass

        # features[3] => change in distance to grass from the right side
        #                   if positive: getting away from the grass
        #                   if negative: getting closer to the grass

        features = [1.0]
        if len(self.previous_sensor_values) > 0:
            features.append(sensors[4] - self.previous_sensor_values[1])
            features.append(sensors[0] - self.previous_sensor_values[2])
            features.append(sensors[2] - self.previous_sensor_values[3])
        else:
            features = [1.0, sensors[0], sensors[1], sensors[2]] # No previous values, the features just return the current sensor values

        self.previous_sensor_values = [value for value in sensors]
        return features


    def learn(self, weights) -> list:
        """
        IMPLEMENT YOUR LEARNING METHOD (i.e. YOUR LOCAL SEARCH ALGORITHM) HERE

        HINT: you can call self.run_episode (see controller_template.py) to evaluate a given set of weights
        :param weights: initial weights of the controller (either loaded from a file or generated randomly)
        :return: the best weights found by your learning algorithm, after the learning process is over
        """
        raise NotImplementedError("This Method Must Be Implemented")
