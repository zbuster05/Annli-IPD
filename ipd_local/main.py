from game_specs import *
from default_functions import *
from data_analysis import *
from simulation import *
from get_inputs import *
import json

def run_full_game():
    strats, rounds, blindness = get_game_inputs()
    raw_data = run_simulation(strats, rounds, blindness)
    # df = pd.DataFrame(data=raw_data)
    # df.to_csv('./latest_raw_out.csv')
    with open('./latest_raw_out.json', 'w') as fp:
        json.dump(raw_data, fp)
    print("done!")

run_full_game()
produce_clean_data()