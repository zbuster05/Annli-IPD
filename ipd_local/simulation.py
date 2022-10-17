import random
import copy
import time
from tqdm import tqdm

from game_specs import *

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
    data = {}
    for player1 in tqdm(strats):
        
        player1_is_valid = True

        start = time.time()
        dat={}
        avg=0

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
                        player1move = bool(player1(player1moves, player2moves, i))
                except Exception as e:
                    print("\nBad function (player1):", player1.__name__)
                    print(e)
                    print("Removing from game.\n ---")
                    strats.remove(player1)
                    player1_is_valid = False
                    break
                
                try:
                    with suppress_stdout():
                        player2move = bool(player2(player2moves, player1moves, i))
                except Exception as e:
                    print("\nBad function (player2):", player2.__name__)
                    print(e)
                    print("Removing from game.\n ---")
                    strats.remove(player2)
                    player2_is_valid = False
                    break
                

                player1moves.append(player1move)
                player2moves.append(player2move)
            
            if not (player1_is_valid and player2_is_valid):
                break

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
            avg+=results["score"][1]

        # dat["Average"]=float(avg/(len(strats)))
        # dat["Total"]=avg
        data[player1.__name__]=dat
        #print(player1.__name__, "took", time.time()-start, "seconds")
    
    # clean = copy.deepcopy(data)
    # for k in list(clean.keys()):
    #     for j in list(clean[k].keys()):
    #       if (type(clean[k][j])== dict):
    #         for key in list(clean[k][j].keys()):
    #             if key == "details":
    #                 del clean[k][j][key]
    # for k in list(clean.keys()):
    #     for j in list(clean[k].keys()):
    #       if (type(clean[k][j])== dict):
    #         clean[k][j] = list(clean[k][j].values())[0]
    
    return data