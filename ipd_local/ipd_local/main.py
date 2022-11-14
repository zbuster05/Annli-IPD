# main!!
# run this file to run the actual simulation

import json

from game_specs import *
from default_functions import *
from data_analysis import *
from simulation import *
from get_inputs import *
from output_locations import *

from loguru import logger
import sys
import time
import types

if DEBUG_MODE == True:
    random.seed(0) 

strats = []

def inc(x):
    return x+1

import marshal
import multiprocessing
# EVERYTHING
# fetches latest data, runs simulation, updates sheets of results
if __name__ == "__main__":
    logger.remove()
    logger.add(PROBLEMS_LOG_LOCATION)
    logger.info("Starting!")
    
    
    data = get_spreadsheet_data()
    students = get_students_and_code(data)    

    # # config for running game
    # # returns list of functions (strats), number of rounds, and blindness
    strats = load_functions(students)
    if INCLUDE_DEFAULTS: # include default functions if user desires
        strats = all_default_functions + strats
    rounds = ROUNDS
    blindness = []

    if NOISE:
        blindness = [NOISE_LEVEL, NOISE_LEVEL]
    else:
        blindness = [0,0]
    
    raw_data = run_simulation_parallel(strats, rounds, blindness) # runs simulation. function defined in simulation.py
    print("Dumping data...")
    old = time.time()
    with open(RAW_OUT_LOCATION, 'w') as fp:
        fp.write(json.dumps(raw_data)) # dumps raw data of simulation to output location
    print(f"Finished dumping data in {time.time()-old}s")
        
    # dumps game specs to output location
    specs = {
        "Noise": NOISE,
        "Noise Level (if applicable)": NOISE_LEVEL,
        "Noise Games Played Before Averaging (if applicable)": NOISE_GAMES_TILL_AVG,
        "Number of Rounds": ROUNDS,
        "Points when both rat": POINTS_BOTH_RAT,
        "Points for winner when different": POINTS_DIFFERENT_WINNER,
        "Points for loser when different": POINTS_DIFFERENT_LOSER,
        "Points when both cooperate": POINTS_BOTH_COOPERATE
    }    
    with open('./latest_specs.json', 'w') as fp:
        fp.write(json.dumps(specs))

    update_sheet() # updates spreadsheet
    
    # print("done!")

# # runs full game!
# run_full_game()


