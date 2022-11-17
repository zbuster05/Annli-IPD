import ipd_local
from ipd_local.default_functions import *
import pytest

from ipd_local.game_specs import *
from ipd_local.default_functions import *
from ipd_local.simulation import *
from ipd_local.get_inputs import *
from ipd_local.output_locations import *
from ipd_local.data_analysis import *

import os
import random
import sys

import pandas as pd
from . import *



def test_full_game():
    sheet = pd.DataFrame([
    ["", "Quackary", "https://pastebin.com/gue8xdjr", "https://pastebin.com/fWAFkbPD" ],
    ["", "huxely. ", "https://pastebin.com/bjthjeT6", "https://pastebin.com/bjthjeT6" ],
    ["", "Jackary!", "https://pastebin.com/0fqA2Wtd", "https://pastebin.com/UxeqY68s" ],       
    ], columns = ["", "Student", "Regular", "Noise" ])
    set_temp_sheet("Test full game", sheet, tab_name="ASCII")
    data = get_spreadsheet_data("Test full game", "ASCII")
    strats = get_and_load_functions(data)
    out = run_simulation(strats)
    if not ipd_local.game_specs.NOISE:
        assert out == {
            "rat": {
                "silent": [POINTS_DIFFERENT_WINNER*ROUNDS, POINTS_DIFFERENT_LOSER*ROUNDS],
                "titFortat": [
                    POINTS_DIFFERENT_WINNER+POINTS_BOTH_RAT*(ROUNDS-1),
                    POINTS_DIFFERENT_LOSER+POINTS_BOTH_RAT*(ROUNDS-1)
                ]
            },
            "silent": {
                "rat": [POINTS_DIFFERENT_LOSER*ROUNDS, POINTS_DIFFERENT_WINNER*ROUNDS],
                "titFortat": [POINTS_BOTH_COOPERATE*ROUNDS, POINTS_BOTH_COOPERATE*ROUNDS],
            },
            "titFortat": {
                "rat": [
                    POINTS_DIFFERENT_LOSER+POINTS_BOTH_RAT*(ROUNDS-1),
                    POINTS_DIFFERENT_WINNER+POINTS_BOTH_RAT*(ROUNDS-1)
                ],
                "silent": [POINTS_BOTH_COOPERATE*ROUNDS, POINTS_BOTH_COOPERATE*ROUNDS],
            },
        }
    else:
        assert out["rat"]["silent"] == [POINTS_DIFFERENT_WINNER*ROUNDS, POINTS_DIFFERENT_LOSER*ROUNDS]
        assert out["silent"]["rat"] == [POINTS_DIFFERENT_LOSER*ROUNDS, POINTS_DIFFERENT_WINNER*ROUNDS]

        res = out["silent"]["titFortat"]
        assert abs((POINTS_BOTH_COOPERATE*(ROUNDS*9/10) + POINTS_DIFFERENT_LOSER*(ROUNDS/10)) - res[0]) < 5
        assert abs((POINTS_BOTH_COOPERATE*(ROUNDS*9/10) + POINTS_DIFFERENT_WINNER*(ROUNDS/10)) - res[1]) < 5
        res = out["titFortat"]["silent"]
        assert abs((POINTS_BOTH_COOPERATE*(ROUNDS*9/10) + POINTS_DIFFERENT_WINNER*(ROUNDS/10)) - res[0]) < 5
        assert abs((POINTS_BOTH_COOPERATE*(ROUNDS*9/10) + POINTS_DIFFERENT_LOSER*(ROUNDS/10)) - res[1]) < 5

        res = out["rat"]["titFortat"]
        assert abs((POINTS_BOTH_RAT*(ROUNDS*9/10) + POINTS_DIFFERENT_WINNER*(ROUNDS/10 + 1)) - res[0]) < 10
        assert abs((POINTS_BOTH_RAT*(ROUNDS*9/10) + POINTS_DIFFERENT_LOSER*(ROUNDS/10 + 1)) - res[1]) < 10
        res = out["titFortat"]["rat"]
        assert abs((POINTS_BOTH_RAT*(ROUNDS*9/10) + POINTS_DIFFERENT_LOSER*(ROUNDS/10 + 1)) - res[0]) < 10
        assert abs((POINTS_BOTH_RAT*(ROUNDS*9/10) + POINTS_DIFFERENT_WINNER*(ROUNDS/10 + 1)) - res[1]) < 10
