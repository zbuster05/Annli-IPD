# simulation specs
NOISE = False # whether or not this tournament has noise
NOISE_LEVEL = 0.1 # percentage noise; only used if NOISE is set to True
ROUNDS = 80 # number of rounds each strategy plays against each other strategy

# scores distribution, assuming symmetry
POINTS_BOTH_RAT = 1             # score for both players if they both rat
POINTS_DIFFERENT_WINNER = 10    # score for for ratting if opponent stays silent
POINTS_DIFFERENT_LOSER = 0      # score for staying silent if opponent rats
POINTS_BOTH_COOPERATE = 5       # score for both players when they cooperate

# run with default functions (always rat, always silent, tit for tat, etc).
# all default functions can be found in defaul_functions.py
INCLUDE_DEFAULTS = True

# whether or not to reload blacklisted functions
# not reloading speeds up simulation.
# however, it will cause problems if functions that are supposed to be blacklisted are not.
# thus, only set this variable to false if you are confident there has been no changes made to the submission sheet
RELOAD_BLACKLIST = True