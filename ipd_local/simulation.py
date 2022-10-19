import random
from tqdm import tqdm

from game_specs import *
from output_locations import *

from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout


def run_simulation(strats, rounds, blindness):
    
    print("Running simulation...")
    
    data = {}
    bad_functions = []
    
    with open(PROBLEMS_LOG_LOCATION, "a") as f:
        f.write("BAD CODE (RUNTIME) - NEW\nThe following functions had errors while playing the game and were blacklisted. If any, please rerun game with RELOAD_BLACKLIST = False:\n\n")
    
    for player1 in tqdm(strats):
        
        player1_is_valid = True
        dat={}

        for player2 in strats:
            
            if not player1_is_valid:
                break

            player2_is_valid = True

            player1moves = []
            player2moves = []
            results={}
            results['score']=[0, 0]
            
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
                    error = player1.__name__ + "\nError: " + str(e) + "\n"
                    with open(PROBLEMS_LOG_LOCATION, "a") as f:
                        f.write(error)                   
                    # print("\nBad function (player1):", player1.__name__)
                    # print(e)
                    # print("Removing from game.\n ---")
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
                    error = player2.__name__ + "\nError: " + str(e) + "\n"
                    with open(PROBLEMS_LOG_LOCATION, "a") as f:
                        f.write(error) 
                    # print("\nBad function (player2):", player2.__name__)
                    # print(e)
                    # print("Removing from game.\n ---")
                    bad_functions.append(player2)
                    strats.remove(player2)
                    player2_is_valid = False
                    break
                

                player1moves.append(player1move)
                player2moves.append(player2move)
            
            if not player1_is_valid:
                break
                       
            if not player2_is_valid:
                continue

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
            
            dat[player2.__name__]=results
        data[player1.__name__]=dat

    with open(BLACKLIST, "a") as f:
        for bad_function in bad_functions:
            f.write(bad_function.__name__ + "\n")

    with open(PROBLEMS_LOG_LOCATION, "a") as f:
        f.write("\n---\n***\n---\n\n")

    print("Simulation done.")
    
    return data




def reload_blacklist(all_strats, rounds, blindness):

    strats = all_strats.copy()
    
    bad_functions = []
    
    with open(PROBLEMS_LOG_LOCATION, "a") as f:
        f.write("BAD CODE (RUNTIME) - BLACKLISTED\nThe following functions had errors while playing the game, and thus were blacklisted:\n\n")
    
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
                    error = player1.__name__ + "\nError: " + str(e) + "\n"
                    with open(PROBLEMS_LOG_LOCATION, "a") as f:
                        f.write(error)                   
                    # print("\nBad function (player1):", player1.__name__)
                    # print(e)
                    # print("Removing from game.\n ---")
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
                    error = player2.__name__ + "\nError: " + str(e) + "\n"
                    with open(PROBLEMS_LOG_LOCATION, "a") as f:
                        f.write(error) 
                    # print("\nBad function (player2):", player2.__name__)
                    # print(e)
                    # print("Removing from game.\n ---")
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

    with open(PROBLEMS_LOG_LOCATION, "a") as f:
        f.write("\n---\n***\n---\n\n")

    # print()