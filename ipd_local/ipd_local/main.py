# main!!
# run this file to run the actual simulation

import json

from .game_specs import *
from .default_functions import *
from .data_analysis import *
from .simulation import *
from .get_inputs import *
from .output_locations import *

from loguru import logger
import sys

# EVERYTHING
# fetches latest data, runs simulation, updates sheets of results
def run_full_game():

    logger.remove()
    logger.add(PROBLEMS_LOG_LOCATION)
    logger.info("Starting!")

    strats, rounds, blindness = get_game_inputs() # fetches game inputs. function defined in get_inputs.py
    
    raw_data = run_simulation(strats, rounds, blindness) # runs simulation. function defined in simulation.py
    with open(RAW_OUT_LOCATION, 'w') as fp:
        json.dump(raw_data, fp) # dumps raw data of simulation to output location

    # dumps game specs to output location
    specs = {
        "Noise": NOISE,
        "Noise Level (if applicable)": NOISE_LEVEL,
        "Number of Rounds": ROUNDS,
        "Points when both rat": POINTS_BOTH_RAT,
        "Points for winner when different": POINTS_DIFFERENT_WINNER,
        "Points for loser when different": POINTS_DIFFERENT_LOSER,
        "Points when both cooperate": POINTS_BOTH_COOPERATE
    }    
    with open('./latest_specs.json', 'w') as fp:
        json.dump(specs, fp)

    update_sheet() # updates spreadsheet
    
    print("done!")

# runs full game!
run_full_game()
