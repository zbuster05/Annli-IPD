from game_specs import *
from default_functions import *
from data_analysis import *
from simulation import *
from get_inputs import *
import json

def run_full_game():
    strats, rounds, blindness = get_game_inputs()
    raw_data = run_simulation(strats, rounds, blindness)
    with open('./latest_raw_out.json', 'w') as fp:
        json.dump(raw_data, fp)

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
    
    print("done!")

run_full_game()