"""
This module collects command line arguments and prepares everything needed to run the simulator/game

Example:
    To quickly start the game and observe sensor readings:

        $ python AIRacers.py -t track1 play
"""
import os
import argparse
import random
import datetime
import time
import numpy
import pygame
from controller1.controller import Controller
import tracks_config as track


def play(track_name: str, b_type: str) -> None:
    """
    Launches the simulator in a mode where the player can control each action with the arrow keys.
    
    :param str track_name: Name of a track, as defined in tracks_config.py
    :param str b_type: String
    :rtype: None
    """
    play_controller = Controller(track_name, bot_type=b_type)
    game_state = play_controller.game_state
    play_controller.sensors = [53, 66, 100, 1, 172.1353274581511, 150, -1, 0, 0]
    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direction = 1
                    feedback = game_state.frame_step(direction)
                    print("sensors  "+str(feedback))
                    print("features "+str(play_controller.compute_features(feedback)))
                    print("score    "+str(play_controller.game_state.car1.score))
                elif event.key == pygame.K_LEFT:
                    direction = 2
                    feedback = game_state.frame_step(direction)
                    print("sensors  "+str(feedback))
                    print("features "+str(play_controller.compute_features(feedback)))
                    print("score    " + str(play_controller.game_state.car1.score))
                elif event.key == pygame.K_UP:
                    direction = 3
                    feedback = game_state.frame_step(direction)
                    print("sensors  "+str(feedback))
                    print("features "+str(play_controller.compute_features(feedback)))
                    print("score    " + str(play_controller.game_state.car1.score))

                elif event.key == pygame.K_DOWN:
                    direction = 4
                    feedback = game_state.frame_step(direction)
                    print("sensors  "+str(feedback))
                    print("features "+str(play_controller.compute_features(feedback)))
                    print("score    " + str(play_controller.game_state.car1.score))


                if event.key == pygame.K_q:
                    exit()
                if event.key == pygame.K_r:
                    game_state.reset()
        pass


def parser() -> (argparse.Namespace, list):
    """
    Parses command line arguments.
    
    :return: a tuple containing parsed arguments and leftovers 
    """
    p = argparse.ArgumentParser(prog='gamename.py')
    mode_p = p.add_subparsers(dest='mode')
    mode_p.required = True
    p.add_argument('-w', nargs=1,
                   help='Specifies the weights\' file path; if not specified, a random vector of weights will be '
                        'generated.\n')
    p.add_argument('-b', nargs=1, choices=['parked_bots', 'dumb_bot', 'safe_bot', 'ninja_bot', 'custom_bot', 'none'],
                   help='Selects bot type')
    p.add_argument('-t', nargs=1,
                   help='Specifies the track you want to select; by default, track1 will be used. '
                        'Check the \'tracks.py\' file to see the available tracks/create new ones.\n')
    mode_p.add_parser('learn',
                      help='Starts %(prog)s in learning mode. This mode does not render the game to your screen, resulting in '
                           'faster learning.\n')
    mode_p.add_parser('evaluate',
                      help='Starts %(prog)s in evaluation mode. This mode runs your AI with the weights/parameters passed as parameter \n')
    mode_p.add_parser('play',
                      help='Starts %(prog)s in playing mode. You can control each action of the car using the arrow '
                           'keys of your keyboard.\n')

    arguments, leftovers = p.parse_known_args()
    p.parse_args()
    return arguments, leftovers


if __name__ == '__main__':

    args, trash = parser()

    # Selects track; by default track1 will be selected
    chosen_track = track.track1
    if args.t is None:
        chosen_track = track.track1
    else:
        for a_track in track.track.track_list:
            if args.t[0] == a_track.name:
                chosen_track = a_track

    # Sets weights
    if args.w is None:
        ctrl_temp = Controller(chosen_track, bot_type=None, evaluate=False)
        fake_sensors = [53, 66, 100, 1, 172.1353274581511, 150, -1, 0, 0]
        features_len = len(ctrl_temp.compute_features(fake_sensors))
        weights = [random.uniform(-1, 1) for i in range(0, features_len*5)]
    else:
        weights = numpy.loadtxt(args.w[0])

    # Selects Bot Type
    if args.b is None:
        bot_type = None
    elif args.b[0] == 'none':
        bot_type = None
    else:
        bot_type = args.b[0]

    # Starts simulator in play mode
    if str(args.mode) == 'play':
        play(chosen_track, bot_type)
    # Starts simulator in evaluate mode
    elif str(args.mode) == 'evaluate':
        ctrl = Controller(chosen_track, bot_type=bot_type)
        score = ctrl.run_episode(weights)
    # Starts simulator in learn mode and saves the best results in a file
    elif str(args.mode) == 'learn':
        ctrl = Controller(chosen_track, evaluate=False, bot_type=bot_type)
        result = ctrl.learn(weights)
        if not os.path.exists("./params"):
            os.makedirs("./params")
        output = "./params/%s.txt" % datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
        print(output)
        numpy.savetxt(output, result)
