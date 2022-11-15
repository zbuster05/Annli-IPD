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

if __name__ == "__main__":
    logger.remove()
    logger.add(PROBLEMS_LOG_LOCATION)
    logger.info("Starting!")    
    
    data = get_spreadsheet_data()
    strats = get_and_load_functions(data)
    if INCLUDE_DEFAULTS:
        strats = all_default_functions + strats

    rounds = ROUNDS
    if NOISE:
        blindness = [NOISE_LEVEL, NOISE_LEVEL]
    else:
        blindness = [0,0]
    
    raw_data = run_simulation_parallel(strats)
    
    with open(RAW_OUT_LOCATION, 'w') as fp:
        fp.write(json.dumps(raw_data))
        
    specs = {
        "Noise": NOISE,
        "Noise Level (if applicable)": NOISE_LEVEL,
        "Noise Games Played Before Averaging (if applicable)": NOISE_GAMES_TILL_AVG,
        "Number of Rounds": ROUNDS,
        "Points when both rat": POINTS_BOTH_RAT,
        "Points for winner when different": POINTS_DIFFERENT_WINNER,
        "Points for loser when different": POINTS_DIFFERENT_LOSER,
        "Points when both cooperate": POINTS_BOTH_COOPERATE,
        "Debug mode (fixed random seed - should be off)": DEBUG_MODE,
    }    
    with open('./latest_specs.json', 'w') as fp:
        fp.write(json.dumps(specs))

    update_sheet()


