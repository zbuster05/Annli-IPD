from game_specs import *
from default_functions import *
from simulation import *
from get_inputs import *

def main():
    strats, rounds, blindness = get_game_inputs()
    raw_data = run_simulation(strats, rounds, blindness)
    print("done!")

main()