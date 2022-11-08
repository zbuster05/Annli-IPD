import random
from tqdm import tqdm

from game_specs import *
from output_locations import *

from loguru import logger

from contextlib import contextmanager
import sys, os

# suppress any print statements that submitted functions may have (as to not clutter terminal)
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


# runs ipd simulation!
# inputs: list of functions, number of rounds, and blindness (noise for each player, which we assume is symmetric)
# outputs: dictionary of dictionaries representing each matchup of functions. values are also dictionary:
    # "score": list of the scores for the players
    # "details": list of each player's moves on each round
def run_simulation(strats, rounds, blindness):

    print("Running simulation...")

    data = {}
    bad_functions = []

    # for every first player
    for player1 in tqdm(strats):

        player1_is_valid = True

        dat={} # datapoint for this player. terrible name choice ian.

        # play against all other players
        for player2 in strats:

            # ensure player is still valid (did not error)
            if not player1_is_valid:
                break

            player2_is_valid = True

            player1moves = []
            player2moves = []
            results={}
            results['score']=[0, 0]

            # play number of rounds specified by input parameter
            for i in range(rounds):

                # incorporate noise, if applicable
                # this code can be optimized but since i just took it from someone else i'm just leaving it like this for now
                if blindness[0] > 0:
                    if random.random()<blindness[0] and len(player1moves):
                        player1moves[-1] = not(player1moves[-1])
                if blindness[1] > 0:
                    if random.random()<blindness[1] and len(player2moves):
                        player2moves[-1] = not(player2moves[-1])

                # get player1's move for this round
                try:
                    with suppress_stdout():
                        player1move = player1(player1moves, player2moves, i)
                        if player1move==None:
                            raise Exception("returned none") # handle None separately because it is cast to False with the bool() function, which is not desired
                        player1move = bool(player1move) # casting allows player to output binary int instead of bool, if desired
                except Exception as e:
                    logger.error(f"Error running function {player1.__name__}: {str(e)}")
                    bad_functions.append(player1)
                    strats.remove(player1) # remove player1 from the simulation, so future functions don't play against it
                    player1_is_valid = False # player1 errored, so it is no longer valid
                    break # stop simulating this matchup

                # same for player2
                # see docs for player1
                try:
                    with suppress_stdout():
                        player2move = player2(player2moves, player1moves, i)
                        if player2move==None:
                            raise Exception("returned none")
                        player2move = bool(player2move)
                except Exception as e:
                    logger.error(f"Error running function {player2.__name__}: {str(e)}")
                    bad_functions.append(player2)
                    strats.remove(player2)
                    player2_is_valid = False
                    break

                player1moves.append(player1move)
                player2moves.append(player2move)

            # do not log scores if either player is invalid
            if not player1_is_valid:
                break
            if not player2_is_valid:
                continue

            # calculate scores
            for i in range(rounds):
                if player1moves[i]:
                    if player2moves[i]:
                        results['score'][0]+=POINTS_BOTH_RAT
                        results['score'][1]+=POINTS_BOTH_RAT
                    else:
                        results['score'][0]+=POINTS_DIFFERENT_LOSER
                        results['score'][1]+=POINTS_DIFFERENT_WINNER
                else:
                    if player2moves[i]:
                        results['score'][0]+=POINTS_DIFFERENT_WINNER
                        results['score'][1]+=POINTS_DIFFERENT_LOSER
                    else:
                        results['score'][0]+=POINTS_BOTH_COOPERATE
                        results['score'][1]+=POINTS_BOTH_COOPERATE
                results['details']=[player1moves, player2moves]

            # create datapoint for matchup
            dat[player2.__name__]=results

        # create datapoint for player1
        data[player1.__name__]=dat

    # update blacklist. hopefully this does nothing; the goal of the blacklist filtering function is to get rid of bad functions.
    with open(BLACKLIST, "a") as f:
        for bad_function in bad_functions:
            f.write(bad_function.__name__ + "\n")

    print("Simulation done.")

    return data


# reloads blacklisted functions by running the simulation without outputting anything
# updates blacklist.txt for every function that errors
# see documentation for run_simulation function
def reload_blacklist(all_strats, rounds, blindness):

    # important!!! create copy of strats as not to modify original list and mess things up
    strats = all_strats.copy()

    bad_functions = []

    for player1 in tqdm(strats):

        player1_is_valid = True

        for player2 in strats:

            if not player1_is_valid:
                break

            player2_is_valid = True

            player1moves = []
            player2moves = []

            for i in range(rounds):
                if blindness[0] > 0:
                    if random.random()<blindness[0] and len(player1moves):
                        player1moves[-1] = not(player1moves[-1])
                if blindness[1] > 0:
                    if random.random()<blindness[1] and len(player2moves):
                        player2moves[-1] = not(player2moves[-1])

                try:
                    with suppress_stdout():
                        player1move = player1(player1moves, player2moves, i)
                        if player1move==None:
                            raise Exception("returned none")
                        player1move = bool(player1move)
                except Exception as e:
                    logger.error(f"Error running function {player1.__name__}: {str(e)}")
                    bad_functions.append(player1)
                    strats.remove(player1)
                    player1_is_valid = False
                    break

                try:
                    with suppress_stdout():
                        player2move = player2(player2moves, player1moves, i)
                        if player2move==None:
                            raise Exception("returned none")
                        player2move = bool(player2move)
                except Exception as e:
                    logger.error(f"Error running function {player2.__name__}: {str(e)}")                    
                    bad_functions.append(player2)
                    strats.remove(player2)
                    player2_is_valid = False
                    break

                player1moves.append(player1move)
                player2moves.append(player2move)

    open(BLACKLIST, 'w').close()
    with open(BLACKLIST, "a") as f:
        for bad_function in bad_functions:
            f.write(bad_function.__name__ + "\n")
