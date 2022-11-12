# main!!
# run this file to run the actual simulation

import orjson

from game_specs import *
from default_functions import *
from data_analysis import *
from simulation import *
from get_inputs import *
from output_locations import *

from loguru import logger
import sys
import time

# EVERYTHING
# fetches latest data, runs simulation, updates sheets of results
def run_full_game():

    logger.remove()
    logger.add(PROBLEMS_LOG_LOCATION)
    logger.info("Starting!")

    strats, rounds, blindness = get_game_inputs() # fetches game inputs. function defined in get_inputs.py
    
    raw_data = run_simulation(strats, rounds, blindness) # runs simulation. function defined in simulation.py
    print(type(raw_data))
    print(len(raw_data))
    print(raw_data["EllieLinPavlov"])
    print("Dumping data...")
    old = time.time()
    with open(RAW_OUT_LOCATION, 'wb') as fp:
        fp.write(orjson.dumps(raw_data)) # dumps raw data of simulation to output location
    print(f"Finished dumping data in {time.time()-old}s")
        
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
    with open('./latest_specs.json', 'wb') as fp:
        fp.write(orjson.dumps(specs, fp))

    update_sheet() # updates spreadsheet
    
    print("done!")

# runs full game!
run_full_game()
